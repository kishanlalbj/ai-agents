import agents

# Setup local model
model = agents.OpenAIChatCompletionsModel(
    model="llama3.2",
    openai_client=agents.AsyncOpenAI(
        base_url="http://localhost:11434/v1",
        api_key="localhost"
    )
)

guidance_agent = agents.Agent(
    name="GuidanceAgent",
    instructions="You are a career guidance teacher, Based on users interest, suggest 3 career roles",
    model=model
)

user_input = "I am interested in AI/ML. What career paths should I consider"
career_result = agents.Runner.run_sync(guidance_agent, user_input)

motivation_agent = agents.Agent(
    name="Motivation Agent",
    instructions="You are a motivational speaker, motivate user to achieve big in those career",
    model=model
)


motivation_result = agents.Runner.run_sync(motivation_agent, career_result.final_output)

print(motivation_result.final_output)