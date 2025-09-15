import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
set_tracing_disable=True

API_KEY=os.getenv("GEMINI_API_KEY")


if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing.Please check your .env file.")

MODEL= "gemini-2.0-flash"

BASE_URL="https://generativelanguage.googleapis.com/v1beta"

external_client= AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

model=OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client
)
async def main():    
    agent=Agent(
    name="Joker",
    instructions="you are a funny assistant,always reply in funny way.",
    model=model
)
    User_Question=input("Enter your Question:")

    result= Runner.run_streamed(agent, User_Question)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            if event.data.delta:
                print(event.data.delta, end="", flush=True)
            
if __name__== "__main__":                        
    asyncio.run(main())
