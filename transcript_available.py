# code to get transcript of a youtube video when transcript is available . 
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from typing import Optional, List, Dict
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranscriptError(Exception):
    pass

def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise TranscriptError("Invalid YouTube URL format")

def get_transcript(url: str) -> Dict[str, str]:
    """
    Get transcript from YouTube video URL.
    Returns a dictionary containing the transcript and language.
    """
    try:
        logger.info(f"Fetching transcript for URL: {url}")
        video_id = extract_video_id(url)
        
        # Get list of available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        try:
            # First try to get Hindi transcript for Hindi videos
            transcript = transcript_list.find_transcript(['hi'])
            language = 'hi'
        except NoTranscriptFound:
            try:
                # Then try English
                transcript = transcript_list.find_transcript(['en'])
                language = 'en'
            except NoTranscriptFound:
                # If neither Hindi nor English, get the first available transcript
                transcript = transcript_list.find_manually_created_transcript()
                language = transcript.language_code
                
                # If no manual transcript, try auto-generated
                if not transcript:
                    transcript = transcript_list.find_generated_transcript()
                    language = transcript.language_code

        # Get the actual transcript
        transcript_data = transcript.fetch()
        
        # Combine transcript entries into a single string
        full_transcript = " ".join(entry['text'] for entry in transcript_data)
        
        # If transcript is not in English, try to translate it
        if language != 'en':
            try:
                translated_transcript = transcript.translate('en').fetch()
                translated_text = " ".join(entry['text'] for entry in translated_transcript)
                return {
                    "transcript": translated_text,
                    "original_transcript": full_transcript,
                    "language": language,
                    "translated": True
                }
            except Exception as e:
                logger.warning(f"Could not translate transcript: {str(e)}")
        
        logger.info(f"Successfully fetched transcript in language: {language}")
        return {
            "transcript": full_transcript,
            "language": language,
            "translated": False
        }
        
    except TranscriptsDisabled:
        logger.error(f"Transcripts are disabled for video: {url}")
        raise TranscriptError("Transcripts are disabled for this video")
    except NoTranscriptFound:
        logger.error(f"No transcript found for video: {url}")
        raise TranscriptError("No transcript available for this video")
    except Exception as e:
        logger.error(f"Error fetching transcript: {str(e)}")
        raise TranscriptError(f"Failed to get transcript: {str(e)}")

# Add this test function
def test_transcript():
    url = "https://www.youtube.com/watch?v=V-LLrIlFAdQ"
    try:
        result = get_transcript(url)
        print("Transcript retrieved successfully:")
        print(f"Language: {result['language']}")
        print(f"Transcript: {result['transcript'][:500]}...")  # First 500 chars
    except TranscriptError as e:
        print(f"Error getting transcript: {e}")

if __name__ == "__main__":
    test_transcript()