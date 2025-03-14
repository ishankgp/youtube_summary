from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from typing import Optional, List, Dict, Union
from enum import Enum
import re
import logging
from datetime import timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranscriptError(Exception):
    """Custom exception for transcript-related errors."""
    pass

class TranscriptLanguage(str, Enum):
    """Supported transcript languages."""
    ENGLISH = "en"
    HINDI = "hi"
    AUTO = "auto"

def format_duration(seconds: float) -> str:
    """Convert duration in seconds to human-readable format."""
    return str(timedelta(seconds=int(seconds)))

def extract_video_id(url: str) -> str:
    """
    Extract video ID from various YouTube URL formats.
    
    Supported formats:
    - youtube.com/watch?v=VIDEO_ID
    - youtu.be/VIDEO_ID
    - youtube.com/v/VIDEO_ID
    - youtube.com/embed/VIDEO_ID
    """
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise TranscriptError(
        "Invalid YouTube URL format. Please provide a valid YouTube video URL."
    )

def get_transcript(
    url: str,
    preferred_language: Union[TranscriptLanguage, str] = TranscriptLanguage.AUTO
) -> Dict[str, any]:
    """
    Get transcript from YouTube video URL with language preference handling.
    
    Args:
        url: YouTube video URL
        preferred_language: Preferred transcript language (en, hi, or auto)
    
    Returns:
        Dictionary containing:
        - text: The transcript text
        - language: Language code of the transcript
        - duration: Video duration in seconds
        - translated: Whether the transcript was translated
        - original_language: Original language if translated
    
    Raises:
        TranscriptError: If transcript cannot be fetched or processed
    """
    try:
        logger.info(f"Fetching transcript for URL: {url}")
        video_id = extract_video_id(url)
        
        # Get list of available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = None
        language = None
        
        # Convert string to enum if needed
        if isinstance(preferred_language, str):
            preferred_language = TranscriptLanguage(preferred_language.lower())
        
        # Try to get transcript in preferred language
        if preferred_language != TranscriptLanguage.AUTO:
            try:
                transcript = transcript_list.find_transcript([preferred_language.value])
                language = preferred_language.value
                logger.info(f"Found transcript in preferred language: {language}")
            except NoTranscriptFound:
                logger.warning(f"No transcript found in preferred language: {preferred_language}")
        
        # If no preferred language or not found, try language priority
        if not transcript:
            for lang in [TranscriptLanguage.HINDI, TranscriptLanguage.ENGLISH]:
                try:
                    transcript = transcript_list.find_transcript([lang.value])
                    language = lang.value
                    logger.info(f"Found transcript in language: {language}")
                    break
                except NoTranscriptFound:
                    continue
        
        # If still no transcript, try any available transcript
        if not transcript:
            try:
                transcript = transcript_list.find_manually_created_transcript()
                language = transcript.language_code
                logger.info(f"Found manual transcript in language: {language}")
            except NoTranscriptFound:
                transcript = transcript_list.find_generated_transcript()
                language = transcript.language_code
                logger.info(f"Found auto-generated transcript in language: {language}")
        
        # Get the actual transcript data
        transcript_data = transcript.fetch()
        
        # Calculate video duration from last entry
        duration = 0
        if transcript_data:
            last_entry = transcript_data[-1]
            duration = float(last_entry['start']) + float(last_entry['duration'])
        
        # Combine transcript entries into a single string with timestamps
        full_transcript = ""
        for entry in transcript_data:
            timestamp = format_duration(float(entry['start']))
            text = entry['text'].strip()
            if text:
                full_transcript += f"[{timestamp}] {text}\n"
        
        result = {
            "text": full_transcript.strip(),
            "language": language,
            "duration": duration,
            "translated": False,
            "original_language": language
        }
        
        # If transcript is not in preferred language and auto-translation is available
        if (preferred_language != TranscriptLanguage.AUTO and 
            language != preferred_language.value and 
            preferred_language.value in transcript_list.translation_languages):
            try:
                translated = transcript.translate(preferred_language.value).fetch()
                translated_text = ""
                for entry in translated:
                    timestamp = format_duration(float(entry['start']))
                    text = entry['text'].strip()
                    if text:
                        translated_text += f"[{timestamp}] {text}\n"
                
                result.update({
                    "text": translated_text.strip(),
                    "language": preferred_language.value,
                    "translated": True,
                    "original_language": language
                })
                logger.info(f"Successfully translated transcript to {preferred_language.value}")
            except Exception as e:
                logger.warning(f"Translation failed: {str(e)}")
        
        return result
        
    except TranscriptsDisabled:
        logger.error(f"Transcripts are disabled for video: {url}")
        raise TranscriptError(
            "Transcripts are disabled for this video. Please try a different video."
        )
    except NoTranscriptFound:
        logger.error(f"No transcript found for video: {url}")
        raise TranscriptError(
            "No transcript available for this video. Please try a different video."
        )
    except Exception as e:
        logger.error(f"Error fetching transcript: {str(e)}")
        raise TranscriptError(f"Failed to get transcript: {str(e)}")

def test_transcript():
    """Test function to verify transcript functionality."""
    test_urls = [
        "https://www.youtube.com/watch?v=V-LLrIlFAdQ",  # Known video with transcript
        "https://youtu.be/V-LLrIlFAdQ",  # Short URL format
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        try:
            # Test with different language preferences
            for lang in TranscriptLanguage:
                print(f"\nTrying language: {lang.value}")
                result = get_transcript(url, lang)
                print(f"Success! Found transcript in {result['language']}")
                print(f"Duration: {format_duration(result['duration'])}")
                print(f"Translated: {result['translated']}")
                if result['translated']:
                    print(f"Original language: {result['original_language']}")
                print(f"First 200 chars:\n{result['text'][:200]}...")
        except TranscriptError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_transcript()