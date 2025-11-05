"""
LLM Chat Interface for Music Generation

This module provides an intelligent chat interface that helps users refine their
music generation ideas through conversation. The LLM analyzes user intent and
automatically configures optimal generation parameters.

Features:
- Natural language music idea processing
- Intelligent parameter extraction from conversation
- Genre, mood, and style suggestions
- Lyrics generation from themes
- Multi-turn conversation for refinement
- Context-aware parameter optimization

Usage:
    from ai_music_gen.chat.music_assistant import MusicAssistant
    
    assistant = MusicAssistant()
    
    # User conversation
    response = assistant.chat("I want a patriotic song about voting")
    # Returns: conversation + suggested parameters
    
    # Generate with refined parameters
    result = assistant.generate_from_conversation(session_id)
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class MusicAssistant:
    """
    Intelligent music generation assistant using LLM.
    Converts natural language ideas into optimized generation parameters.
    """
    
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        self.ollama_host = ollama_host
        self.model = os.getenv("OLLAMA_MODEL", "llama2")
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"MusicAssistant initialized with model: {self.model}")
    
    def chat(
        self,
        user_message: str,
        session_id: Optional[str] = None,
        include_suggestions: bool = True
    ) -> Dict[str, Any]:
        """
        Process user message and return conversation response with suggestions.
        
        Args:
            user_message: User's natural language input
            session_id: Conversation session ID (creates new if None)
            include_suggestions: Whether to include parameter suggestions
            
        Returns:
            Dict containing:
                - response: LLM's conversational response
                - parameters: Extracted/suggested music parameters
                - session_id: Session identifier
                - conversation_history: Full chat history
        """
        # Create or retrieve session
        if session_id is None:
            session_id = self._create_session()
        
        session = self.sessions.get(session_id)
        if not session:
            session = self._create_session()
        
        # Add user message to history
        session["conversation"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Build system prompt for music generation
        system_prompt = self._build_system_prompt()
        
        # Build conversation context
        context = self._build_context(session)
        
        # Call Ollama LLM
        try:
            llm_response = self._call_ollama(
                system_prompt=system_prompt,
                user_message=user_message,
                context=context
            )
            
            # Add assistant response to history
            session["conversation"].append({
                "role": "assistant",
                "content": llm_response["response"],
                "timestamp": datetime.now().isoformat()
            })
            
            # Extract parameters if requested
            parameters = {}
            if include_suggestions:
                parameters = self._extract_parameters(
                    user_message,
                    llm_response["response"],
                    session
                )
                session["parameters"] = {**session.get("parameters", {}), **parameters}
            
            return {
                "success": True,
                "response": llm_response["response"],
                "parameters": parameters,
                "session_id": session_id,
                "conversation_history": session["conversation"],
                "ready_to_generate": self._is_ready_to_generate(session)
            }
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for music generation assistant"""
        return """You are an expert music generation assistant. Your role is to help users 
create amazing music by understanding their ideas and suggesting optimal parameters.

Your capabilities:
1. Understand musical concepts (genre, mood, tempo, instrumentation)
2. Extract key themes and emotions from user descriptions
3. Suggest appropriate vocal styles and arrangements
4. Generate lyrics when requested
5. Recommend optimal engine (Suno, Udio, or MusicGen) based on needs

When users describe their music idea:
- Ask clarifying questions to refine the concept
- Suggest genres, moods, and tempos
- Offer lyrical themes or write lyrics if requested
- Recommend voice styles (male/female, country/blues/rock, etc.)
- Consider privacy needs (cloud vs local generation)

Be creative, enthusiastic, and helpful. Guide users to create their best music."""
    
    def _build_context(self, session: Dict[str, Any]) -> str:
        """Build conversation context from session history"""
        context_parts = []
        
        # Add previous conversation
        for msg in session["conversation"][-5:]:  # Last 5 messages
            role = msg["role"].capitalize()
            content = msg["content"]
            context_parts.append(f"{role}: {content}")
        
        # Add current parameters if any
        if session.get("parameters"):
            params = session["parameters"]
            context_parts.append(f"\nCurrent Parameters:")
            for key, value in params.items():
                context_parts.append(f"  - {key}: {value}")
        
        return "\n".join(context_parts)
    
    def _call_ollama(
        self,
        system_prompt: str,
        user_message: str,
        context: str
    ) -> Dict[str, Any]:
        """Call Ollama API for chat completion"""
        url = f"{self.ollama_host}/api/generate"
        
        # Combine system prompt, context, and user message
        full_prompt = f"{system_prompt}\n\n{context}\n\nUser: {user_message}\n\nAssistant:"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return {
            "response": result.get("response", "").strip()
        }
    
    def _extract_parameters(
        self,
        user_message: str,
        llm_response: str,
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract music generation parameters from conversation.
        Uses keyword matching and LLM response analysis.
        """
        parameters = {}
        combined_text = f"{user_message} {llm_response}".lower()
        
        # Genre extraction
        genre_keywords = {
            "americana": ["americana", "folk", "bluegrass", "country folk"],
            "blues": ["blues", "rhythm and blues", "r&b"],
            "rock": ["rock", "rock and roll", "classic rock"],
            "country": ["country", "nashville", "honky tonk"],
            "jazz": ["jazz", "swing", "bebop"],
            "electronic": ["electronic", "edm", "techno", "house"],
            "hip-hop": ["hip hop", "rap", "hip-hop"],
            "classical": ["classical", "orchestral", "symphony"]
        }
        
        for genre, keywords in genre_keywords.items():
            if any(kw in combined_text for kw in keywords):
                parameters["genre"] = genre
                break
        
        # Mood extraction
        mood_keywords = {
            "uplifting": ["uplifting", "upbeat", "happy", "joyful", "cheerful"],
            "melancholic": ["sad", "melancholic", "sorrowful", "mournful"],
            "energetic": ["energetic", "powerful", "driving", "intense"],
            "calm": ["calm", "peaceful", "relaxing", "soothing"],
            "patriotic": ["patriotic", "america", "freedom", "liberty", "voting"]
        }
        
        for mood, keywords in mood_keywords.items():
            if any(kw in combined_text for kw in keywords):
                parameters["mood"] = mood
                break
        
        # Tempo extraction
        if any(word in combined_text for word in ["fast", "upbeat", "energetic"]):
            parameters["tempo"] = 120
        elif any(word in combined_text for word in ["slow", "ballad", "relaxed"]):
            parameters["tempo"] = 70
        else:
            parameters["tempo"] = 90  # Default medium tempo
        
        # Vocal style extraction
        if "male" in combined_text and "voice" in combined_text:
            parameters["vocal_style"] = "male"
        elif "female" in combined_text and "voice" in combined_text:
            parameters["vocal_style"] = "female"
        
        # Duration extraction (look for numbers + seconds/minutes)
        import re
        duration_match = re.search(r'(\d+)\s*(second|minute|min|sec)', combined_text)
        if duration_match:
            value = int(duration_match.group(1))
            unit = duration_match.group(2)
            if unit.startswith("min"):
                parameters["duration"] = value * 60
            else:
                parameters["duration"] = value
        else:
            parameters["duration"] = 120  # Default 2 minutes
        
        # Instrumental detection
        if any(word in combined_text for word in ["instrumental", "no vocals", "no singing"]):
            parameters["instrumental"] = True
        
        # Engine suggestion based on privacy/quality
        if any(word in combined_text for word in ["private", "local", "offline"]):
            parameters["suggested_engine"] = "musicgen"
        elif any(word in combined_text for word in ["best quality", "professional", "high quality"]):
            parameters["suggested_engine"] = "suno"  # or udio
        
        return parameters
    
    def _is_ready_to_generate(self, session: Dict[str, Any]) -> bool:
        """
        Determine if session has enough information to generate music.
        """
        params = session.get("parameters", {})
        
        # Minimum requirements: genre or mood, and some content
        has_musical_direction = "genre" in params or "mood" in params
        has_conversation = len(session.get("conversation", [])) > 0
        
        return has_musical_direction and has_conversation
    
    def _create_session(self) -> str:
        """Create new conversation session"""
        import uuid
        session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "conversation": [],
            "parameters": {}
        }
        
        return session_id
    
    def generate_from_conversation(
        self,
        session_id: str,
        override_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate music using parameters extracted from conversation.
        
        Args:
            session_id: Conversation session ID
            override_params: Optional parameters to override extracted ones
            
        Returns:
            Generation result from selected engine
        """
        session = self.sessions.get(session_id)
        if not session:
            return {
                "success": False,
                "error": "Session not found"
            }
        
        # Build generation parameters
        params = {**session.get("parameters", {})}
        if override_params:
            params.update(override_params)
        
        # Generate prompt from conversation
        if "prompt" not in params:
            params["prompt"] = self._generate_prompt_from_conversation(session)
        
        # Select engine
        engine = params.pop("suggested_engine", "musicgen")
        
        logger.info(f"Generating music with {engine} engine")
        logger.info(f"Parameters: {json.dumps(params, indent=2)}")
        
        # Import and call appropriate engine
        try:
            if engine == "suno":
                from engines.suno import generate_music
            elif engine == "udio":
                from engines.udio import generate_music
            else:  # musicgen
                from engines.musicgen_local import generate_music
            
            result = generate_music(**params)
            
            # Add to session history
            session["generations"] = session.get("generations", [])
            session["generations"].append({
                "timestamp": datetime.now().isoformat(),
                "engine": engine,
                "parameters": params,
                "result": result
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_prompt_from_conversation(self, session: Dict[str, Any]) -> str:
        """Generate music generation prompt from conversation history"""
        conversation = session.get("conversation", [])
        params = session.get("parameters", {})
        
        # Extract key themes from conversation
        themes = []
        for msg in conversation:
            if msg["role"] == "user":
                content = msg["content"].lower()
                # Extract key phrases (simplified)
                if len(content) > 20:
                    themes.append(content[:100])
        
        # Build prompt
        prompt_parts = []
        
        if params.get("genre"):
            prompt_parts.append(f"{params['genre']} style")
        
        if params.get("mood"):
            prompt_parts.append(f"with {params['mood']} mood")
        
        if themes:
            prompt_parts.append(f"about {themes[0]}")
        
        if params.get("vocal_style"):
            prompt_parts.append(f"featuring {params['vocal_style']} vocals")
        
        prompt = " ".join(prompt_parts)
        
        return prompt if prompt else "Original musical composition"
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of conversation session"""
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}
        
        return {
            "session_id": session_id,
            "created_at": session["created_at"],
            "message_count": len(session["conversation"]),
            "parameters": session.get("parameters", {}),
            "ready_to_generate": self._is_ready_to_generate(session),
            "generation_count": len(session.get("generations", []))
        }
    
    def generate_lyrics(
        self,
        theme: str,
        style: str = "country",
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate lyrics based on theme using LLM.
        
        Args:
            theme: Lyrical theme or topic
            style: Musical style for lyrics
            session_id: Optional session to add lyrics to
            
        Returns:
            Dict with generated lyrics
        """
        prompt = f"""Write lyrics for a {style} song about {theme}.

Structure:
- Verse 1 (4 lines)
- Chorus (4 lines)
- Verse 2 (4 lines)
- Chorus (repeat)
- Bridge (4 lines)
- Chorus (repeat)

Make them meaningful, emotional, and authentic to the {style} genre."""
        
        try:
            response = self._call_ollama(
                system_prompt="You are a talented songwriter.",
                user_message=prompt,
                context=""
            )
            
            lyrics = response["response"]
            
            # Add to session if provided
            if session_id and session_id in self.sessions:
                self.sessions[session_id]["parameters"]["lyrics"] = lyrics
            
            return {
                "success": True,
                "lyrics": lyrics,
                "theme": theme,
                "style": style
            }
            
        except Exception as e:
            logger.error(f"Lyrics generation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


def test_music_assistant():
    """Test the music assistant chat interface"""
    print("=" * 60)
    print("Music Assistant Test")
    print("=" * 60)
    
    assistant = MusicAssistant()
    
    # Test conversation
    print("\n1. User: I want to create a patriotic americana song about voting")
    response1 = assistant.chat(
        "I want to create a patriotic americana song about voting"
    )
    
    print(f"\nAssistant: {response1['response']}")
    print(f"\nExtracted Parameters: {json.dumps(response1['parameters'], indent=2)}")
    print(f"Ready to generate: {response1['ready_to_generate']}")
    
    session_id = response1['session_id']
    
    # Follow-up
    print("\n\n2. User: Make it with a male country voice, about 2 minutes")
    response2 = assistant.chat(
        "Make it with a male country voice, about 2 minutes",
        session_id=session_id
    )
    
    print(f"\nAssistant: {response2['response']}")
    print(f"\nUpdated Parameters: {json.dumps(response2['parameters'], indent=2)}")
    
    # Generate lyrics
    print("\n\n3. Generating lyrics...")
    lyrics_result = assistant.generate_lyrics(
        theme="voting and American freedom",
        style="americana country",
        session_id=session_id
    )
    
    if lyrics_result["success"]:
        print(f"\nGenerated Lyrics:\n{lyrics_result['lyrics'][:200]}...")
    
    # Session summary
    print("\n\n4. Session Summary:")
    summary = assistant.get_session_summary(session_id)
    print(json.dumps(summary, indent=2))
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    test_music_assistant()
