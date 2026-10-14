from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from tripmateai_langgraph_multiagent.graph_schema import graph_schema

from tripmateai_langgraph_multiagent.agents.aviation_node import aviation_agent_node
from tripmateai_langgraph_multiagent.agents.hotel_node import hotel_agent_node
from tripmateai_langgraph_multiagent.agents.sightseeing_node import sightseeing_agent_node
from tripmateai_langgraph_multiagent.agents.itinerary_node import itinerary_agent_node
from tripmateai_langgraph_multiagent.agents.weather_node import weather_agent_node

from tripmateai_langgraph_multiagent.database import get_postgres_conn
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.mongodb import MongoDBSaver
from tripmateai_langgraph_multiagent.database import get_mongodb_client

# conn = get_postgres_conn()
# checkpointer = PostgresSaver(conn)
# checkpointer.setup()

mongodb_client = get_mongodb_client()
mongodb_checkpointer = MongoDBSaver(mongodb_client, db_name="tripMateAiDb")

graph = StateGraph(graph_schema)

graph.add_node("aviation_agent_node", aviation_agent_node)
graph.add_node("hotel_agent_node", hotel_agent_node)
graph.add_node("sightseeing_agent_node", sightseeing_agent_node)
graph.add_node("weather_agent_node", weather_agent_node)
graph.add_node("itinerary_agent_node", itinerary_agent_node)

graph.add_edge(START, "aviation_agent_node")
graph.add_edge(START, "hotel_agent_node")
graph.add_edge(START, "sightseeing_agent_node")
graph.add_edge(START, "weather_agent_node")

graph.add_edge(["aviation_agent_node", "hotel_agent_node", "sightseeing_agent_node", "weather_agent_node"], "itinerary_agent_node")
graph.add_edge("itinerary_agent_node", END)

final_graph = graph.compile(checkpointer=mongodb_checkpointer)