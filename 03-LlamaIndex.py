import asyncio
import math

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool


def multiply(radius: float):
    return 2 * math.pi * radius

multiply_tool =FunctionTool.from_defaults(multiply)

agent = FunctionAgent(
    llm=Ollama(
        tool=[multiply_tool],
        model="llama3.2",
        request_timeout=360.0,
        context_window=8000
    ),
    system_prompt=(
    "You are a concise and accurate assistant. "
    "Only Use tool for multiplication "
    "Only return the final numeric result. Do not include commas"
    )
)


async def main():
    response = await agent.run("What is 3?")
    print(str(response))


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())