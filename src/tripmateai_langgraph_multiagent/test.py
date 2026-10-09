from tripmateai_langgraph_multiagent.graph_excute import run_tripMate_agent

final_response = run_tripMate_agent(
    user_query="Find the cheapest flight from Delhi to Banglore and 2 nights hotel stay and 2 days I want to explore the tourist spot near banglore",
    thread_id="test_user"
    )

print(final_response)