from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class graph_schema(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_query: str
    flight_result: str
    hotel_result: str
    weather_result: str
    sightseeing_result: str
    itinerary_result: str