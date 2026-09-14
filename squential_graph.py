from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import display, Image

class State(TypedDict):
    current: str
    cleaned: str
    title_case: str
    final: str

def clean_node(state:State)-> dict:
    cleaned=state["current"].strip().lower()
    print(f"[clean]      '{state['current']}' → '{cleaned}'")
    return {"cleaned": cleaned,"current": cleaned}

def titlecase_node(state:State)-> dict:
    title=state["current"].title()
    print(f"[title_case]      '{state['current']}' → '{title}'")
    return {"title_case":title,"current":title}

def format_node(state:State)-> dict:
    final="Result: "+state["current"]
    print(f"[format]      '{state['current']}' → '{final}'")
    return {"final": final,"current":final}

builder=StateGraph(State)

builder.add_node("clean",clean_node)
builder.add_node("titlecase",titlecase_node)
builder.add_node("format",format_node)

builder.add_edge(START,"clean")
builder.add_edge("clean","titlecase")
builder.add_edge("titlecase","format")
builder.add_edge("format",END)

graph=builder.compile()
png_bytes = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png_bytes)

inputs=[
    " I am Subhadip ",
    " Building AI agent "
]

for raw in inputs:
    r=graph.invoke({
    "current": raw,
    "cleaned": "",
    "title_case": "",
    "final":""
    }
)

print(f"Output: {r['final']}\n")




