import os
from dotenv import load_dotenv
load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("bro it is working")

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_core.prompts import MessagesPlaceholder

from tripmateai_langgraph_multiagent.tools.flight_tool import aviationStack_tool
from tripmateai_langgraph_multiagent.graph_schema import graph_schema

llm_model = init_chat_model(model="gpt-5-nano")


class llm_aviation_schema(BaseModel):
    dep_iata: str | None = Field(
        description=(
            "Departure airport for the current trip, resolved from "
            "the conversation and latest corrections. Preserve an "
            "earlier departure unless changed. Return null only if "
            "unresolved or ambiguous after considering the history."
        ),
        pattern=r"^[A-Z]{3}$",
    )

    arr_iata: str | None = Field(
        description=(
            "Arrival airport for the current trip, resolved from "
            "the conversation and latest corrections. Preserve an "
            "earlier arrival unless changed. Return null only if "
            "unresolved or ambiguous after considering the history."
        ),
        pattern=r"^[A-Z]{3}$",
    )

    limit: int = Field(
        default=2,
        ge=1,
        le=10,
        description=(
            "Maximum flight records. Preserve the previously requested "
            "limit unless changed. Use 2 when no limit was provided."
        ),
    )
llm_with_aviation_structured_output = llm_model.with_structured_output(llm_aviation_schema)

def aviation_agent_node(state : graph_schema):

    history = state["messages"]

    aviation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Resolve the CURRENT flight route from the conversation.

Read the messages chronologically:
1. Identify the user's established departure and arrival.
2. Apply later corrections only to the fields being changed.
3. Preserve fields that the user has not changed.

A field absent from the latest message is NOT missing if it
was established earlier for the same trip.

Interpret "sorry", "actually", and "instead" as corrections
to the existing trip unless the user explicitly starts a new trip.

Examples:
- Earlier: "Flights from Bangalore to Delhi."
  Latest: "Sorry, I will travel from Chennai."
  Result: dep_iata="MAA", arr_iata="DEL", limit=2.

- Earlier: "Flights from Bangalore to Delhi."
  Latest: "Actually, I want to go to Mumbai."
  Result: dep_iata="BLR", arr_iata="BOM", limit=2.

- Latest: "A new trip: flights from Chennai."
  No destination is provided for this new trip.
  Result: dep_iata="MAA", arr_iata=null, limit=2.

Convert unambiguous airport locations to IATA codes.
Do not invent airports or silently substitute another city.
Return null only when a field remains missing or ambiguous
after resolving the relevant conversation.

Preserve an earlier result limit unless changed.
Use 2 if unspecified; keep it between 1 and 10.
"""
    ),
    MessagesPlaceholder(variable_name="history"),
])

    aviation_chain = aviation_prompt | llm_with_aviation_structured_output

    response = aviation_chain.invoke({"history" : history})
    
    if response.dep_iata is None or response.arr_iata is None:
        return {
            "flight_result": (
                "Flight search was not performed because the departure "
                "or arrival airport is missing or ambiguous. "
                "Ask the user to clarify the airports."
            )
        }

    final_result = aviationStack_tool.invoke({
        "dep_iata" : response.dep_iata,
        "arr_iata" : response.arr_iata,
        "limit" : response.limit
    })

    llm_answer = llm_model.invoke([
        HumanMessage(content=f"Summarize the following flight details in a human-readable format:\n\n{final_result}")
    ])

    llm_answer.name = "aviation_node"
    
    return{
        "flight_result" : llm_answer.content,
        "messages" : [llm_answer]
    }

