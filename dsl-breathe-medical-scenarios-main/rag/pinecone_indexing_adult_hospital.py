import os
import re

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

from openai import OpenAI

from tqdm import tqdm
from tika import parser

from dotenv import load_dotenv

load_dotenv(override=True)

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
spec = ServerlessSpec(cloud="aws", region="us-east-1")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = 'text-embedding-ada-002'

# Define the index name
# index_name = "clinical-guidelines-sections"
index_name = "adult-hospital"

# Create the index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(index_name, dimension=1536, spec=spec)

# Instantiate the index
index = pc.Index(index_name)


# Define a function to preprocess text
def preprocess_text(text):
    # Replace consecutive spaces, newlines and tabs
    text = re.sub(r'\s+', ' ', text)
    return text


def process_pdf(file_path):
    # create a loader
    loader = PyPDFLoader(file_path)
    # load your data
    data = loader.load()
    # Split your data up into smaller documents with Chunks
    # TODO: split the data based on the chapter names

    whole_text = ''

    # Extract the text from the PDF, these are the relevant pages
    for i in range(42, 602):
        page = data[i].page_content
        whole_text += preprocess_text(page.replace('\n', ' ').replace('\uf0b7', ' '))

    # delete page numbers
    pattern = r'(2019\s+\w+)'
    whole_text = re.sub(pattern, '', whole_text)

    # match for chapters
    pattern = (r'(\b(?:[1-9]|1[0-9]|20)(?:\.(?:[1-9]|1[0-9]|20)){1,})\s(.*?)(?=\b(?:[1-9]|1[0-9]|20)(?:\.(?:[1-9]|1['
               r'0-9]|20)){1,}\b|$)')
    texts = re.findall(pattern, whole_text)

    # discard text if it is too short or too long
    filtered_texts = [text[0] + ' ' + text[1] for text in texts if (10 < len(text[1].split(' ')) < 1000)]

    return filtered_texts


# Create embeddings
def create_embeddings(texts):
    embeddings_list = []
    for text in tqdm(texts):
        # print(text)
        if len(text) > 8000:
            continue
        res = client.embeddings.create(input=text, model=MODEL)
        embeddings_list.append(res.data[0].embedding)
    return embeddings_list


# Upsert embeddings to Pinecone
def upsert_embeddings_to_pinecone(index, embeddings, texts, filename):
    # upsert embeddings in batches
    batch_size = 100
    for i in tqdm(range(0, len(embeddings), batch_size)):
        meta_batch = [{'text': text} for text in texts[i:i + batch_size]]
        embedding_batch = embeddings[i:i + batch_size]
        ids_batch = [f'{filename}_{i + j}' for j in range(batch_size)][:len(embedding_batch)]
        index.upsert(vectors=[{
            'id': id,
            'values': embedding,
            'metadata': meta
        } for id, embedding, meta in zip(ids_batch, embedding_batch, meta_batch)])


# # Process a PDF and create embeddings
# file_path = "HPSCA_Clinical_Guidelines.pdf"
file_path = "Adult Hospital level Standard treatment guidelines and Essential medicines list for 2019.pdf"

print(f"Processing {file_path}")
texts = process_pdf(file_path)

# Preprocess the texts
print("Creating embeddings for the texts")
embeddings = create_embeddings(texts)

# Upsert the embeddings to Pinecone
print("Upserting embeddings to Pinecone")
upsert_embeddings_to_pinecone(index, embeddings, texts, 'generated heart attack.pdf')
