import asyncio
from my_agent import agent
from datetime import datetime

async def main():
    question = "說一個冷笑話。"
    print(f"問: {question}")
    start_time = datetime.now()
    result = await agent.run(question)
    end_time = datetime.now()
    print(f"答: {result}")
    print(f"耗時: {(end_time - start_time).total_seconds():.2f} 秒")

asyncio.run(main())