from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from transcript_available import get_transcript, TranscriptError
from ai_handler import AIHandler
import logging

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

class TranscriptRequest(BaseModel):
    urls: List[str]

class TranscriptResponse(BaseModel):
    transcripts: Dict[str, dict]
    status: str

class SummarizeRequest(BaseModel):
    transcripts: Dict[str, str]
    prompt: str

class SummarizeResponse(BaseModel):
    summary: str
    status: str

@app.post("/api/transcripts")
async def fetch_transcripts(request: TranscriptRequest):
    try:
        # Dictionary to store transcripts for each video
        all_transcripts = {}
        failed_urls = []
        
        # Fetch transcripts for all videos
        for url in request.urls:
            try:
                logger.info(f"Fetching transcript for URL: {url}")
                transcript_data = get_transcript(url)
                all_transcripts[url] = transcript_data
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
            status="success"
        )

    except Exception as e:
        logger.error(f"Error in fetch_transcripts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize")
async def summarize_transcripts(request: SummarizeRequest):
    try:
        # Combine all transcripts with video context
        combined_transcript = ""
        for url, transcript in request.transcripts.items():
            combined_transcript += f"\nVideo: {url}\n{transcript}\n"

        # Generate summary using AI
        logger.info("Generating summary")
        summary_result = await ai_handler.generate_summary(
            transcript=combined_transcript,
            prompt=request.prompt
        )
        logger.info("Summary generated successfully")

        return SummarizeResponse(
            summary=summary_result["summary"],
            status="success"
        )

    except Exception as e:
        logger.error(f"Error in summarize_transcripts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refine")
async def refine_summary(request: dict):
    try:
        refined_summary = await ai_handler.refine_summary(
            summary=request["summary"],
            feedback=request["feedback"]
        )
        return {"summary": refined_summary, "status": "success"}
    except Exception as e:
        logger.error(f"Error in refine_summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)