from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END

class MyState(TypedDict):
    password: str
    is_valid: bool

def password_check_node(state: MyState)-> dict:
    p=state["password"]
    if p.__len__()>=8 and ("@" in p or "#" in p):
        is_valid=True
    else:
        is_valid=False
    return {"password":p, "is_valid":is_valid}

def valid_node(state:MyState)-> dict:
    return {"password": state["password"], "is_valid": True}

def invalid_node(state:MyState)-> dict:
    return {"password": state["password"], "is_valid": False}

def route_password_condition(state:MyState)-> Literal["valid", "invalid"]:
    if state["is_valid"]:
        return "valid"
    else:
        return "invalid"

builder=StateGraph(MyState)
builder.add_node("password_check", password_check_node)
builder.add_node("valid", valid_node)
builder.add_node("invalid", invalid_node)


builder.add_edge(START, "password_check")
builder.add_conditional_edges("password_check", route_password_condition,{
    "valid": "valid",
    "invalid": "invalid"
},)

graph=builder.compile()
png_bytes = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png_bytes)


result = graph.invoke({
    "password": "mypassword.123",
    "is_valid": False,
})

print(f"{result} -> {result['is_valid']}")


       