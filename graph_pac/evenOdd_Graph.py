from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START,END 


class State(TypedDict):
    number: int
    category: str

def evenOdd_node(state:State)-> dict:
    n=state["number"]
    if(n%2==0):
        category="even"
    else:
        category="odd"
    return {"number":n, "category":category}

def even_node(state:State)->dict:
    return {"number":state["number"], "category":"this is a even number"}

def odd_node(state:State)->dict:
    return {"number":state["number"], "category":"this is a odd number"}

def route_by_category(state:State)->Literal["even","odd"]:
    return state["category"]

builder=StateGraph(State)
builder.add_node("evenOdd",evenOdd_node)
builder.add_node("even",even_node)
builder.add_node("odd",odd_node)

builder.add_edge(START,"evenOdd")
builder.add_edge("evenOdd",END)
builder.add_conditional_edges("evenOdd",route_by_category,{
    "even":"even",
    "odd":"odd",
},)

graph=builder.compile()
png_bytes = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png_bytes)

for num in [7,2,3,4]:
    r=graph.invoke({
        "number":num,
        "category":""
    })

    print(f"Result: {r}-> {r['category']}\n")







    

