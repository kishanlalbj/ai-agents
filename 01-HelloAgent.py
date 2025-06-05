import agents

model = agents.OpenAIChatCompletionsModel(
    model="llama3.2",
    openai_client = agents.AsyncOpenAI(
        base_url="http://localhost:11434/v1",
        api_key="localmodel"
    )
)

agent = agents.Agent(
    model=model,
    name="Hello Agent",
    instructions="First Agent"
)

result = agents.Runner.run_sync(agent,  input="Create a travel plan to bengaluru")

print(result.final_output)