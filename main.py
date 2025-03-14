from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from transcript_available import get_transcript, TranscriptError
from ai_handler import AIHandler
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Handler
ai_handler = AIHandler()

class TranscriptLanguage(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    AUTO = "auto"

class TranscriptRequest(BaseModel):
    urls: List[str] = Field(..., description="List of YouTube video URLs to process")
    preferred_language: TranscriptLanguage = Field(
        default=TranscriptLanguage.AUTO,
        description="Preferred language for transcripts. Will fallback to available languages if not found."
    )

class TranscriptData(BaseModel):
    text: str
    language: str
    duration: float
    url: str

class TranscriptResponse(BaseModel):
    transcripts: Dict[str, TranscriptData]
    status: str
    failed_urls: Optional[List[Dict[str, str]]] = None

class SummarizeRequest(BaseModel):
    transcripts: Dict[str, str] = Field(..., description="Map of video URLs to their transcripts")
    prompt: str = Field(
        default="Please provide a comprehensive summary of the video content",
        description="Custom prompt for the summary generation"
    )
    language: TranscriptLanguage = Field(
        default=TranscriptLanguage.ENGLISH,
        description="Language to generate the summary in"
    )

class SummarizeResponse(BaseModel):
    summary: str
    status: str
    language: str

class RefineRequest(BaseModel):
    summary: str = Field(..., description="Original summary to refine")
    feedback: str = Field(..., description="User feedback for refinement")

@app.post("/api/transcripts", response_model=TranscriptResponse)
async def fetch_transcripts(request: TranscriptRequest):
    """
    Fetch transcripts for multiple YouTube videos.
    Handles language preferences and provides detailed error information.
    """
    try:
        all_transcripts = {}
        failed_urls = []
        
        for url in request.urls:
            try:
                logger.info(f"Fetching transcript for URL: {url}")
                transcript_data = get_transcript(
                    url, 
                    preferred_language=request.preferred_language
                )
                
                all_transcripts[url] = TranscriptData(
                    text=transcript_data["text"],
                    language=transcript_data["language"],
                    duration=transcript_data["duration"],
                    url=url
                )
                
                logger.info(f"Successfully fetched transcript for URL: {url}")
                
            except TranscriptError as e:
                error_msg = f"Error processing {url}: {str(e)}"
                logger.error(error_msg)
                failed_urls.append({"url": url, "error": str(e)})

        if not all_transcripts:
            if failed_urls:
                error_details = "\n".join([f"{item['url']}: {item['error']}" for item in failed_urls])
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to process all URLs:\n{error_details}"
                )
            raise HTTPException(
                status_code=400,
                detail="No valid transcripts found"
            )

        return TranscriptResponse(
            transcripts=all_transcripts,
            status="success",
            failed_urls=failed_urls if failed_urls else None
        )

    except Exception as e:
        logger.error(f"Error in fetch_transcripts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize_transcripts(request: SummarizeRequest):
    """
    Generate a structured summary from multiple video transcripts.
    Follows our design system for consistent formatting and organization.
    """
    try:
        # Combine all transcripts with video context
        combined_transcript = ""
        for url, transcript in request.transcripts.items():
            video_id = url.split("v=")[-1] if "v=" in url else url
            combined_transcript += f"\nVideo ({video_id}):\n{transcript}\n"

        # Generate summary using AI
        logger.info("Generating structured summary")
        summary_result = await ai_handler.generate_summary(
            transcript=combined_transcript,
            prompt=request.prompt,
            language=request.language
        )
        logger.info("Summary generated successfully")

        return SummarizeResponse(
            summary=summary_result["summary"],
            status="success",
            language=summary_result["language"]
        )

    except Exception as e:
        logger.error(f"Error in summarize_transcripts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {str(e)}"
        )

@app.post("/api/refine", response_model=SummarizeResponse)
async def refine_summary(request: RefineRequest):
    """
    Refine an existing summary based on user feedback.
    Maintains the structured format while incorporating improvements.
    """
    try:
        refined_summary = await ai_handler.refine_summary(
            summary=request.summary,
            feedback=request.feedback
        )
        
        return SummarizeResponse(
            summary=refined_summary,
            status="success",
            language="en"  # Refinement maintains the original language
        )
        
    except Exception as e:
        logger.error(f"Error in refine_summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refine summary: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)