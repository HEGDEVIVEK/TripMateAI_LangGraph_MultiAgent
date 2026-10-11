from langgraph.checkpoint.postgres import PostgresSaver
from tripmateai_langgraph_multiagent.database import get_postgres_conn


def get_saved_threads():
    conn = get_postgres_conn()

    try:
        checkpointer = PostgresSaver(conn)
        all_threads = {}

        for saved in checkpointer.list(None):
            config = saved.config["configurable"]
            print(saved)

            if config.get("checkpoint_ns", "") != "":
                continue

            thread_id = config["thread_id"]

            if thread_id in all_threads:
                continue

            all_threads[thread_id] = saved.checkpoint.get(
                "channel_values", {}
            )

        return all_threads

    finally:
        conn.close()