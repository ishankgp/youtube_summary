import requests
import json
import logging
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://web-production-5da4a.up.railway.app"

def test_direct_youtube_api():
    """Test YouTube Transcript API directly with different configurations"""
    test_videos = [
        "dQw4w9WgXcQ",  # Known video with captions
        "V-LLrIlFAdQ",  # Alternative video
        "9bZkp7q19f0"   # Gangnam Style (very popular, likely to have captions)
    ]
    
    for video_id in test_videos:
        try:
            logger.info(f"\nTesting direct API access for video: {video_id}")
            
            # Try without any special configuration
            logger.info("Attempting standard API call...")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Check available languages
            manual = list(transcript_list._manually_created_transcripts.keys())
            auto = list(transcript_list._generated_transcripts.keys())
            logger.info(f"Available manual transcripts: {manual}")
            logger.info(f"Available auto-generated: {auto}")
            
            # Try to fetch English transcript
            transcript = transcript_list.find_transcript(['en'])
            text = transcript.fetch()
            logger.info(f"Successfully fetched transcript with {len(text)} entries")
            return True
        except Exception as e:
            logger.error(f"Error with video {video_id}: {str(e)}")
    return False

def test_health():
    response = requests.get(f"{BASE_URL}/")
    logger.info(f"Health check response: {response.status_code}")
    logger.info(f"Response content: {response.json()}")
    return response.status_code == 200

def test_transcripts():
    headers = {"Content-Type": "application/json"}
    # Try with a very short video that's likely to have captions
    data = {
        "urls": ["https://www.youtube.com/watch?v=9bZkp7q19f0"],
        "preferred_language": "auto"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/transcripts",
            headers=headers,
            json=data
        )
        logger.info(f"Transcript response status: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        logger.info(f"Response content: {response.text}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error testing transcripts: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Testing direct YouTube API access...")
    direct_ok = test_direct_youtube_api()
    logger.info(f"Direct API test {'passed' if direct_ok else 'failed'}\n")
    
    logger.info("Testing health check endpoint...")
    health_ok = test_health()
    logger.info(f"Health check {'passed' if health_ok else 'failed'}\n")
    
    logger.info("Testing transcripts endpoint...")
    transcripts_ok = test_transcripts()
    logger.info(f"Transcripts test {'passed' if transcripts_ok else 'failed'}") 