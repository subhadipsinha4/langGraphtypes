from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ============================================================
# 1. STATE
# ============================================================

class MyState(TypedDict):
    name: str
    greeting: str
    farewell: str


# ============================================================
# 2. NODES
# ============================================================

def name_node(state: MyState) -> dict:
    name= f"Mr. {state['name']}"
    return {"name": name}

def greet_node(state: MyState) -> dict:
    greeting = f"Hello, {state['name']}! Welcome to LangGraph. 👋"

    print(f"[greet_node] {greeting}")

    return {"greeting": greeting}


def farewell_node(state: MyState) -> dict:
    farewell = f"Goodbye, {state['name']}! See you next time. 🙌"

    print(f"[farewell_node] {farewell}")

    return {"farewell": farewell}


# ============================================================
# 3. CREATE STATE GRAPH
# ============================================================

builder = StateGraph(MyState)


# ============================================================
# 4. ADD NODES
# ============================================================

builder.add_node("greet", greet_node)
builder.add_node("farewell", farewell_node)
builder.add_node("name",name_node)


# ============================================================
# 5. ADD EDGES
# ============================================================

builder.add_edge(START, "name")
builder.add_edge("name","greet")
builder.add_edge("greet", "farewell")
builder.add_edge("farewell", END)


# ============================================================
# 6. COMPILE GRAPH
# ============================================================

graph = builder.compile()


# ============================================================
# 7. CREATE GRAPH VISUALIZATION
# ============================================================

png_bytes = graph.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(png_bytes)

print("\n✅ Graph visualization saved as graph.png")


# ============================================================
# 8. RUN GRAPH
# ============================================================

result = graph.invoke(
    {
        "name": "Yash",
        "greeting": "",
        "farewell": "",
    }
)


# ============================================================
# 9. DISPLAY RESULT
# ============================================================

print("\n✅ Final State:")

print(f"  name: {result['name']}")
print(f"  greeting : {result['greeting']}")
print(f"  farewell : {result['farewell']}")

print("\n✅ Complete Result")

print(result)