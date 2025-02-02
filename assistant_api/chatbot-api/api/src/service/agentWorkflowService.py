from langchain.agents import Tool
import sys
from tools.watsonXDocumentTool import DocumentTool
from dotenv import load_dotenv
from envLoader.envLoader import load_app_env
load_app_env()

def test_tool(action_input):
    print('action_input: ', action_input)
    return "The discounts present in the King Diamond Tools contract are - Aggregate Order Discount"

def test_tool_db(action_input):
    print('action_input: ', action_input)
    return "The latest invoices are 13444, 13455"

def take_single_action(input_question: str):
    tools = [
        Tool(
                name="Document Service",
                func=DocumentTool,
                description="useful for when you need to get information about commodity pricing forecast,contracts, contract consumption,and any type of information"
            )
    ]
    name_to_tool_map = {tool.name: tool for tool in tools}
    print("calling chat endpoint")
    
    # return generate()
    response = "Document Service"
    print("Agent Response START")
    print(response)
    print("Agent Response END")
    response_data = {}

    if "Final Answer:" in response:
        final_answer = response.split("Final Answer:")[-1].strip()
        print(final_answer, flush=True)
        response_data['success'] = True
        response_data['data'] = final_answer
        response_data['type'] = 0
        return response_data
    else:
        action = response
        #action_input = match.group(2)
        action_input = input_question
        print(action)
        print(action_input)
        tool = name_to_tool_map[action]
        observation = tool.run(action_input, verbose=True, color='green', callbacks=None)
        response_data['success'] = True
        if action == "Document Service":
            response_data['type'] = ""
            response_data['data'] = observation["chat_response"]
            response_data['doclink'] = observation["doclink"]
        elif action == "Database Service":
            response_data['type'] = "table"
            response_data['data'] = observation
        else:
            print(f"Could not parse LLM output: `{response}`")
            response_data['success'] = False
            response_data['data'] = "Apologies. It seems we are facing some issues. Please try again later or try another question." 
        sys.stdout.flush()

        return response_data

def stream_1(input_question: str, tools):
    print('in stream_1', flush=True)
    response = "Document Service"
    response_data = {}
    action = response
    action_input = input_question
    print(action)
    #print(action_input)

    if action == "Document Service":
        response_data['success'] = True
        response_data['final'] = False
        response_data['action'] = action
        response_data['action_input'] = input_question
    elif action == "Database Service":
        response_data['success'] = True
        response_data['final'] = False
        response_data['action'] = action
        response_data['action_input'] = input_question
    else:
        print(f"Could not parse LLM output: `{response}`")
        response_data['success'] = False
        response_data['data'] = "Apologies. It seems we are facing some issues. Please try again later or try another question." 
    return response_data

def stream_2(action: str, action_input: str, name_to_tool_map):
    print('in stream_2', flush=True)
    print(action)
    print(action_input)
    response_data = {}
    tool = name_to_tool_map[action]
    print(tool)
    # print('tool')
    observation = tool.run(action_input, verbose=True, color='green', callbacks=None)
    print('tool run completed')
    # print(observation)
    response_data['success'] = True
    # response data type // 0: text response only, 1: text area response, 2: tabular data, 3: map data 
    if action == "Document Service":
        response_data['type'] = ""
        response_data['data'] = observation["chat_response"]
        response_data['doclink'] = observation["doclink"]
    elif action == "Database Service":
        response_data['type'] = "table"
        response_data['data'] = observation
    else:
        response_data['type'] = ""
        response_data['data'] = observation
        if (observation["doclink"]):
            response_data['doclink'] = observation["doclink"]
    sys.stdout.flush()
    return response_data

def test_stream():
    yield 1
    yield 2
    yield 3

def take_single_action_stream(input_question: str):
    tools = [
        Tool(
                name="Document Service",
                func=DocumentTool,
                description="useful for when you need to get information about Material Requirements Planning (MRP),Data Managemnet from documents about  Reorder point planning,planning calender,and any type of information"
            )
    ]
    name_to_tool_map = {tool.name: tool for tool in tools}
    def generate():
        print('in gen')
        response_data_1 = {}
        
        response_1 = stream_1(input_question=input_question, tools=tools)
        if response_1["success"]:
            if response_1["final"]:
                response_data_1["stream_end"] = True
                response_data_1["success"] = True
                response_data_1["data"] = response_1["data"]
                response_data_1["type"] = ""
                yield response_data_1
            else:
                response_data_1["stream_end"] = False
                response_data_1["success"] = True
                response_data_1["data"] = "Calling the " + response_1["action"]
                response_data_1["type"] = ""
                yield response_data_1
                response_2 = {}
                try:
                    print('going fo stream2')
                    print(response_1["action"])
                    print(response_1["action_input"])
                    response_2 = stream_2(response_1["action"], response_1["action_input"], name_to_tool_map)
                    response_2["stream_end"] = True
                except Exception as e:
                    print('exception when calling document tool')
                    #print(e)
                    response_2['success'] = False
                    response_2["stream_end"] = True
                    response_2['data'] = "Apologies. It seems we are facing some issues. Please try again later or try another question." 
                    response_2["type"] = ""
                yield response_2
        else:
            response_data_1["stream_end"] = True
            response_data_1["success"] = False
            response_data_1["data"] = response_1["data"]
            response_data_1["type"] = ""
            yield response_data_1
    
    return generate()

        