import asyncio

from browser_use import Agent
from langchain_ollama import ChatOllama


llm = ChatOllama(model="mistral")


async def main():

    agent = Agent(
        task="""
Abra o Google Maps
e pesquise Petrolina
""",
        llm=llm,
    )

    await agent.run()


asyncio.run(main())
