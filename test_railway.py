import requests
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BACKEND_URL = "https://web-production-5da4a.up.railway.app"
TEST_VIDEO_URL = "https://www.youtube.com/watch?v=akEAGqxAvsI"

def test_health() -> bool:
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/")
        logger.info(f"Health check status: {response.status_code}")
        logger.info(f"Health check response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return False

def test_transcript(url: str, language: str = "auto") -> Dict[str, Any]:
    """Test transcript fetching for a specific URL"""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "urls": [url],
            "preferred_language": language
        }
        
        logger.info(f"Testing transcript fetch for URL: {url}")
        logger.info(f"Request payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BACKEND_URL}/api/transcripts",
            headers=headers,
            json=payload,
            timeout=30  # Increased timeout for transcript fetching
        )
        
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info("Transcript fetch successful!")
            logger.info(f"Transcript languages: {[t['language'] for t in result['transcripts'].values()]}")
            logger.info(f"Transcript lengths: {[len(t['transcript']) for t in result['transcripts'].values()]}")
            return result
        else:
            logger.error(f"Error response: {response.text}")
            return {"error": response.text}
            
    except Exception as e:
        logger.error(f"Transcript test failed: {str(e)}")
        return {"error": str(e)}

def main():
    """Run all tests"""
    logger.info("Starting Railway backend tests...")
    
    # Test 1: Health Check
    logger.info("\n=== Testing Health Check ===")
    if test_health():
        logger.info("✅ Health check passed")
    else:
        logger.error("❌ Health check failed")
    
    # Test 2: Transcript Fetch (Auto language)
    logger.info("\n=== Testing Transcript Fetch (Auto) ===")
    auto_result = test_transcript(TEST_VIDEO_URL)
    if "error" not in auto_result:
        logger.info("✅ Auto language transcript test passed")
    else:
        logger.error("❌ Auto language transcript test failed")
    
    # Test 3: Transcript Fetch (English)
    logger.info("\n=== Testing Transcript Fetch (English) ===")
    en_result = test_transcript(TEST_VIDEO_URL, "en")
    if "error" not in en_result:
        logger.info("✅ English transcript test passed")
    else:
        logger.error("❌ English transcript test failed")

if __name__ == "__main__":
    main() 