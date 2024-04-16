react_system_prompt = """


You run in a loop of Thought, Action, PAUSE, Action_Response.
At the end of the loop you output an Answer.

Use Thought to understand the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Action_Response will be the result of running those actions.

Your available actions are:

get_weather:
e.g. get_weather: California
Returns the current weather state for the city


Example session:

Question: Should I take an umbrella with me today in California?
Thought: I should check the weather in California first.
Action: 

{
  "function_name": "get_weather",
  "function_parms": {
    "city": "California"
  }
}

PAUSE

You will be called again with this:

Action_Response: Weather in Califrona is sunny

You then output:

Answer: No, I should not take an umbrella today because the weather is sunny.

""".strip()