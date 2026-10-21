from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "ResearchNexus AI"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Vector DB
    CHROMA_URL: str = "./chroma_db"
    
    # Auth
    SECRET_KEY: str = "super_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # External APIs
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    GEMINI_FALLBACK_MODEL: str = "gemini-3.1-flash-lite"
    LOCAL_LLM_ENABLED: bool = False
    LOCAL_LLM_MODEL: str = "llama3.2"  # Recommend a small instruct model suitable for a laptop
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    AGRIS_API_KEY: str | None = None
    NASA_ADS_API_TOKEN: str | None = None
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
