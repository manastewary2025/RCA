from langchain.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts.chat import (
    ChatPromptTemplate
)
import os
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores.chroma import Chroma
from rag.embeddingRetriver import create_vector_store
from ibm_watsonx_ai.foundation_models.extensions.langchain import WatsonxLLM
from ibm_watsonx_ai.foundation_models import Model
from dotenv import load_dotenv
from envLoader.envLoader import load_app_env
load_app_env()
from static.prompts import prompt_text_excel,prediction_prompt_excel
from static.constants import rag_parameters,EXCEPTION_ANSWER
import sys

my_credentials = { 
    "url"    : os.getenv("url"), 
    "apikey" : os.getenv("api_key")
}      
project_id  = os.getenv("project_id")
model_id = os.getenv("document_model_id")
document_s3_bucket_link=os.getenv("s3_bucket_url")

parameters = rag_parameters
# parameters = {
#         "decoding_method": "greedy",
#         "max_new_tokens": 1000,
#         "repetition_penalty": 1
#     }

def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


@tool
def DocumentTool(question):
    '''
    Retrieves Information from doc files
    '''
    print("Watsonx Document tool")
    print("\nin document tool\nquestion: ", question)
    print("\ndoc tool model_id: ", model_id)
    sys.stdout.write("Watsonx Document tool")
    sys.stdout.write("doc tool model_id: "+ model_id)

    ##RAG Model Intialization
    llama_3_instruct_custom = Model(
            model_id=model_id,
            params=parameters,
            credentials=my_credentials,
            project_id=project_id)
    custom_rag_llm = WatsonxLLM(model=llama_3_instruct_custom)

    ## RAG Prompt creation
    prompt_new = ChatPromptTemplate.from_messages(
            [
                ("human", prediction_prompt_excel)
            ]
    )

    ##RAG supplier number filter
    #supplier_number=apply_filter(input_question=question)
    ## Vector Store creation
    vector_store_retriver=create_vector_store()

    retriver=vector_store_retriver.as_retriever()
    #retriver.search_kwargs={"filter":{'supplier_number': {'$in': supplier_number}}}
        
    ##Rag Creation
    rag_chain = (
        {"context": retriver| format_docs, "question": RunnablePassthrough()}
        | prompt_new
        | custom_rag_llm
        | StrOutputParser()
       )

    ##RAG invoke and source document retrival
    response=rag_chain.invoke(question)

    docs=retriver.invoke(question)
    if docs and len(docs) > 0:
            doclinks = []
            for doc in docs:
                filename =os.path.basename(doc.metadata["source"])#doc.metadata["source"].split("./../data/docs/", 1)[1]
                # Construct the link for each document
                doclink = document_s3_bucket_link + filename
                #doclinks.append(doclink)
    else:
        raise ValueError("Document list is empty.")

    response = {"chat_response": response, "doclink": doclink}
    return response
        
