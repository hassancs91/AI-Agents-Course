#Hardcoded Agent
from openai_module import generate_text_basic
from prompts import react_system_prompt

prompt = """
Should I take an umbrella when going out today in Arizona?"""

response = generate_text_basic(prompt, model="gpt-4",system_prompt = react_system_prompt)

print(response)