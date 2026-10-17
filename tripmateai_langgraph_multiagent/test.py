from langchain_core.messages import HumanMessage, AIMessage
from tripmateai_langgraph_multiagent.agents.hotel_node import hotel_agent_node
from tripmateai_langgraph_multiagent.agents.aviation_node import aviation_agent_node

'''
hotel_agent_node({
    "messages": [
        HumanMessage(
            content="Hotels in Sirsi under 3000 rupees."
        ),
        AIMessage(
            content="""
Previously suggested options in Sirsi:
- Captain's Camp: indicative price from ₹2,368/night;
  parking was listed.
- Hotel Supriya International: indicative listings around
  ₹1,465–₹3,000/night.
- Ashwini Hotel & Lodging: parking was listed, but the price
  was not verified.

These were search-based suggestions, not confirmed prices
or availability. Travel dates and guest count were not provided.
"""
        ),
        HumanMessage(
            content=(
                "I don't like Hotel Supriya International."
            )
        ),
    ]
})
'''

aviation_agent_node({
    "messages": [
        HumanMessage(content="Flights from Bangalore to Delhi"),

        AIMessage(
            content=(
                "Flights from Bangalore (BLR) to Delhi (DEL):\n"
                "- IndiGo 869: departure October 17, 2026 at "
                "18:40 IST; arrival 21:35 IST. Status: scheduled.\n"
                "- Akasa Air 1821: departure October 17, 2026 at "
                "18:35 IST; arrival 21:30 IST. Status: scheduled."
            ),
            name="itinerary_node",
        ),

        HumanMessage(content="I will travel from Chennai."),
    ]
})