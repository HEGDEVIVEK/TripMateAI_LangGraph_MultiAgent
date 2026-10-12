from langgraph.checkpoint.postgres import PostgresSaver
from tripmateai_langgraph_multiagent.database import get_postgres_conn
from langgraph.checkpoint.mongodb import MongoDBSaver
from tripmateai_langgraph_multiagent.database import get_mongodb_client


def get_saved_all_chats_postgres():
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


def get_saved_chat_with_thread_id(thread_id):
    conn = get_postgres_conn()
    config = {
        "configurable": {
            "thread_id": thread_id,
            "checkpoint_ns": "",
        }
    }

    try:
        checkpointer = PostgresSaver(conn)
        saved = checkpointer.get_tuple(config)

        return saved.checkpoint.get(
            "channel_values", {}
        )

    finally:
        conn.close()


def get_saved_all_chats_mongodb():
    mongodb_client = get_mongodb_client()

    try:
        checkpointer = MongoDBSaver(mongodb_client, db_name="tripMateAiDb")
        all_threads = {}

        for saved in checkpointer.list(None):
            config = saved.config["configurable"]

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
        mongodb_client.close()