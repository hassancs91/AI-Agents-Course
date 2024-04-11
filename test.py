from openai_module import generate_text_basic

prompt = "Should I take an umbrella when going out today in California?"

response = generate_text_basic(prompt,model="gpt-4")

print(response)