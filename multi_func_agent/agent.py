from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text
from functions import seo_audit_web_page,search_wikipedia,load_content_from_url
from prompt import system_prompt_three_examples,system_prompt_two_examples,system_prompt_one_example

llm_instance = LLM.create(LLMProvider.OPENAI,model_name="gpt-4o")


available_actions = {
    "seo_audit_web_page": seo_audit_web_page,
    "search_wikipedia": search_wikipedia,
    "load_content_from_url": load_content_from_url
}


user_query_1 = """
what is the response time of this web page: learnwithhasan.com?"""

user_query_2 = """
generate a conside bullet point summary of the following article: 
https://learnwithhasan.com/generate-content-ideas-ai/?"""

user_query_3 = """
When was Isaac Newton born?"""


messages = [
    {"role": "system", "content": system_prompt_one_example},
    {"role": "user", "content": user_query_1}
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
        print("Observation:", result)
        function_result_messge = f"Observation: {result}"
        messages.append({"role": "user", "content": function_result_messge})
        print("----------------------")
    else:
        break