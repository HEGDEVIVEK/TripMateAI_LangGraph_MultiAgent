import os
from dotenv import load_dotenv
load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("bro it is working")

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from tripmateai_langgraph_multiagent.tools.tavily_tool import tavily_search_tool
from tripmateai_langgraph_multiagent.graphSchema import graph_schema

llm_model = init_chat_model(model="gpt-5-nano")


class llm_hotel_schema(BaseModel):
    search_query : str | None = Field(
        description=(
            "A web search query for hotels at the user's destination. "
            "Include location, budget, currency, dates, guests, and "
            "preferences only when provided. "
            "Return null if the destination is missing or ambiguous."
        )
    )
llm_with_hotel_structured_output = llm_model.with_structured_output(llm_hotel_schema)

def hotel_agent_node(state: graph_schema):

    user_query = state["user_query"]

    hotel_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Create a focused web search query for hotels. "
            "Use the destination city, not the departure city. "
            "Preserve the user's budget, currency, dates, and preferences. "
            "Do not invent missing details. "
            "Return null for search_query if the destination is unclear."
        ),
        ("human", "{user_query}")
    ])

    hotel_chain = hotel_prompt | llm_with_hotel_structured_output

    response = hotel_chain.invoke({"user_query" : user_query})

    final_result = tavily_search_tool.invoke({"search_query" : response.search_query})

    llm_answer = llm_model.invoke([
        HumanMessage(content=f"Summarize the following hotel details in a human-readable format:\n\n{final_result}")
    ])

    return{
        "hotel_result" : final_result,
        "messages" : [llm_answer]
    }

# test_state = graph_schema(
#     user_query = "I need to travel to Banglore form Delhi. Find hotels near Tin Factory in Banglore under 5000 INR per night.",
#     messages = [],
#     flight_result = [],
#     hotel_result = "",
#     itinerary_result = ""
# )

# result = hotel_agent_node(test_state)
# print(result["hotel_result"])

