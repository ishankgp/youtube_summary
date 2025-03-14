import google.generativeai as genai
import os
from typing import Dict
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not found in environment variables")
    logger.info("Please create a .env file in the root directory with your Gemini API key:")
    logger.info("GEMINI_API_KEY=your_api_key_here")
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check .env file.")

# Configure the API
genai.configure(api_key=GEMINI_API_KEY)

class AIHandler:
    def __init__(self):
        # Configure the model
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-lite-preview-02-05",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

    async def generate_summary(self, transcript: str, prompt: str, language: str = "en") -> Dict[str, str]:
        """
        Generate a summary of the transcript using Gemini API.
        """
        try:
            system_prompt = f"""You are a helpful AI assistant that summarizes video transcripts.
            Language of transcript: {language}
            Task: {prompt}
            
            You will receive transcripts from one or more videos. Each video transcript is clearly marked.
            Please provide a structured summary in the following format:

            # Overall Summary
            [A comprehensive overview combining insights from all videos]

            ## Key Points from Each Video
            ### Video 1
            - [Key points from first video]
            
            ### Video 2
            - [Key points from second video]
            [Continue for each video...]

            ## Common Themes & Insights
            - [Themes that appear across multiple videos]
            - [Connections between different videos]

            ## Notable Quotes
            > "Quote text here" - Video X
            > "Another quote text" - Video Y

            ## Additional Insights
            [Any other relevant observations or analysis]

            IMPORTANT FORMATTING RULES:
            1. Use markdown headers (#, ##, ###) for section titles only
            2. DO NOT use any bold formatting (** **) in the content
            3. DO NOT use any other markdown formatting except for:
               - Headers (#, ##, ###)
               - Bullet points (-)
               - Quote blocks (>) for the Notable Quotes section
            4. Keep all content in regular weight text, not bold
            5. For quotes, use the exact format: > "Quote text" - Source

            Please ensure:
            1. Each video's content is clearly represented
            2. Connections between videos are highlighted
            3. The summary is comprehensive but concise
            4. Key points are properly attributed to their source videos
            5. NO bold formatting is used in the content
            """

            # Combine prompts and transcript
            full_prompt = f"{system_prompt}\n\nTranscript:\n{transcript}"

            logger.info("Generating summary with Gemini API")
            
            # Generate content
            response = await self.model.generate_content_async(
                contents=full_prompt,
                stream=False
            )

            # Check if response has text
            if not response.text:
                raise Exception("Empty response from Gemini API")

            return {
                "summary": response.text,
                "language": language
            }

        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise

    async def refine_summary(self, summary: str, feedback: str) -> str:
        """
        Entre Prompt 
        """
        try:
            prompt = f"Please refine this summary based on the following feedback:\n\nOriginal Summary:\n{summary}\n\nFeedback:\n{feedback}"
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error refining summary: {str(e)}")
            raise 