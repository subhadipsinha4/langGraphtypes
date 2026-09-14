from typing import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

class MyState(TypedDict):
    number: int
    category: str
    result: str

def classify_node(state:MyState)-> dict:
    n=state["number"]
    if n<0:
        category="negative"
    elif n==0:
        category="zero"
    elif n%2==0:
        category="even"
    else:
        category="odd"
    print(f"[classify] {n}-> {category}")
    return {"category":category}

def negative_node(state:MyState)->dict:
    return {"result":f"{state['number']} is a negative value"}

def zero_node(state: MyState)-> dict:
    return {"result":f"{state['number']} is a zero value"}

def even_node(state:MyState)-> dict:
    return {"result":f"{state['number']} is a even value"}

def odd_node(state: MyState)-> dict:
    return {"result":f"{state['number']} is a odd value"}

def route_by_category(state: MyState)-> Literal["negative","zero","even","odd"]:
    return state["category"]

builder=StateGraph(MyState)
builder.add_node("classify",classify_node)
builder.add_node("negative",negative_node)
builder.add_node("zero",zero_node)
builder.add_node("even",even_node)
builder.add_node("odd",odd_node)

builder.add_edge(START,"classify")

builder.add_conditional_edges("classify",route_by_category,{
        "negative": "negative",
        "zero": "zero",
        "even": "even",
        "odd": "odd",
    },)

for branch in ["negative", "zero", "even", "odd"]:
    builder.add_edge(branch, END)

graph = builder.compile()
png_bytes = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png_bytes)

for num in [-6,0,1,5,2]:
    r=graph.invoke(
        {
        "number": num,
        "category": "",
        "result": ""
        }
    )






