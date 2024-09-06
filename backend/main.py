from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from models import Query, Response, init_models  # New import for model initialization
from config import Settings
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import torch
import weaviate
from ingest import ingest_document
import tempfile
import os

app = FastAPI()
settings = Settings()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Weaviate client
client = weaviate.Client(
    url=settings.weaviate_url,
    auth_client_secret=weaviate.AuthApiKey(api_key=settings.weaviate_api_key)
)
'''
# Initialize language model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(settings.model_name)
model = AutoModelForCausalLM.from_pretrained(settings.model_name, device_map="auto", torch_dtype=torch.float16)

# Initialize sentence transformer for embeddings
embedding_model = SentenceTransformer(settings.embedding_model)
'''
# Initialize models
tokenizer, model, embedding_model = init_models(settings)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        ingest_document(temp_file_path)
        os.unlink(temp_file_path)
        return {"message": "File uploaded and ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=Response)
async def query_portfolio(query: Query):
    try:
        query_embedding = embedding_model.encode(query.text).tolist()
        
        try:
            results = (
                client.query
                .get("Portfolio", ["text"])
                .with_near_vector({"vector": query_embedding})
                .with_limit(3)
                .do()
            )
        except weaviate.exceptions.WeaviateQueryException as e:
            raise HTTPException(status_code=500, detail=f"Weaviate query error: {str(e)}")
        
        
        context = "\n".join([obj['text'] for obj in results['data']['Get']['Portfolio']])
        
        prompt = f"""You are an AI assistant answering questions about the portfolio owner. Use the following context to answer the question. If you can't answer based on the context, say you don't have enough information.

Context: {context}

Question: {query.text}

Answer:"""

        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=150, temperature=0.7)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return Response(answer=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}