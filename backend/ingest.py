#print("Starting ingest.py")
import weaviate
from weaviate.auth import AuthApiKey
from sentence_transformers import SentenceTransformer
from config import Settings
import nltk
from nltk.tokenize import sent_tokenize
from huggingface_hub import login
'''
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
'''
import os
import argparse

def download_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt resource...")
        nltk.download('punkt')
    
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("Downloading NLTK punkt_tab resource...")
        nltk.download('punkt_tab')

# Call this function before using NLTK
download_nltk_resources()

settings = Settings()

print(f"Attempting to connect to Weaviate at: {settings.weaviate_url}")
print(f"API Key present: {'Yes' if settings.weaviate_api_key else 'No'}")

auth_config = AuthApiKey(api_key=settings.weaviate_api_key) if settings.weaviate_api_key else None
client = weaviate.Client(
    url=settings.weaviate_url,
    auth_client_secret=auth_config
)
# Test the connection
try:
    print(client.get_meta())
except Exception as e:
    print(f"Error connecting to Weaviate: {e}")

client = weaviate.Client(
    url=settings.weaviate_url,
    auth_client_secret=weaviate.AuthApiKey(api_key=settings.weaviate_api_key) if settings.weaviate_api_key else None
)

embedding_model = SentenceTransformer(settings.embedding_model)

def ensure_schema():
    class_obj = {
        "class": "Portfolio",
        "vectorizer": "none",
        "properties": [
            {
                "name": "text",
                "dataType": ["text"],
                "description": "The content of the portfolio chunk",
            },
            {
                "name": "source",
                "dataType": ["string"],
                "description": "The source document of this chunk",
            }
        ],
    }

    try:
        class_exists = client.schema.exists("Portfolio")
        if not class_exists:
            client.schema.create_class(class_obj)
            print("Created 'Portfolio' class in Weaviate")
        else:
            print("'Portfolio' class already exists in Weaviate")
    except Exception as e:
        print(f"Error working with Weaviate schema: {e}")

def split_into_chunks(text, max_chunk_size=1000):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def ingest_document(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    chunks = split_into_chunks(content)
    
    ensure_schema()  # Ensure the schema exists before ingesting

    for chunk in chunks:
        embedding = embedding_model.encode(chunk).tolist()
        try:
            client.data_object.create(
                "Portfolio",
                {
                    "text": chunk,
                },
                vector=embedding
            )
        except Exception as e:
            print(f"Error ingesting chunk: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a document into Weaviate.")
    parser.add_argument("file_path", help="Path to the resume or document to ingest")
    args = parser.parse_args()

    try:
        ingest_document(args.file_path)
        print(f"Successfully ingested {args.file_path}")
    except Exception as e:
        print(f"Error: {e}")