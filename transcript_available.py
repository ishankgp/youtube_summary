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
        
        try:
            # Get list of available transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            logger.info("Successfully retrieved transcript list")
        except Exception as e:
            logger.error(f"Error listing transcripts: {str(e)}")
            raise TranscriptError(
                "Could not access video transcripts. Please check if the video exists and has captions enabled."
            )

        transcript = None
        language = None
        translated = False
        original_language = None
        
        # Convert string to enum if needed
        if isinstance(preferred_language, str):
            preferred_language = TranscriptLanguage(preferred_language.lower())

        try:
            # First try: Get transcript in preferred language
            if preferred_language != TranscriptLanguage.AUTO:
                try:
                    transcript = transcript_list.find_transcript([preferred_language.value])
                    language = preferred_language.value
                    logger.info(f"Found transcript in preferred language: {language}")
                except NoTranscriptFound:
                    logger.info(f"No transcript found in preferred language: {preferred_language.value}")

            # Second try: Try English or Hindi
            if not transcript:
                for lang in [TranscriptLanguage.ENGLISH.value, TranscriptLanguage.HINDI.value]:
                    try:
                        transcript = transcript_list.find_transcript([lang])
                        language = lang
                        logger.info(f"Found transcript in language: {language}")
                        break
                    except NoTranscriptFound:
                        continue

            # Third try: Get any available transcript
            if not transcript:
                try:
                    transcript = transcript_list.find_transcript([])
                    language = transcript.language_code
                    logger.info(f"Found transcript in language: {language}")
                except NoTranscriptFound:
                    raise NoTranscriptFound("No transcript found in any language")

        except NoTranscriptFound as e:
            logger.error(f"No transcript found for video: {url}")
            raise TranscriptError(
                "No transcript available for this video. Please check if captions are enabled."
            )
        except Exception as e:
            logger.error(f"Error finding transcript: {str(e)}")
            raise TranscriptError(f"Failed to find transcript: {str(e)}")
        
        # Get the actual transcript data
        try:
            transcript_data = transcript.fetch()
            logger.info("Successfully fetched transcript data")
        except Exception as e:
            logger.error(f"Error fetching transcript data: {str(e)}")
            raise TranscriptError(f"Failed to fetch transcript data: {str(e)}")
        
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
            "translated": translated,
            "original_language": language
        }
        
        # Try translation if needed and available
        if (preferred_language != TranscriptLanguage.AUTO and 
            language != preferred_language.value):
            try:
                # Check if translation is available
                translation_languages = transcript_list.translation_languages
                logger.info(f"Available translation languages: {translation_languages}")
                
                if preferred_language.value in translation_languages:
                    translated_transcript = transcript.translate(preferred_language.value).fetch()
                    translated_text = ""
                    for entry in translated_transcript:
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
                logger.warning(f"Translation failed, using original transcript: {str(e)}")
        
        return result
        
    except TranscriptsDisabled:
        logger.error(f"Transcripts are disabled for video: {url}")
        raise TranscriptError(
            "Transcripts are disabled for this video. Please check if captions are enabled."
        )
    except Exception as e:
        logger.error(f"Error in get_transcript: {str(e)}")
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
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_transcript()