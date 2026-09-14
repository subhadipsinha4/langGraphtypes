from typing import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START,END 

class MyState(TypedDict):
    username: str
    password: str
    message: str
    is_authenticated: bool
    attempts: int

def login_node(state:MyState) -> dict:
    state["attempts"] += 1
    if state["username"]=="admin" and state["password"]=="admin":
        return {"username": state["username"],"password": state["password"],"message": "Login successful", "is_authenticated": True,"attempts": state["attempts"]}
    else:
        return {"username": state["username"],"password": state["password"],"message": "Invalid credentials", "is_authenticated": False,"attempts": state["attempts"]}

def should_continue_node(state:MyState) -> Literal["retry", "_end_"]:
    if state["is_authenticated"]:
        return "_end_"
    elif state["attempts"] >= 3:
        state["message"]="Max limit reached"
        return "_end_"
    else:
        return "retry"

builder=StateGraph(MyState)
builder.add_node("login",login_node)

builder.add_edge(START,"login")
builder.add_conditional_edges("login",should_continue_node,{
    "retry": "login",
    "_end_": END
})

graph=builder.compile()
    
for auth in ["ads","adddd","admin"]:
    r=graph.invoke({
        "username": auth,
        "password": auth,
        "message": "",
        "is_authenticated": False,
        "attempts": 0
    })
    print(f"Result for user {auth}: {r}")



    
