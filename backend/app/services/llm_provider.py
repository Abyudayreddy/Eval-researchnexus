import re
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from google import genai
from app.core.config import settings

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, query: str, evidence_context: str, system_instruction: str = None) -> dict:
        pass

    @abstractmethod
    def generate_search_query(self, query: str) -> str:
        pass

class GeminiProvider(LLMProvider):
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.GEMINI_MODEL

    def generate(self, query: str, evidence_context: str, system_instruction: str = None) -> dict:
        if not settings.GEMINI_API_KEY:
            return {
                "text": "ERROR: GEMINI_API_KEY is not configured.",
                "provider": "gemini",
                "model": self.model_name,
                "generation_status": "generation_failed"
            }
            
        if system_instruction:
            prompt = (
                f"{system_instruction}\n\n"
                f"Evidence Context:\n{evidence_context}\n\n"
                f"Query: {query}"
            )
        else:
            prompt = (
                f"Answer the research query based strictly on the following evidence. "
                f"If the evidence does not contain the answer, state that you cannot answer based on the retrieved documents. "
                f"Cite your sources using the [index] numbers provided.\n\n"
                f"Evidence:\n{evidence_context}\n\nQuery: {query}"
            )
        
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return {
                "text": response.text or "",
                "provider": "gemini",
                "model": self.model_name,
                "generation_status": "success"
            }
        except Exception as e:
            error_str = str(e).lower()
            if "429" in error_str or "quota" in error_str or "exhausted" in error_str or "too many requests" in error_str:
                print(f"Gemini API Error: QUOTA_EXCEEDED ({self.model_name}) - {e}")
                return {
                    "text": "Research evidence was retrieved successfully, but the AI generation quota is temporarily unavailable. Please try again shortly.",
                    "provider": "gemini",
                    "model": self.model_name,
                    "generation_status": "quota_exceeded"
                }
            else:
                print(f"Gemini API Error: GENERATION_FAILED ({self.model_name}) - {e}")
                return {
                    "text": "Research evidence was retrieved, but the answer could not be generated. Please try again.",
                    "provider": "gemini",
                    "model": self.model_name,
                    "generation_status": "generation_failed"
                }

    def generate_search_query(self, query: str) -> str:
        # Use deterministic processing to save Gemini API calls
        return LLMProviderManager.deterministic_query_extractor(query)


class LocalOllamaProvider(LLMProvider):
    def generate(self, query: str, evidence_context: str, system_instruction: str = None) -> dict:
        pass # We use async in LLMProviderManager instead
        
    def generate_search_query(self, query: str) -> str:
        return LLMProviderManager.deterministic_query_extractor(query)

class LLMProviderManager:
    @staticmethod
    async def generate(query: str, evidence_context: str, system_instruction: str = None) -> dict:
        if settings.LLM_PROVIDER == "local":
            return await LLMProviderManager._generate_local(query, evidence_context, system_instruction)
            
        gemini_primary = GeminiProvider(model_name=settings.GEMINI_MODEL)
        result = gemini_primary.generate(query, evidence_context, system_instruction)
        
        # 1st Fallback: Gemini 3.1 Flash-Lite
        if result["generation_status"] == "quota_exceeded" and getattr(settings, "GEMINI_FALLBACK_MODEL", None):
            print(f"Gemini Primary ({settings.GEMINI_MODEL}) Quota Exceeded. Falling back to Secondary ({settings.GEMINI_FALLBACK_MODEL}).")
            gemini_secondary = GeminiProvider(model_name=settings.GEMINI_FALLBACK_MODEL)
            result = gemini_secondary.generate(query, evidence_context, system_instruction)
            
        # 2nd Fallback: Local Ollama
        if result["generation_status"] == "quota_exceeded" and settings.LOCAL_LLM_ENABLED:
            print("Gemini Secondary Quota Exceeded. Falling back to local LLM.")
            return await LLMProviderManager._generate_local(query, evidence_context, system_instruction)
            
        return result
        
    @staticmethod
    async def _generate_local(query: str, evidence_context: str, system_instruction: str = None) -> dict:
        prefix = f"{system_instruction}\n\n" if system_instruction else "Answer ONLY using the supplied research evidence.\nDo not use outside knowledge.\n"
        prompt = (
            f"{prefix}"
            f"Evidence:\n{evidence_context}\n\nQuery: {query}"
        )
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": settings.LOCAL_LLM_MODEL,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=120.0
                )
                response.raise_for_status()
                data = response.json()
                
                return {
                    "text": data.get("response", ""),
                    "provider": "local",
                    "model": settings.LOCAL_LLM_MODEL,
                    "generation_status": "fallback_success"
                }
        except Exception as e:
            print(f"Local Ollama API Error: {e}")
            return {
                "text": "Research evidence was retrieved successfully, but AI generation is temporarily unavailable.",
                "provider": "local",
                "model": settings.LOCAL_LLM_MODEL,
                "generation_status": "quota_exceeded"
            }

    @staticmethod
    def generate_search_query(query: str) -> str:
        if settings.LLM_PROVIDER == "local":
            return LocalOllamaProvider().generate_search_query(query)
        return GeminiProvider().generate_search_query(query)

    @staticmethod
    def deterministic_query_extractor(query: str) -> str:
        q = query.lower().replace('?', '').strip()
        q = re.sub(r'\bbeing used for\b', 'use', q)
        q = re.sub(r'\bused for\b', 'use', q)
        
        fillers = [
            r'\bwhat are the\b', r'\bwhat are\b', r'\bwhat is\b',
            r'\bhow is\b', r'\bhow do\b', r'\bhow does\b',
            r'\bcan you\b', r'\bplease\b', r'\btell me\b',
            r'\bfind\b', r'\bsearch for\b', r'\bi need\b',
            r'\bshow me\b', r'\bcould you\b', r'\bwould you\b',
            r'\bthe\b', r'\ba\b', r'\ban\b', r'\bof\b', r'\bin\b', r'\bfor\b'
        ]
        
        for f in fillers:
            q = re.sub(f, '', q)
                
        q = re.sub(r'\s+', ' ', q).strip()
        if not q:
            return query.strip().replace('?', '')
        return q
