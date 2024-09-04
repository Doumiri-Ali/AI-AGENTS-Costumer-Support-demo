import os
import numpy as np
import time
import re
import json
import requests
from langchain_groq import ChatGroq
#from langchain_anthropic import ChatAnthropic



os.environ["GROQ_API_KEY"] = "GROQ_API_KEY_HERE"
#os.environ["ANTHROPIC_API_KEY"] = "ANTHROPIC_API_KEY_HERE" if using ANTHROPIC claude model
#os.environ["TAVILY_API_KEY"] = "TAVILY_API_KEY_HERE" for using web search tool



# Define paths
policy_rules_path = 'Rental-Car-Business-Demo/data/company_rules.md'



# File paths
CARS_FILE_PATH = 'Rental-Car-Business-Demo/data/cars.csv'
BOOKINGS_FILE_PATH = 'Rental-Car-Business-Demo/data/bookings.csv'
USERS_FILE_PATH = 'Rental-Car-Business-Demo/data/users.csv'
# Retrieve the path to the temporary file from the environment variable
user_id_file_path = os.getenv('USER_ID_FILE')

#llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.7)
llm = ChatGroq(model="llama3-groq-70b-8192-tool-use-preview", temperature=0.7, max_tokens=None, timeout=None)



def load_policy_rules(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


class VectorStoreRetriever:
    def __init__(self, docs: list, vectors: list):
        self._arr = np.array(vectors)
        self._docs = docs
        self.api_url = 'https://api-inference.huggingface.co/models/jinaai/jina-embeddings-v2-base-en'
        self.headers = {'Authorization': f'Bearer $huggingface_api_here$'}  # Replace with your API key

    def get_embedding(self, text):
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": text[:2000]})

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

        result = response.json()

        if isinstance(result, list) and isinstance(result[0], float):
            return result
        else:
            raise KeyError(f"Unexpected response structure: {result}")

    @classmethod
    def from_docs(cls, docs, vectors_path='vectors.json'):
        # Check if vectors file exists
        if os.path.exists(vectors_path):
            print("Loading vectors from file...")
            try:
                with open(vectors_path, 'r') as f:
                    vectors = json.load(f)
                if not vectors:
                    raise ValueError("The vectors file is empty.")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error loading vectors from file: {e}")
                print("Generating vectors...")
                vectors = cls.generate_vectors(docs, vectors_path)
        else:
            print("Vectors file does not exist. Generating vectors...")
            vectors = cls.generate_vectors(docs, vectors_path)

        return cls(docs, vectors)

    @staticmethod
    def generate_vectors(docs, vectors_path):
        vectors = []
        instance = VectorStoreRetriever(docs, vectors)
        for doc in docs:
            time.sleep(1)  # Adjust sleep time as necessary
            embedding = instance.get_embedding(doc["page_content"][:2000])
            vectors.append(embedding)

        # Save the vectors to a file
        with open(vectors_path, 'w') as f:
            json.dump(vectors, f)

        return vectors

    def query(self, query: str, k: int = 5) -> list[dict]:
        time.sleep(1)  # Adjust sleep time as necessary
        query_embedding = self.get_embedding(query[:2000])

        scores = np.dot(self._arr, query_embedding)
        top_k_idx = np.argpartition(scores, -k)[-k:]
        top_k_idx_sorted = top_k_idx[np.argsort(-scores[top_k_idx])]
        return [
            {**self._docs[idx], "similarity": scores[idx]} for idx in top_k_idx_sorted
        ]


# Example usage:
policy_rules_text = load_policy_rules(policy_rules_path)
docs = [{"page_content": txt} for txt in re.split(r"(?=\n##)", policy_rules_text)]
retriever = VectorStoreRetriever.from_docs(docs)
