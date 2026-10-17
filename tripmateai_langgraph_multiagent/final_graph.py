from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from tripmateai_langgraph_multiagent.graph_schema import graph_schema

from tripmateai_langgraph_multiagent.agents.guardrail_node import guadrail_agent_node
from tripmateai_langgraph_multiagent.agents.supervisor_node import supervisor_agent_node
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

def route_after_guadrails(state:graph_schema):
    if state["guardrail_allowed"] == "allow":
        return "supervisor_agent_node"
    else:
        return END

def route_after_supervisor(state:graph_schema):
    selected_agents = state["selected_agents"]

    if selected_agents:
        return selected_agents
    else:
        return "itinerary_agent_node"


graph = StateGraph(graph_schema)

graph.add_node("guadrail_agent_node", guadrail_agent_node)
graph.add_node("supervisor_agent_node", supervisor_agent_node)
graph.add_node("aviation_agent_node", aviation_agent_node)
graph.add_node("hotel_agent_node", hotel_agent_node)
graph.add_node("sightseeing_agent_node", sightseeing_agent_node)
graph.add_node("weather_agent_node", weather_agent_node)
graph.add_node("itinerary_agent_node", itinerary_agent_node)

graph.add_edge(START, "guadrail_agent_node")

graph.add_conditional_edges( 
    "guadrail_agent_node", 
    route_after_guadrails, 
    {
        "supervisor_agent_node": "supervisor_agent_node", 
        END: END
    }
 )

graph.add_conditional_edges(
    "supervisor_agent_node", 
    route_after_supervisor, 
    {
        "aviation_agent_node": "aviation_agent_node",
        "hotel_agent_node": "hotel_agent_node",
        "sightseeing_agent_node": "sightseeing_agent_node",
        "weather_agent_node": "weather_agent_node",
        "itinerary_agent_node": "itinerary_agent_node",
    }
)

graph.add_edge("aviation_agent_node", "itinerary_agent_node")
graph.add_edge("hotel_agent_node", "itinerary_agent_node")
graph.add_edge("sightseeing_agent_node", "itinerary_agent_node")
graph.add_edge("weather_agent_node", "itinerary_agent_node")

graph.add_edge("itinerary_agent_node", END)

final_graph = graph.compile(checkpointer=mongodb_checkpointer)

final_graph.get_graph().draw_mermaid_png(output_file_path="tripmate_ai_graph.png")