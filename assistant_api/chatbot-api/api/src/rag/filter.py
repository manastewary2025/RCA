# import os
# from ibm_watsonx_ai.foundation_models import Model
# from static.prompts import rag_filter_prompt
# from static.constants import rag_parameters
# from langchain import PromptTemplate
# import ast

# def apply_filter(input_question):
#     my_credentials = { 
#         "url"    : os.getenv("url"), 
#         "apikey" : os.getenv("api_key")
#     }      
#     project_id  = os.getenv("project_id")
#     model_id = os.getenv("document_model_id")
#     parameters=rag_parameters
#     # parameters = {
#     #         "decoding_method": "greedy",
#     #         "max_new_tokens": 1000,
#     #         "repetition_penalty": 1
#     #     }

#     llama_3_instruct_custom_v2 = Model(
#             model_id=model_id,
#             params=parameters,
#             credentials=my_credentials,
#             project_id=project_id)


#     prompt_template_v1 = PromptTemplate(input_variables = ["input"],template = rag_filter_prompt)
#     agent_prompt_v1=prompt_template_v1.format(input=input_question)

#     answer=llama_3_instruct_custom_v2.generate(agent_prompt_v1)
#     print(answer['results'][0]['generated_text'])
#     supplier_number=answer['results'][0]['generated_text']

#     # Convert to list using ast.literal_eval
#     result_list = ast.literal_eval(supplier_number)

#     return result_list