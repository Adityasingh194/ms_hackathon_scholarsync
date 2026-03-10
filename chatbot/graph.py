from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from .state import ChatState
from .llm import llm_with_tools, SYSTEM_PROMPT
from .mcp_client import get_mcp_tools


# ---------------- Agent Node ----------------
async def chat_node(state: ChatState):

    # Limit memory to prevent token overflow
    messages = [SYSTEM_PROMPT] + state["messages"][-8:]

    response = await llm_with_tools.ainvoke(messages)

    return {
        "messages": [response]
    }


# ---------------- Build Graph ----------------
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)


# Load tools from MCP server
tools = get_mcp_tools()

tool_node = ToolNode(tools)

graph.add_node("tools", tool_node)


# Entry
graph.add_edge(START, "chat_node")


# Tool routing
graph.add_conditional_edges(
    "chat_node",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END,
    }
)


# Tool → back to agent
graph.add_edge("tools", "chat_node")