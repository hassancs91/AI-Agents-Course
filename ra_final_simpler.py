
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text


llm_instance = LLM.create(provider=LLMProvider.OPENAI,model_name="gpt-4o")



from prompts import react_system_prompt
from sample_functions import get_weather



#Available actions are:
available_actions = {
    "get_weather": get_weather
}


prompt = """
what is the weather in New york?"""

messages = [
    {"role": "system", "content": react_system_prompt},
    {"role": "user", "content": prompt},
]

turn_count = 1
max_turns = 5

while turn_count < max_turns:
    print (f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1

    response = llm_instance.generate_response(messages=messages)

    print(response)

    json_function = extract_json_from_text(response)

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
            messages.append({"role": "user", "content": function_result_message})
            print(function_result_message)
    else:
         break