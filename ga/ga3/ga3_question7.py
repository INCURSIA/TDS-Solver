from fastapi import HTTPException
from pydantic import BaseModel
from typing import List
import requests
import numpy as np
import os

# Define a Pydantic model for the request body
class SimilarityRequest(BaseModel):
    docs: List[str]
    query: str

def cosine_similarity(a, b):
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return 0.0 if norm_a == 0 or norm_b == 0 else np.dot(a, b) / (norm_a * norm_b)

def run_question_server7():
    """
    Handles the similarity logic directly when called from main.py.
    """
    async def similarity_endpoint(payload: SimilarityRequest):
        try:
            # Load the AIPROXY_TOKEN from environment variables
            AIPROXY_TOKEN = "AIPROXY_TOKEN"
            if not AIPROXY_TOKEN:
                raise ValueError("AIPROXY_TOKEN environment variable not set.")

            docs = payload.docs
            query = payload.query

            if not docs or not query:
                raise HTTPException(status_code=400, detail="Missing 'docs' or 'query' in request body")

            # Combine query and docs for the embeddings request
            input_texts = [query] + docs

            # Make a request to the AI Proxy service
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {AIPROXY_TOKEN}"
            }
            data = {"model": "text-embedding-3-small", "input": input_texts}
            embeddings_response = requests.post(
                "https://aiproxy.sanand.workers.dev/openai/v1/embeddings",
                headers=headers,
                json=data
            )

            embeddings_response.raise_for_status()
            embeddings_data = embeddings_response.json()

            # Extract embeddings
            query_embedding = embeddings_data['data'][0]['embedding']
            doc_embeddings = [emb['embedding'] for emb in embeddings_data['data'][1:]]

            # Calculate cosine similarities
            similarities = [
                (i, cosine_similarity(query_embedding, doc_embeddings[i]), docs[i])
                for i in range(len(docs))
            ]
            ranked_docs = sorted(similarities, key=lambda x: x[1], reverse=True)
            top_matches = [doc for _, _, doc in ranked_docs[:min(3, len(ranked_docs))]]

            return {"matches": top_matches}

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with AI Proxy: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    # Return the endpoint function to be mounted dynamically in main.py
    return similarity_endpoint
