#Hardcoded Agent
from openai_module import generate_text_basic
from sample_functions import get_weather

current_weather = get_weather("California")

prompt = f"""
Should I take an umbrella when going out today in
California based on the following weather conditions: {current_weather}?"""

response = generate_text_basic(prompt,model="gpt-4o")

print(response)