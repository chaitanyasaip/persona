from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import torch
from huggingface_hub import login

def init_models(settings):
    # Authenticate with Hugging Face
    login(token=settings.huggingface_token)
    tokenizer = AutoTokenizer.from_pretrained(settings.model_name)
    model = AutoModelForCausalLM.from_pretrained(settings.model_name)
    embedding_model = SentenceTransformer(settings.embedding_model)
    return tokenizer, model, embedding_model

class Query(BaseModel):
    text: str

class Response(BaseModel):
    answer: str