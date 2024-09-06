from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from huggingface_hub import login
from typing import Optional

# Get the directory of the current file (config.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_dir, '.env')
#os.environ["HF_TOKEN"] = HUGGINGFACE_TOKEN

class Settings(BaseSettings):
    #weaviate_url: str = "http://host.docker.internal:8080"
    weaviate_url: str = "http://weaviate:8080"
    weaviate_api_key: Optional[str] = None
    #weaviate_api_key: str | None = None
    frontend_url: str = "http://localhost:3000"
    embedding_model: str = "all-MiniLM-L6-v2"
    #model_name: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    model_name: str = "distilgpt2"  # Using a smaller model for faster setup
    huggingface_token: str = ""
    #model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    class Config:
        env_file = ".env"
        protected_namespaces = ('settings_',)

# Debug: Print current working directory and check if .env file exists
print(f"Current working directory: {os.getcwd()}")
print(f"Looking for .env file at: {env_file_path}")
print(f".env file exists: {os.path.exists('.env')}")

settings = Settings()

# Debug: Print loaded settings
print(f"Loaded settings: {settings.dict()}")