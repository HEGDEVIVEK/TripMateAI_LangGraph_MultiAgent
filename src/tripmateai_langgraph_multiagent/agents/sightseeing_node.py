import os
from dotenv import load_dotenv
load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("bro it is working")

from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from tripmateai_langgraph_multiagent.tools.tavily_tool import tavily_search_tool
from tripmateai_langgraph_multiagent.graphSchema import graph_schema

llm_model = init_chat_model(model="gpt-5-nano")

class llm_sightseeing_schema(BaseModel):
    search_query: str | None = Field(
        description=(
            "A search query for sightseeing attractions at the destination. "
            "Include the destination, user interests, and travel dates "
            "when provided. Search for opening hours, closed days, "
            "official websites, and ticket booking information. "
            "Return null if the destination is missing or ambiguous."
        )
    )   
llm_with_sightseeing_output = llm_model.with_structured_output(llm_sightseeing_schema)

def sightseeing_agent_node(state : graph_schema):

    user_query = state["user_query"]

    sightseeing_prompt = ChatPromptTemplate.from_messages([
        (
        "system",
        "Create a concise web search query for sightseeing attractions. "
        "Use the destination city, not the departure city. "
        "Include the user's sightseeing interests. "
        "Search for official attraction websites, opening hours, "
        "closed days, and entry tickets. "
        "Do not name specific attractions unless the user names them. "
        "Exclude hotel searches and accommodation budgets. "
        "Do not write instructions such as 'provide details' or "
        "'create an itinerary' inside the search query. "
        "Do not invent missing preferences or dates. "
        "Return null for search_query if the destination is unclear."
        ),
        ("human", "{user_query}")
    ])

    sightseeing_chain = sightseeing_prompt | llm_with_sightseeing_output

    response = sightseeing_chain.invoke({"user_query" : user_query})

    final_result = tavily_search_tool.invoke({"search_query" : response.search_query})

    llm_answer = llm_model.invoke([
        HumanMessage(content=f"Summarize the following sightseeing details in a human-readable format:\n\n{final_result}")
    ])

    return{
        "sightseeing_result" : final_result,
        "messages" : [llm_answer]
    }

# test_state = {
#     "user_query": "I need to travel to Banglore form Delhi. Find hotels near Tin Factory in Banglore under 5000 INR per night.",
#     "messages": [],
#     "flight_result": [],
#     "hotel_result": "",
#     "sightseeing_result": [],
#     "itinerary": "",
# }
# result = sightseeing_agent_node(test_state)
# print(result["sightseeing_result"])

