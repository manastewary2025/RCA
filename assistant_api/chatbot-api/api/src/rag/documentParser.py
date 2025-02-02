from ibm_watsonx_ai.foundation_models import Model
from glob import glob
import os
import re
import pdfplumber
import pandas as pd
import openpyxl
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv
from math import ceil

# Load environment variables
def load_app_env():
    """Load environment variables from a .env file."""
    flask_env = os.getenv("FLASK_ENV")

    if flask_env == 'development':
        load_dotenv(dotenv_path='/mnt/secrets-store/sca-genai-assistant-api')
        model_id = os.getenv("document_model_id")
        api_key = os.getenv("api_key")
    else:
        load_dotenv()

load_app_env()

document_parsing_parameters_llm = {
    "decoding_method": "sample",
    "min_new_token": 5,
    "max_new_tokens": 500,
    "repetition_penalty": 2,
    "random_seed": 1234,
    "top_k": 3,
    "temperature": 0.1
}

embedding_model_name = os.getenv("embedding_model_name")
file_path = os.getenv("document_path")
embedding_path_insert = os.getenv("embedding_path_insert")

chunk_size = 1000
chunk_overlap = 100

# Model Initialization
watsonx_model = os.getenv('pdf_metadata_model')
index_name = f'index_db_hd_{embedding_model_name}_section_{chunk_size}_{chunk_overlap}'
parameters_llm = document_parsing_parameters_llm

my_credentials = { 
    "url"    : os.getenv("url"), 
    "apikey" : os.getenv("api_key")
}
project_id  = os.getenv("project_id")

metadata_extract_model = Model(
    model_id=watsonx_model,
    params=parameters_llm,
    credentials=my_credentials,
    project_id=project_id
)

# Text Splitter Initialization
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

# Function to process Excel file
def process_excel(file_path, batch_size=100):
    """
    Processes an Excel file and converts its rows to Document objects in batches.

    Args:
        file_path (str): Path to the Excel file.
        batch_size (int): Number of rows to process in each batch.

    Returns:
        List[List[Document]]: A list of batches, where each batch is a list of Document objects.
    """
    print(f"Processing Excel file: {file_path}")
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        print(f"Columns in the Excel file: {df.columns.tolist()}")

        # Total number of batches
        total_batches = ceil(len(df) / batch_size)
        print(f"Total rows: {len(df)}, Processing in {total_batches} batches (Batch size: {batch_size})")

        # Function to convert a row to a Document
        def row_to_document(row, idx):
            content = row.to_dict()
            content_str = "\n".join(
                [f"{key}: {value}" for key, value in content.items() if pd.notnull(value)]
            )
            return Document(
                page_content=content_str,
                metadata={
                    "source": file_path,
                    "row_index": idx
                }
            )

        # Process rows in batches
        batched_documents = []
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min((batch_num + 1) * batch_size, len(df))
            print(f"Processing batch {batch_num + 1}/{total_batches} (Rows {start_idx} to {end_idx - 1})")

            # Convert rows in the current batch to Document objects
            batch = [
                row_to_document(df.iloc[idx], idx)
                for idx in range(start_idx, end_idx)
            ]
            batched_documents.append(batch)

        print("Excel processing completed.")
        return batched_documents

    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return []

# File paths

excel_file_path = glob("C:\\ibm-aws-sca\\assistant_api\\chatbot-api\\api\\src\\rag\\data\\documents\\*.xlsx", recursive=True)

# Process Excel file
print("Excel process started")
if isinstance(excel_file_path, list) and len(excel_file_path) > 0:
    excel_file_path = excel_file_path[0]

if isinstance(excel_file_path, str) and os.path.isfile(excel_file_path):
    excel_texts = process_excel(excel_file_path)
else:
    print(f"Invalid or missing Excel file at: {excel_file_path}")
    excel_texts = []

# Combine all documents
# Flatten the nested list structure of excel_texts
flattened_excel_texts = [doc for batch in excel_texts for doc in batch] if isinstance(excel_texts, list) else []


# Ensure texts are not empty before processing
print(f"Number of documents to process: {len(flattened_excel_texts)}")
if len(flattened_excel_texts) == 0:
    print("No documents found, please check if PDF and Excel parsing are working correctly.")
else:
    # Initialize embeddings for Chroma vector store
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vector_db_path = os.getcwd() + embedding_path_insert
    print(f"Vector DB will be stored at: {vector_db_path}")

    # Handle the case where documents might be too large in one go
    # Split the documents into manageable chunks for Chroma if batch size exceeds limit
    MAX_BATCH_SIZE = 166
    batched_documents = []
    total_batches = ceil(len(flattened_excel_texts) / MAX_BATCH_SIZE)

    for batch_num in range(total_batches):
        start_idx = batch_num * MAX_BATCH_SIZE
        end_idx = min((batch_num + 1) * MAX_BATCH_SIZE, len(flattened_excel_texts))
        batch = flattened_excel_texts[start_idx:end_idx]
        batched_documents.append(batch)

        print(f"Processing batch {batch_num + 1}/{total_batches} (Documents {start_idx} to {end_idx - 1})")
        # Create the vector store for this batch
        vectordb = Chroma.from_documents(batch, embedding=embeddings, persist_directory=vector_db_path)
        vectordb.persist()  # Save the current batch
        print(f"Persisted {len(batch)} documents from batch {batch_num + 1}")

    # After all batches have been processed, check total number of documents
    print("All batches processed. Final vector store count:")
    print(vectordb._collection.count())
