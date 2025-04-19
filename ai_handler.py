import google.generativeai as genai
import os
from typing import Dict, List
import logging
from dotenv import load_dotenv
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables")
    logger.info("API will be unavailable for summary generation until key is provided")
    GEMINI_API_KEY = "dummy_key_for_startup"  # Allow app to start for health checks

# Configure the API
genai.configure(api_key=GEMINI_API_KEY)

class AIHandler:
    def __init__(self):
        """Initialize the AI handler with Gemini model."""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.warning("No Gemini API key found. Some features will be limited.")
                self.model = None
                return

            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini AI model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Gemini AI model: {str(e)}")
            self.model = None
    
    def _extract_video_titles(self, transcript: str) -> List[Dict[str, str]]:
        """
        Extract video titles and their transcripts from the combined transcript.
        Returns a list of dictionaries containing video titles and their transcripts.
        """
        videos = []
        current_video = None
        current_transcript = []
        
        for line in transcript.split('\n'):
            # Match lines starting with "Video:" or "Video (id):"
            video_match = re.match(r'Video(?:\s*\(([^)]+)\))?\s*:\s*(.+)?', line.strip())
            if video_match:
                # If we have a previous video, save it
                if current_video is not None:
                    videos.append({
                        'id': current_video.get('id', ''),
                        'title': current_video.get('title', ''),
                        'transcript': '\n'.join(current_transcript).strip()
                    })
                # Start a new video
                current_video = {
                    'id': video_match.group(1) or '',
                    'title': video_match.group(2) or ''
                }
                current_transcript = []
            elif current_video is not None:
                current_transcript.append(line)
        
        # Add the last video
        if current_video is not None:
            videos.append({
                'id': current_video.get('id', ''),
                'title': current_video.get('title', ''),
                'transcript': '\n'.join(current_transcript).strip()
            })
        
        return videos

    async def generate_summary(self, transcript: str, prompt: str = None, language: str = "en") -> Dict[str, str]:
        """Generate a summary of the transcript."""
        if not self.model:
            return {
                "summary": "AI summarization is currently unavailable. Please try again later.",
                "language": language
            }
        
        try:
            # Extract video information
            videos = self._extract_video_titles(transcript)
            video_info = "\n".join([
                f"Video {i+1}: {v['title'] or v['id']}"
                for i, v in enumerate(videos)
            ])

            system_prompt = f"""You are a helpful AI assistant that summarizes video transcripts.
            Language of transcript: {language}
            Task: {prompt}
            
            Videos to summarize:
            {video_info}
            
            Please provide a structured summary in the following format:

            # Overall Summary
            [A comprehensive overview combining insights from all videos. Focus on the main message, key arguments, and significant conclusions. Keep this section concise but informative.]

            ## Key Points
            [Organize key points by themes or topics. Each point should be substantive and meaningful.]

            ### Main Arguments
            - [Core arguments and central ideas]
            - [Supporting evidence and examples]
            - [Counter-arguments or alternative perspectives if present]

            ### Technical Details
            - [Specific methodologies or processes mentioned]
            - [Data points, statistics, or metrics]
            - [Technical terminology explanations]

            ### Practical Applications
            - [Real-world applications discussed]
            - [Implementation suggestions]
            - [Best practices or recommendations]

            ## Notable Quotes
            [Select the most impactful quotes that illustrate key points]
            > "Quote text here" - [Video Title, Timestamp]
            > "Another significant quote" - [Video Title, Timestamp]

            ## Cross-References
            - [Connections to other topics mentioned]
            - [Related resources or materials referenced]
            - [External links or citations provided]

            IMPORTANT FORMATTING AND CONTENT RULES:
            1. Use markdown headers (#, ##, ###) for section titles
            2. NO bold formatting (** **) in the content
            3. Keep quotes brief and impactful
            4. Include video title and timestamp for quotes
            5. Organize points by themes, not by video source
            6. Focus on substantive content, avoid superficial observations
            7. Include technical details when present
            8. Highlight practical applications
            9. Note any cross-references or external resources
            10. Keep language clear and professional

            STRUCTURE GUIDELINES:
            1. Overall Summary: Clear, concise overview (2-3 paragraphs)
            2. Key Points: Organized by themes, not source
            3. Notable Quotes: Only the most significant ones, with video titles
            4. Cross-References: Clear connections to related content

            Please ensure:
            1. Content is well-organized and logically structured
            2. Technical accuracy is maintained
            3. Practical value is emphasized
            4. Key insights are properly contextualized
            5. Language is clear and accessible
            6. Video titles are included with quotes and references
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
        Refine an existing summary based on user feedback.
        Maintains the same structured format while incorporating the feedback.
        """
        if not self.model:
            logger.error("Cannot refine summary: Gemini API not available")
            return "Summary refinement unavailable. Please set the GEMINI_API_KEY environment variable."
            
        try:
            system_prompt = """You are a helpful AI assistant that refines video summaries.
            Please maintain the existing structure while incorporating the feedback:

            1. Keep the same sections:
               - Overall Summary
               - Key Points (with subsections)
               - Notable Quotes (with video titles)
               - Cross-References

            2. Follow these rules:
               - Maintain clear organization
               - Keep technical accuracy
               - Ensure practical value
               - Preserve important context
               - Use clear language
               - Include video titles with quotes

            3. Do not:
               - Add new sections
               - Use bold formatting
               - Lose existing important information
               - Change the basic structure
            """

            prompt = f"{system_prompt}\n\nOriginal Summary:\n{summary}\n\nFeedback:\n{feedback}"
            
            response = await self.model.generate_content_async(
                contents=prompt,
                stream=False
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Error refining summary: {str(e)}")
            raise