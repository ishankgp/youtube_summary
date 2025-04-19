from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from transcript_available import get_transcript, TranscriptError, extract_video_id
from ai_handler import AIHandler
import logging
from enum import Enum
import os
import sys
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Get port from environment variable for Railway
port = int(os.environ.get("PORT", 8080))

# Configure CORS with more secure allow_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
        "https://youtube-summary-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Initialize AI Handler
ai_handler = AIHandler()

# Add a root route for health check
@app.get("/")
async def read_root():
    """Health check endpoint"""
    return {"status": "ok", "message": "YouTube Transcript Processor API is running"}

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
    transcript: str
    language: str
    duration: float
    translated: Optional[bool] = False
    original_language: Optional[str] = None
    is_generated: Optional[bool] = False

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
    """Fetch transcripts for the given YouTube URLs"""
    try:
        transcripts = {}
        failed_urls = []
        
        for url in request.urls:
            try:
                video_id = extract_video_id(url)
                language = request.preferred_language.value if request.preferred_language != "auto" else None
                transcript_text, detected_language = get_transcript(video_id, language)
                
                transcripts[url] = TranscriptData(
                    transcript=transcript_text,
                    language=detected_language,
                    duration=0.0,  # Duration will be added later if needed
                    translated=False,
                    original_language=None,
                    is_generated=True
                )
            except Exception as e:
                logger.error(f"Error processing URL {url}: {str(e)}")
                failed_urls.append({"url": url, "error": str(e)})
        
        return TranscriptResponse(
            transcripts=transcripts,
            status="success" if not failed_urls else "partial",
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
    uvicorn.run(app, host="0.0.0.0", port=port)