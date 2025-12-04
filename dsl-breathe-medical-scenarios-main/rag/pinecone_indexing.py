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
spec = ServerlessSpec(cloud="aws", region="eu-west-1")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = 'text-embedding-ada-002'

# Define the index name
index_name = "clinical-guidelines-sections"

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
    for i in range(4, 207):
        whole_text += data[i].page_content

    # Finding chapter splits (note that this is a proxy and may be imperfect)
    texts = []
    chapter_splitter = doc_splitter = re.compile(r"(?<=\n)(\d+\. .*?)(?<=\n)(?=\d+\. |$)", re.DOTALL)
    doc_splitter = re.compile(r"(?<=\n)(\d+\.\d+.*?)(?<=\n)(?=\d+\.\d+|$)", re.DOTALL)

    chapter_split = chapter_splitter.finditer(whole_text)

    for match in tqdm(chapter_split):
        split_chapter = doc_splitter.finditer(match.group())

        chapter_name = match.group().split('\n')[0].strip()

        current_section = ''
        current_subsection = ''

        for match in split_chapter:
            section_name = match.group().split('\n')[0].strip()

            section_text = preprocess_text(match.group().replace('\n', ' '))
            
            processed_text = ''

            # Check if the match is a section (e.g. 1.1)
            if re.match(r"\d+\.\d+ ", section_name):
                current_section = section_name
                processed_text = f'{chapter_name} > {section_text}'

            # Check if the match is a subsection (e.g. 1.1.1)
            elif re.match(r"\d+\.\d+\.\d+ ", section_name):
                current_subsection = section_name
                processed_text = f'{chapter_name} > {current_section} > {section_text}'
            else:
                processed_text = f'{chapter_name} > {current_section} > {current_subsection} > {section_text}'

            # If text is too short (proxy that it has less than 8 words), it is only a title and should be skipped
            if len(processed_text.split(' ')) < 8:
                continue

            texts.append(processed_text)
            # print(processed_text)

    return texts

# Create embeddings
def create_embeddings(texts):
    embeddings_list = []
    for text in tqdm(texts):
        res = client.embeddings.create(input=text, model=MODEL)
        embeddings_list.append(res.data[0].embedding)
    return embeddings_list

# Upsert embeddings to Pinecone
def upsert_embeddings_to_pinecone(index, embeddings, texts, filename):
    # upsert embeddings in batches
    batch_size = 100
    for i in tqdm(range(0, len(embeddings), batch_size)):
        meta_batch = [{'text': text} for text in texts[i:i+batch_size]]
        embedding_batch = embeddings[i:i+batch_size]
        ids_batch = [f'{filename}_{i + j}' for j in range(batch_size)][:len(embedding_batch)]
        index.upsert(vectors=[{
            'id': id,
            'values': embedding,
            'metadata': meta
        } for id, embedding, meta in zip(ids_batch, embedding_batch, meta_batch)])

# # Process a PDF and create embeddings
file_path = "HPSCA_Clinical_Guidelines.pdf"

print(f"Processing {file_path}")
texts = process_pdf(file_path)

# Preprocess the texts
print("Creating embeddings for the texts")
embeddings = create_embeddings(texts)

# Upsert the embeddings to Pinecone
print("Upserting embeddings to Pinecone")
upsert_embeddings_to_pinecone(index, embeddings, texts, 'HPSCA_Clinical_Guidelines')