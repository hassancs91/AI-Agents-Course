
from openai_module import generate_text_basic
from prompts import react_system_prompt
from sample_functions import get_weather
from json_helpers import extract_json


#Available actions are:
available_actions = {
    "get_weather": get_weather
}


prompt = """
Should I take an umbrella when going out today in London?"""

response = generate_text_basic(prompt, model="gpt-4o",system_prompt = react_system_prompt)

#print(f"Response from the model: {response}")
#we want to instruct the model to call the action or the function
json_function = extract_json(response)

#print(f"Extracted Json Functions{json_function}")

if json_function:
        function_name = json_function[0]['function_name']
        function_parms = json_function[0]['function_parms']
        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}: {function_parms}")
        print(f" -- running {function_name} {function_parms}")
        action_function = available_actions[function_name]
        #call the function
        result = action_function(**function_parms)
        function_result_message = f"Action_Response: {result}"
        print(function_result_message)