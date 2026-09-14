from typing import TypedDict
from typing import Literal
import random
from langgraph.graph import StateGraph, START,END 

class State(TypedDict):
    target: int
    attempts: int
    guess: int
    passed: bool

def guess_node(state: State)-> dict:
    attempts=state["attempts"]+1
    guess=random.randint(1,5)
    passed=guess==state["target"]
    return {"attempts": attempts,"guess": guess,"passed": passed}

def should_continue(state: State) -> Literal["guess", "__end__"]:
    if state["passed"]:
        print(f"✅ Correct! Found target in {state['attempts']} attempt(s).")
        return END
    if state["attempts"] >= 5:
        print(f"⚠️  Max attempts reached. Stopping.")
        return END
    print(f"🔄 Looping back to try again...")
    return "guess"

builder=StateGraph(State)
builder.add_node(guess_node,"guess_node")
builder.add_edge(START, "guess_node")
builder.add_conditional_edges("guess_node", should_continue,{"guess":"guess_node",END:END},)
graph=builder.compile()

result=graph.invoke(
    {
        "target": 3,
        "attempts": 0,
        "guess": 0,
        "passed": False
    }
)

print(f"\n Final State: guess={result['guess']}, attempts={result['attempts']}, passed={result['passed']}")