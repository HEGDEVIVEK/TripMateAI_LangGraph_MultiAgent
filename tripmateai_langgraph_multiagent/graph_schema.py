from typing import Annotated, TypedDict, Any
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class graph_schema(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_query: str

    # Gaudrail state
    guardrail_allowed: str             #Whether the user query is allowed or not
    guardrail_reason: str               #Reason for the gaudrail state

    # Supervisor state
    selected_agents: list[str]          #List of agents selected by the supervisor based on the user query
    supervisor_reasoning: str           #Why those agents are selected based on the user query
    
    # Agent result state
    flight_result: str                  #Result of the flight agent
    hotel_result: str                   #Result of the hotel agent
    weather_result: str                 #Result of the weather agent
    sightseeing_result: str             #Result of the sightseeing agent
    itinerary_result: str               #Result of the itinerary agent
    budget_result: str                  #Result of the budget agent

    #Human-in-the-Loop state
    approval_request: bool              #Whether the human approval is requested or not
    approved : bool                     #Whether the human approved the result or not
    human_feedback: str                 #Human feedback on the result
    