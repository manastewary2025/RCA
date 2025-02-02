import os
from langchain.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain import PromptTemplate
from langchain_core.prompts.chat import (
    ChatPromptTemplate
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.chroma import Chroma
from ibm_watsonx_ai.foundation_models.extensions.langchain import WatsonxLLM
from ibm_watsonx_ai.foundation_models import Model
import pandas as pd

my_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": ""
}

project_id = "d506c97c-6601-4c81-9d2e-26adf97f675e"
space_id = None
verify = False

model_id = "meta-llama/llama-3-70b-instruct"
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 1000,
    "repetition_penalty": 1
}

def format_docs_from_excel(file_path):
    # Load data from Excel
    data = pd.read_excel(file_path)

    # Select and format all columns
    formatted_docs = []
    for _, row in data.iterrows():
        doc_content = (
            f"Incident Number: {row.get('Number', 'N/A')}\n"
            f"Problem: {row.get('Problem', 'N/A')}\n"
            f"Priority: {row.get('Priority', 'N/A')}\n"
            f"ALM: {row.get('ALM', 'N/A')}\n"
            f"Assigned To: {row.get('Assigned to', 'N/A')}\n"
            f"State: {row.get('State', 'N/A')}\n"
            f"Short Description: {row.get('Short Description', 'N/A')}\n"
            f"Description: {row.get('Description', 'N/A')}\n"
            f"Configuration Item: {row.get('Configuration Item', 'N/A')}\n"
            f"Comments and Work Notes: {row.get('Comments and Work notes', 'N/A')}\n"
            f"Opened: {row.get('Opened', 'N/A')}\n"
            f"Opened By: {row.get('Opened by', 'N/A')}\n"
            f"Created: {row.get('Created', 'N/A')}\n"
            f"Assignment Group: {row.get('Assignment Group', 'N/A')}\n"
            f"Closed: {row.get('Closed', 'N/A')}\n"
        )
        formatted_docs.append(doc_content)
    
    return "\n\n".join(formatted_docs)

def create_vector_store_from_excel(file_path):
    embedding_model_name = "all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

    # Format documents from Excel file
    formatted_docs = format_docs_from_excel(file_path)

    # Create Chroma vector store
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory="" + os.getcwd() + "/incident_chroma_store",
    )

    # Add formatted docs to the vector store (Mocked for illustration)
    vector_store.add_texts([formatted_docs])

    return vector_store

prompt_text = """You always answer the questions with markdown formatting using GitHub syntax.
The markdown formatting you support: headings, bold, italic, links, lists, code blocks, and blockquotes.
You must omit that you answer the questions with markdown.
Any HTML tags must be wrapped in block quotes, for example <html>.
You will be penalized for not rendering code in block quotes.
When returning code blocks, specify language.
You are a helpful, respectful, and honest assistant. Always answer as helpfully as possible, while being safe.
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.
Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, explain why instead of answering something not correct.
If you don't know the answer to a question, please don't share false information.

You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.

Context: {context}

Question: {question}

Answer:
"""

@tool
def DocumentTool(question, file_path):
    '''
    Retrieves Information from Excel-based incident files
    '''
    print("Watsonx Document tool")
    print("\nQuestion: ", question)

    ## RAG Model Initialization
    llama_3_instruct_custom = Model(
        model_id=model_id,
        params=parameters,
        credentials=my_credentials,
        project_id=project_id)
    custom_rag_llm = WatsonxLLM(model=llama_3_instruct_custom)

    ## RAG Prompt creation
    prompt_new = ChatPromptTemplate.from_messages(
        [
            ("human", prompt_text)
        ]
    )

    ## Vector Store creation from Excel
    vector_store_retriver = create_vector_store_from_excel(file_path)

    ## RAG Chain
    rag_chain = (
        {"context": vector_store_retriver.as_retriever() | format_docs_from_excel(file_path), "question": RunnablePassthrough()}
        | prompt_new
        | custom_rag_llm
        | StrOutputParser()
    )

    ## Invoke RAG and retrieve source document
    response = rag_chain.invoke(question)
    print("Response from rag_chain.invoke:", response)

    docs = vector_store_retriver.similarity_search(question)
    if docs and len(docs) > 0:
        doclinks = []
        for doc in docs:
            filename = os.path.basename(doc.metadata.get("source", ""))
            doclink = "https://example.com/docs/" + filename
            doclinks.append(doclink)
    else:
        doclinks = []

    response = {"chat_response": response, "doclinks": doclinks}
    return response

# Example usage
file_path = "/mnt/data/Incidents_Exports_mini.xlsx"
question = "Summarize incidents related to Windows errors."
DocumentTool(question, file_path)
