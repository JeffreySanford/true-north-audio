"""
FastAPI endpoints for the music chat assistant.
This module provides REST API endpoints that expose the MusicAssistant functionality.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import sys
import os

# Add parent directory to path to import music_assistant
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from chat.music_assistant import MusicAssistant

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Music Chat API", version="1.0.0")

# Initialize Music Assistant
assistant = MusicAssistant()


# Request/Response Models
class ChatMessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    include_suggestions: bool = True


class GenerateLyricsRequest(BaseModel):
    theme: str
    style: str = "country"
    session_id: Optional[str] = None


class GenerateFromChatRequest(BaseModel):
    session_id: str
    override_params: Optional[Dict[str, Any]] = None


# API Endpoints
@app.post("/chat/message")
async def send_message(request: ChatMessageRequest):
    """
    Send a message to the music assistant and get a conversational response.
    
    Returns:
        - response: AI assistant's response text
        - parameters: Extracted music parameters
        - ready_to_generate: Boolean indicating if enough info is collected
        - session_id: Session identifier for conversation continuity
    """
    try:
        logger.info(f"Chat message received: {request.message[:50]}...")
        
        result = assistant.chat(
            user_message=request.message,
            session_id=request.session_id
        )
        
        return {
            "success": True,
            **result
        }
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )


@app.post("/chat/generate-lyrics")
async def generate_lyrics(request: GenerateLyricsRequest):
    """
    Generate song lyrics based on a theme using LLM.
    
    Returns:
        - lyrics: Generated song lyrics
        - theme: The theme used
        - style: The style used
    """
    try:
        logger.info(f"Generating lyrics: theme={request.theme}, style={request.style}")
        
        lyrics = assistant.generate_lyrics(
            theme=request.theme,
            style=request.style
        )
        
        return {
            "success": True,
            "lyrics": lyrics,
            "theme": request.theme,
            "style": request.style
        }
    except Exception as e:
        logger.error(f"Lyrics generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lyrics generation failed: {str(e)}"
        )


@app.post("/chat/generate")
async def generate_from_conversation(request: GenerateFromChatRequest):
    """
    Generate music based on a conversation session.
    
    Returns:
        - music_file: Path to generated music file
        - parameters: Final parameters used for generation
        - engine: Which engine was used
    """
    try:
        logger.info(f"Generating from session: {request.session_id}")
        
        result = assistant.generate_from_conversation(
            session_id=request.session_id,
            override_params=request.override_params
        )
        
        return {
            "success": True,
            **result
        }
    except Exception as e:
        logger.error(f"Generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Music generation failed: {str(e)}"
        )


@app.get("/chat/session/{session_id}")
async def get_session_summary(session_id: str):
    """
    Get summary of a conversation session.
    
    Returns:
        - conversation_history: List of messages
        - parameters: Current extracted parameters
        - ready_to_generate: Whether ready to generate
    """
    try:
        if session_id not in assistant.sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {session_id} not found"
            )
        
        session = assistant.sessions[session_id]
        
        return {
            "success": True,
            "session_id": session_id,
            "conversation_history": session["conversation_history"],
            "parameters": session["parameters"],
            "ready_to_generate": assistant._is_ready_to_generate(session["parameters"])
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session retrieval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve session: {str(e)}"
        )


@app.get("/chat/health")
async def health_check():
    """
    Check if the chat service and Ollama are available.
    
    Returns:
        - available: Boolean indicating service health
        - ollama_available: Boolean indicating Ollama connectivity
        - model: The LLM model being used
    """
    try:
        # Test Ollama connection
        import requests
        
        ollama_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        try:
            response = requests.get(f"{ollama_url}/api/tags", timeout=5)
            ollama_available = response.status_code == 200
        except Exception:
            ollama_available = False
        
        return {
            "available": True,
            "ollama_available": ollama_available,
            "model": assistant.model,
            "ollama_url": ollama_url,
            "active_sessions": len(assistant.sessions)
        }
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "available": False,
            "error": str(e)
        }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Music Chat API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat/message",
            "lyrics": "/chat/generate-lyrics",
            "generate": "/chat/generate",
            "session": "/chat/session/{session_id}",
            "health": "/chat/health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Music Chat API server...")
    logger.info(f"Ollama URL: {os.getenv('OLLAMA_API_URL', 'http://localhost:11434')}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
