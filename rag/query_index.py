from openai import OpenAI
from pinecone import Pinecone

import os
from dotenv import load_dotenv

load_dotenv(override=True)

def rag_filter(query):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

    MODEL = 'text-embedding-ada-002'

    xq = client.embeddings.create(input=query, model=MODEL).data[0].embedding

    # Define the index name
    index_name = "adult-hospital"

    # Instantiate the index
    index = pc.Index(index_name)

    res = index.query(vector=[xq], top_k=3, include_metadata=True)

    matches = ""

    for match in res['matches']:
        matches += "\n" + match['metadata']['text']

    
    return matches