import os 
import asyncio
from dotenv import load_dotenv
load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("bro it is working")
    
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from tripmateai_langgraph_multiagent.graph_schema import graph_schema
from langchain_core.messages import HumanMessage
from tripmateai_langgraph_multiagent.mcp_client.weather_mcp import get_weather_mcp_tool
from langchain_core.prompts import MessagesPlaceholder

llm_model = init_chat_model(model="gpt-5-nano")

class llm_weather_schema(BaseModel):
    search_query : str | None = Field(
        description=(
             "The city whose weather the user wants, resolved from "
            "the conversation and latest corrections. Preserve the "
            "previous city unless changed. Return null if the city "
            "remains missing or ambiguous after considering history."
        )
    )
llm_with_weather_structured_output = llm_model.with_structured_output(llm_weather_schema)

def weather_agent_node(state:graph_schema):
    history = state["messages"]

    weather_prompt = ChatPromptTemplate.from_messages([ 
        ("system",
        """
            Extract the city whose weather the user currently wants.

            Use conversation history to understand follow-up requests.
            Prioritize the latest user instructions.
            Preserve earlier trip details unless the user changes them.

            If the user explicitly requests weather for a particular city,
            use that city. Otherwise, use the trip's destination.

            A city absent from the latest message is not missing if it
            was clearly established earlier for the same trip.

            Do not reuse an earlier destination when the user explicitly
            starts a new trip without specifying a destination.

            Return only the city in search_query.
            Do not invent missing details.
            Return null if no single city can be resolved.
        """
    ),
    MessagesPlaceholder(variable_name="history"),
    ])

    weather_chain = weather_prompt | llm_with_weather_structured_output

    response = weather_chain.invoke({"history" : history})

    mcp_tool_result = asyncio.run(get_weather_mcp_tool(response.search_query))

    llm_answer = llm_model.invoke([
        HumanMessage(content=f"Summarize the following weather details in a human-readable format and give suggetion whether it is good time to visit based on the weather condition:\n\n{mcp_tool_result}")
    ])

    llm_answer.name = "weather_node"

    return{
        "weather_result" : llm_answer.content,
        "messages" : [llm_answer]
    }