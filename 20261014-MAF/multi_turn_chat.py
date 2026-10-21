import asyncio
from my_agent import agent, mslearn_mcp
from datetime import datetime
from agent_framework import AgentSession

# open the session file and load the session
# import json
# this_session = None
# with open("session.json", "r", encoding="utf-8") as f:
#     session_data = json.load(f)
#     this_session = AgentSession.from_dict(session_data)

this_session = agent.create_session()

async def main():
    while True:
        question = input("請輸入問題:(輸入'exit'或'quit'或按下Enter離開) ")
        if not question or question.lower() in ["exit", "quit"]:
            # serialized = this_session.to_dict()
            # print("\nSerialized session:")
            # print(serialized)
            # #export to json file
            # with open("session3.json", "w", encoding="utf-8") as f:
            #     import json
            #     json.dump(serialized, f, indent=4, ensure_ascii=False)
            await mslearn_mcp.close()
            break

        print("學號：1131533 姓名：黃詠珍")
        print(f"問: {question}")
        start_time = datetime.now()
        result = await agent.run(question, session=this_session)
        print(f"答: {result.text}")
        end_time = datetime.now()
        print(f"耗時: {(end_time - start_time).total_seconds():.2f} 秒")

asyncio.run(main())