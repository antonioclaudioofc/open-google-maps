import asyncio
import os
from dotenv import load_dotenv

from browser_use import Agent
from browser_use.llm.google import ChatGoogle

load_dotenv()


async def main():
    api_key = os.getenv("GOOGLE_API_KEY")

    llm = ChatGoogle(model="gemini-2.5-flash", api_key=api_key)

    agent = Agent(
        task="Abra o Google Maps e pesquise por 'Pizzarias em São Paulo'",
        llm=llm,
    )

    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
