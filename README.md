# sca_genai_python

assistant-api for flask api with custom sca agent that combines pdf and dynamic sql tools. requirements_v2.txt contains the python libraries required. 
sca assistant uses the /reply endpoint, which calls sca_custom_agent in  chatbot-api/custom_agents/  

## Installation Steps

All required libraries to run the flask server is in file requirements_v2.txt , run the following commands:
```
pip install -r requirements_v2.txt
```

To run the server
```
flask --app .assistant_api/chatbot-api/api/src/index.py  --debug run -h 0.0.0.0 -p 5002
```

### Scripts & Data

- `assistant_api/chatbot-api/api/src/rag/documentparserGeneric.py`: Load files into vector db