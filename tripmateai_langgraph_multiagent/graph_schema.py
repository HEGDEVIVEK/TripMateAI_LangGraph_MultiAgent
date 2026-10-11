from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class graph_schema(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_query: str
    flight_result: list[dict]
    hotel_result: str
    sightseeing_result: str
    itinerary_result: str