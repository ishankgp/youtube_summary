from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.proxies import WebshareProxyConfig
from typing import Optional, List, Dict, Union, Tuple
from enum import Enum
import re
import logging
from datetime import timedelta
from youtube_transcript_api.formatters import TextFormatter
import time
from urllib.parse import urlparse, parse_qs
import os
import random

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_proxy_config() -> Optional[WebshareProxyConfig]:
    """Get Webshare proxy configuration from environment variables"""
    webshare_username = os.getenv("WEBSHARE_USERNAME")
    webshare_password = os.getenv("WEBSHARE_PASSWORD")
    
    if webshare_username and webshare_password:
        logger.info("Using Webshare proxy configuration")
        return WebshareProxyConfig(
            proxy_username=webshare_username,
            proxy_password=webshare_password
        )
    
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        logger.warning("No Webshare proxy credentials configured. YouTube may block requests from Railway's IP.")
    return None

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
    """Extract video ID from YouTube URL with detailed logging"""
    try:
        logger.info(f"Extracting video ID from URL: {url}")
        
        # Handle different URL formats
        parsed_url = urlparse(url)
        if parsed_url.hostname and ('youtube.com' in parsed_url.hostname or 'youtu.be' in parsed_url.hostname):
            if parsed_url.hostname == 'youtu.be':
                video_id = parsed_url.path[1:]
            else:
                query_params = parse_qs(parsed_url.query)
                video_id = query_params.get('v', [None])[0]
            
            if video_id:
                logger.info(f"Successfully extracted video ID: {video_id}")
                return video_id
            
        raise ValueError("Invalid YouTube URL format")
    except Exception as e:
        logger.error(f"Error extracting video ID: {str(e)}")
        raise TranscriptError(f"Invalid YouTube URL: {str(e)}")

def get_transcript(video_id: str, language: str = None, retries: int = 3) -> Tuple[str, str]:
    logger.debug(f"Attempting to fetch transcript for video {video_id} in language {language}")
    
    # Get proxy configuration
    proxy_config = get_proxy_config()
    yt_api = YouTubeTranscriptApi(proxy_config=proxy_config)
    
    for attempt in range(retries):
        try:
            # First, get available transcripts to check languages
            transcript_list = yt_api.list_transcripts(video_id)
            available_languages = [t.language_code for t in transcript_list._manually_created_transcripts.values()]
            available_auto = [t.language_code for t in transcript_list._generated_transcripts.values()]
            
            logger.debug(f"Available manual transcripts: {available_languages}")
            logger.debug(f"Available auto-generated transcripts: {available_auto}")
            
            # Try different approaches
            approaches = [
                ("standard", lambda: yt_api.get_transcript(video_id, languages=[language] if language else None)),
                ("cookies-disabled", lambda: yt_api.get_transcript(video_id, languages=[language] if language else None, cookies='CONSENT=YES+1')),
                ("no-headers", lambda: yt_api.get_transcript(video_id, languages=[language] if language else None, headers={})),
                ("minimal-headers", lambda: yt_api.get_transcript(video_id, languages=[language] if language else None, headers={'User-Agent': 'Mozilla/5.0'}))
            ]
            
            last_error = None
            for approach_name, approach_func in approaches:
                try:
                    logger.debug(f"Trying {approach_name} approach for video {video_id}")
                    transcript_data = approach_func()
                    actual_language = language or 'en'  # Default to English if no language specified
                    logger.info(f"Successfully fetched transcript using {approach_name} approach")
                    return transcript_data, actual_language
                except Exception as e:
                    last_error = e
                    logger.debug(f"{approach_name} approach failed: {str(e)}")
            
            if last_error:
                raise last_error
            
        except TranscriptsDisabled:
            logger.error(f"Transcripts are disabled for video {video_id}")
            raise
        except NoTranscriptFound:
            logger.error(f"No transcript found for video {video_id} in language {language}")
            raise
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{retries} failed: {str(e)}")
            if attempt == retries - 1:
                raise
            time.sleep(1)  # Wait before retry
    
    raise Exception("All approaches failed to fetch transcript")

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
                result = get_transcript(url, lang.value)
                print(f"Success! Found transcript in {result['language']}")
                print(f"Duration: {format_duration(result['duration'])}")
                print(f"Translated: {result['translated']}")
                if result['translated']:
                    print(f"Original language: {result['original_language']}")
                print(f"First 200 chars:\n{result['text'][:200]}...")
        except TranscriptError as e:
            print(f"Error: {str(e)}")

def diagnose_video(video_url: str):
    """
    Diagnostic function to check transcript availability and details for a video.
    """
    try:
        video_id = extract_video_id(video_url)
        logger.info(f"Diagnosing video {video_id}")
        
        # Get proxy configuration
        proxy_config = get_proxy_config()
        yt_api = YouTubeTranscriptApi(proxy_config=proxy_config)
        
        # Get transcript list
        transcript_list = yt_api.list_transcripts(video_id)
        
        # Log manual transcripts
        manual_transcripts = transcript_list._manually_created_transcripts
        logger.info("Manual transcripts:")
        for lang, transcript in manual_transcripts.items():
            logger.info(f"  - {lang}: {transcript.language_code} (is_translatable: {transcript.is_translatable})")
        
        # Log auto-generated transcripts
        auto_transcripts = transcript_list._generated_transcripts
        logger.info("Auto-generated transcripts:")
        for lang, transcript in auto_transcripts.items():
            logger.info(f"  - {lang}: {transcript.language_code} (is_translatable: {transcript.is_translatable})")
        
        # Try to fetch default transcript
        try:
            default_transcript = transcript_list.find_manually_created_transcript()
            logger.info(f"Default transcript language: {default_transcript.language_code}")
            logger.info(f"Default transcript is translatable: {default_transcript.is_translatable}")
        except Exception as e:
            logger.warning(f"Could not get default transcript: {str(e)}")
        
        # Try English specifically
        try:
            en_transcript = transcript_list.find_transcript(['en'])
            logger.info("English transcript is available")
            # Try to fetch it
            transcript_data = en_transcript.fetch()
            logger.info(f"Successfully fetched English transcript with {len(transcript_data)} segments")
        except Exception as e:
            logger.warning(f"English transcript test failed: {str(e)}")
            
    except Exception as e:
        logger.error(f"Diagnosis failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_transcript()