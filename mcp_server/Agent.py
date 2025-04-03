from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
import asyncio
load_dotenv()
Groq_key=os.getenv("Groq_api")
groq=ChatGroq(
    api_key=Groq_key,
    model_name="gemma2-9b-it",
    temperature=0,
    )
async def main(state):
    prompt=state['Prompt']
    print(prompt)
    print("--------------------------------------------------------------------------------")
    async with MultiServerMCPClient(
        {
            "Drive": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["C:/Users/Manu/Desktop/Drive_AI/mcp_server/mcp_server1.py"],
                "transport": "stdio",
            },
            "Send": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["C:/Users/Manu/Desktop/Drive_AI/mcp_server/mcp_server2.py"],
                "transport": "stdio",
            },
        }
    ) as client:
        agent = create_react_agent(groq, client.get_tools())
        response = await agent.ainvoke({"messages": prompt})
        print(response['messages'][-2].content)
        final_res=response['messages'][-2].content
        return final_res
def main_sync(state):
    res=asyncio.run(main(state))
    return {"messages":res}