from pydantic import conset
import os
from dotenv import load_dotenv
load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("bro it is working")

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from tripmateai_langgraph_multiagent.tools.flight_tool import aviationStack_tool
from tripmateai_langgraph_multiagent.graphSchema import graph_schema

llm_model = init_chat_model(model="gpt-5-nano")


class llm_aviation_schema(BaseModel):
    dep_iata : str | None = Field(
        description="Departure airport code: exactly 3 uppercase letters, such as BLR. Return null if missing or ambiguous.",
        pattern=r"^[A-Z]{3}$"
    )

    arr_iata : str | None = Field(
        description="Arrival airport code: exactly 3 uppercase letters, such as DEL. Return null if missing or ambiguous.",
        pattern=r"^[A-Z]{3}$"
    )

    limit : int = Field(
        default=2,
        ge=1,
        le=10,
        description="Maximum flight records to return. Use 2 if unspecified."
    )
llm_with_aviation_structured_output = llm_model.with_structured_output(llm_aviation_schema)

def aviation_agent_node(state: graph_schema):

    user_query = state["user_query"]

    aviation_prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract the departure airport, arrival airport, and limit."
        "Convert unambiguous city names to airport IATA codes."
        "Return null for missing or ambiguous airports."
        "Use a limit of 2 unless specified; keep it between 1 and 10."),
        ("human", "{user_query}"),
    ])

    aviation_chain = aviation_prompt | llm_with_aviation_structured_output

    response = aviation_chain.invoke({"user_query" : user_query})

    final_result = aviationStack_tool.invoke({
        "dep_iata" : response.dep_iata,
        "arr_iata" : response.arr_iata,
        "limit" : response.limit
    })

    llm_answer = llm_model.invoke([
        HumanMessage(content=f"Summarize the following flight details in a human-readable format:\n\n{final_result}")
    ])

    return{
        "flight_result" : final_result,
        "messages" : [llm_answer]
    }


# test_state = {
#     "user_query": "I need to travel to Banglore form Delhi. Find hotels near Tin Factory in Banglore under 5000 INR per night.",
#     "messages": [],
#     "flight_result": [],
#     "hotel_result": "",
#     "itinerary": "",
# }
# result = aviation_agent_node(test_state)
# print(result["flight_result"])
