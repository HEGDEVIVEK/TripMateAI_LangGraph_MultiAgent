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

llm_model = init_chat_model(model="gpt-5-nano")

class llm_weather_schema(BaseModel):
    search_query : str | None = Field(description="Extract the destination city name from the user query. Return null if the destination is missing or ambiguous.")

llm_with_weather_structured_output = llm_model.with_structured_output(llm_weather_schema)

def weather_agent_node(state:graph_schema):
    user_query = state["user_query"]

    weather_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Extract the destination city name from the user query."
            "Return null if the destination is missing or ambiguous."
            "Don't make up any additional details"
            "Destination city name ony required no aditional deatils are needed"
            "Destination cuty name is required to the weather mcp tool api call later"
        ),
        ("human", "{user_query}")
    ])

    weather_chain = weather_prompt | llm_with_weather_structured_output

    response = weather_chain.invoke({"user_query" : user_query})

    mcp_tool_result = asyncio.run(get_weather_mcp_tool(response.search_query))

    llm_answer = llm_model.invoke([
        HumanMessage(content=f"Summarize the following weather details in a human-readable format and give suggetion whether it is good time to visit based on the weather condition:\n\n{mcp_tool_result}")
    ])

    llm_answer.name = "weather_node"

    return{
        "weather_result" : llm_answer.content,
        "messages" : [llm_answer]
    }


# state ={
#     "user_query" : "I need to travel from Banglore to madgaon. Find hotels near railway station in madgaon",
#     "messages" : [],
#     "flight_result" : [],
#     "hotel_result" : "",
#     "itinerary_result" : ""
# }

# result = weather_node(state)
# print(result["weather_result"])
# print(result["messages"])