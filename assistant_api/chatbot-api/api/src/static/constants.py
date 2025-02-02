
### LLM Parameters ###
DECODING_METHOD_STR="decoding_method"
MAX_NEW_TOKENS_STR="max_new_tokens"
MIN_NEW_TOKENS_STR="min_new_tokens"
TEMERATURE_STR="temperature"
TOP_K_STR="top_k"
TOP_P_STR="top_p"
REPETITION_PENALTY_STR="repetition_penalty"
RANDOM_SEED_STR="random_seed"


### SQL LLM PARAMS ###
SQL_MAX_NEW_TOKENS= 400
SQL_RANDOM_SEED= 42
SQL_REPETITION_PENALTY= 1.03
SQL_TEMPERATURE=0.5
SQL_TOP_K=10
SQL_TOP_P=0.95
SQL_STOP_SEQUENCES=["SQL:",";"]

### CLASIFICATION LLM PARAMS ###
DECODING_METHOD_GREEDY="greedy"
CLASS_MAX_NEW_TOKENS= 200
CLASS_REPETITION_PENALTY= 1
CLASS_RANDOM_SEED= 42

class_parameters = {
    DECODING_METHOD_STR: DECODING_METHOD_GREEDY,
    MAX_NEW_TOKENS_STR: CLASS_MAX_NEW_TOKENS,
    REPETITION_PENALTY_STR: CLASS_REPETITION_PENALTY,
    RANDOM_SEED_STR: CLASS_RANDOM_SEED
}

codellama_params = {
    DECODING_METHOD_STR: "sample",
    MIN_NEW_TOKENS_STR: 1,
    MAX_NEW_TOKENS_STR: 400,
    RANDOM_SEED_STR: 42,
    TEMERATURE_STR: 0.05,
    TOP_K_STR: 5,
    #TOP_P_STR:0.95,
    REPETITION_PENALTY_STR: CLASS_REPETITION_PENALTY
}


keyword_params = {
    DECODING_METHOD_STR: "sample",
    MIN_NEW_TOKENS_STR: 1,
    MAX_NEW_TOKENS_STR: 300,
    RANDOM_SEED_STR: 42,
    TEMERATURE_STR: 0.05,
    TOP_K_STR: 5,
    #TOP_P_STR:0.90,
    REPETITION_PENALTY_STR: CLASS_REPETITION_PENALTY
}

### RAG LLM PARAMS ###
rag_parameters = {
        DECODING_METHOD_STR: DECODING_METHOD_GREEDY,
        MAX_NEW_TOKENS_STR: 1000,
        REPETITION_PENALTY_STR: CLASS_REPETITION_PENALTY,
    }

pdf_parsing_parameters_llm = {
    "decoding_method": "sample",
    "min_new_token": 5,
    "max_new_tokens": 500,
    "repetition_penalty": 2,
    "random_seed": 1234,
    "top_k":3,
    "temperature":0.1
}

EXCEPTION_ANSWER="Apologies. It seems we are facing some issues. Please try again later or try another question."

table_conn={'organization__org_type':'organization table can be joined to org_type table with joining key org_type_id.',
            'item__item_category':'item table can be joined to item_category table with joining key category_id.',
            'item__inventory':'item table can be joined to inventory table with joining key item_id.',
            'item__purchase_order':'item table can be joined to purchase order table with joining key item_id.',
            'organization__purchase_order':'organization table can be joined to purchase order table with joining key org_id.'}