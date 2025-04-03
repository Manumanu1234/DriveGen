# Import the required libraries
import os.path
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pydantic import BaseModel,Field
from langchain.prompts import PromptTemplate
from mcp_server.helper import Auth,Remove
load_dotenv()
Groq_key=os.getenv("Groq_api")
groq=ChatGroq(
    api_key=Groq_key,
    model_name="gemma2-9b-it",
    temperature=0,
    )
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from typing import Optional

class AnalysisData(BaseModel):
    """Data model for analysis results with file and communication details."""
    filename: str = Field(default="None", description="Name of the file ")
    send_method: str = Field(default="Email", description="Communication method: Telegram/Email")
    email: Optional[str] = Field(default=None, description="Receiver email address if method is Email")

def ai_analysis(state) -> dict:
    """
    Analyze the query and extract structured data using AI.
    
    Args:
        query: User input query containing file information
        llm_client: Configured LLM client (e.g., Groq)
        
    Returns:
        Structured AnalysisData object
        
    Raises:
        ValueError: If structured output parsing fails
    """
    template = """You are an assistant that extracts file information from queries.
    Extract ONLY the following details:
    - File name
    - Preferred send method (Telegram or Email or Download)
    - Email address (if method is Email)
    
    Query: {query}
    """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=['query']
    )
    
    try:
        structured_output = groq.with_structured_output(AnalysisData)
        chain = prompt | structured_output
        result = chain.invoke({"query": state['messages'][-1].content})
        print(result)
        
        if not isinstance(result, AnalysisData):
            raise ValueError("Failed to parse structured output")
        return {"Method":result.send_method,"FileName":result.filename}
        
    except Exception as e:
        print(f"Analysis failed: {str(e)}")
        raise

def router(state):
    if state['Method']=='Telegram':
        return "Telegram"
    elif state['Method']=='Email':
        return 'Email'
    return "Download"
def Fun1(state):
    #For Telegram
    prompt=f"First Download the File from the Drive Filename={state['FileName']} And Then Send the file Through Email"
    print("---Working--")
    return {"Prompt":prompt}
def Fun2(state):
    #
    prompt=f"First Download the File from the Drive Filename={state['FileName']} And Then Send the file Through Telegram"
    return {"Prompt":prompt}
def Fun3(state):
    prompt=f"Download the File Frome the Drive Filename={state['FileName']}"
    return {"Prompt":prompt}
from mcp_server.Agent import main_sync
from langgraph.graph import StateGraph,START,END,MessagesState
class FinalGraph(MessagesState):
    Method:str
    FileName:str
    Prompt:str
    final_ans:str
workflow=StateGraph(FinalGraph)

workflow.add_node("Query_Analyisis",ai_analysis)
workflow.add_edge(START,"Query_Analyisis")
workflow.add_node("Pre_Prop1",Fun1)
workflow.add_node("Pre_Prop2",Fun2)
workflow.add_node("Pre_Prop3",Fun3)
workflow.add_conditional_edges(
    "Query_Analyisis",
    router,{
        "Email":"Pre_Prop1",
        "Telegram":"Pre_Prop2",
        "Download":"Pre_Prop3"
    }
)
workflow.add_node("Agents",main_sync)

workflow.add_edge("Pre_Prop1","Agents")
workflow.add_edge("Pre_Prop2","Agents")
workflow.add_edge("Pre_Prop3","Agents")
workflow.add_edge("Agents",END)

app=workflow.compile()
#question="can you please download the file 'PM YUVA 3.pdf'"

def execute(question):
    result=app.invoke({"messages":[question]})
    print("----------------------------------")
    print(result['messages'][-1])
    return {"result":result['messages'][-1].content}