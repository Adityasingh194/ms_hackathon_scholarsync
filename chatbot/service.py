from langchain_core.messages import HumanMessage
from langsmith import traceable
from langchain_core.tracers.context import tracing_v2_enabled

from . import memory
from .config import threads


@traceable(name="ScholarSync Chat")
async def chat_stream(user_message: str, thread_id: str):

    if thread_id not in threads:
        threads[thread_id] = user_message[:30]

    state = {
        "messages": [HumanMessage(content=user_message)]
    }

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    with tracing_v2_enabled(project_name="ScholarSync"):

        async for event in memory.chatbot.astream_events(
            state,
            config=config
        ):

            # Stream tokens ONLY (prevents duplication)
            if event["event"] == "on_chat_model_stream":

                chunk = event["data"]["chunk"]

                if chunk.content:
                    yield chunk.content