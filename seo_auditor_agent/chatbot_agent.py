from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text
from actions import get_seo_page_report
from prompt import react_system_prompt
import time


llm_instance = LLM.create(LLMProvider.OPENAI,model_name="gpt-4")


available_actions = {
    "get_seo_page_report": get_seo_page_report
}


# user_query = """
# how many images without alt tags are there on learnwithhasan.com"""


# messages = [
#     {"role": "system", "content": react_system_prompt},
#     {"role": "user", "content": user_query}
# ]

def get_final_response(messages):
    
    turn_count = 1
    max_turns = 5
    final_response = ""  # Variable to store the final response

    while turn_count < max_turns:
        turn_count += 1

        agent_response = llm_instance.generate_response(messages=messages)
        messages.append({"role": "assistant", "content": agent_response})
        final_response = agent_response  # Update final response each loop

        action_json = extract_json_from_text(agent_response)

        if action_json:
            function_name = action_json[0]['function_name']
            function_parms = action_json[0]['function_parms']
            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}")
            action_function = available_actions[function_name]
            result = action_function(**function_parms)  # Call the function
            function_result_message = f"Action_Response: {result}"
            messages.append({"role": "user", "content": function_result_message})
        else:
            break

    return final_response


def get_final_response_updated(messages):


    turn_count = 1
    max_turns = 5
    final_response = ""
    function_used = False
    function_name_used = None  # To store the name of the function used
    start_time = time.time()

    while turn_count < max_turns:
        agent_response = llm_instance.generate_response(messages=messages)
        messages.append({"role": "assistant", "content": agent_response})
        final_response = agent_response

        action_json = extract_json_from_text(agent_response)
        if action_json:
            function_used = True
            function_name = action_json[0]['function_name']
            function_parms = action_json[0]['function_parms']
            function_name_used = function_name  # Store the function name
            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}")
            action_function = available_actions[function_name]
            result = action_function(**function_parms)
            function_result_message = f"Action_Response: {result}"
            messages.append({"role": "user", "content": function_result_message})
        else:
            break

        turn_count += 1

    elapsed_time = time.time() - start_time
    return {
        "response": final_response,
        "execution_time": elapsed_time,
        "function_used": function_used,
        "function_name_used": function_name_used,
        "iterations": turn_count
    }




#the simple chatbot agent
def chat_with_ai():
    messages = [
        {"role": "system", "content": react_system_prompt}
    ]

    print("Chat with the AI agent. Type 'exit' to end the chat.")

    while True:
        user_query = input("You: ")
        if user_query.lower() == 'exit':
            break
        
        messages.append({"role": "user", "content": user_query})
        response = get_final_response_updated(messages)
        print("AI:", response["response"])
        print("Itterations:", response["iterations"])
        print(f"Time Taken: {response['execution_time']:.2f} seconds")
        if response["function_used"]:
            print(f"A function ({response["function_name_used"]}) was executed during this interaction.")
        else:
            print("No function was executed.")

     
        

chat_with_ai()


