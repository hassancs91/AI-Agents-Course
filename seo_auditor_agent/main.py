from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text
from actions import get_seo_page_report
from prompt import react_system_prompt

llm_instance = LLM.create(LLMProvider.OPENAI,model_name="gpt-4")


available_actions = {
    "get_seo_page_report": get_seo_page_report
}


user_query = """
how many images without alt tags are there on learnwithhasan.com"""


messages = [
    {"role": "system", "content": react_system_prompt},
    {"role": "user", "content": user_query}
]

turn_count = 1
max_turns = 5


while turn_count < max_turns:
    print (f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1

    agent_response = llm_instance.generate_response(messages=messages)

    messages.append({"role": "assistant", "content": agent_response})

    print(agent_response)

    #extract action JSON From Text Response.
    action_json = extract_json_from_text(agent_response)

    if action_json:
        function_name = action_json[0]['function_name']
        function_parms = action_json[0]['function_parms']
        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}: {function_parms}")
        print(f" -- running {function_name} {function_parms}")
        action_function = available_actions[function_name]
        action_function(**function_parms)
        #call the function
        result = action_function(**function_parms)
        print("Action_Response:", result)
        function_result_messge = f"Action_Response: {result}"
        messages.append({"role": "user", "content": function_result_messge})
        print("----------------------")
    else:
        break