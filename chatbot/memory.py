from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from .config import DATABASE_URL
from .graph import graph

chatbot = None

async def init_chatbot():

    global chatbot

    saver_cm = AsyncPostgresSaver.from_conn_string(DATABASE_URL)

    saver = await saver_cm.__aenter__()

    await saver.setup()

    chatbot = graph.compile(checkpointer=saver)

    print("✅ AsyncPostgresSaver initialized")

    return saver_cm
