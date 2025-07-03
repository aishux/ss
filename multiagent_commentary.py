import sys
import os
import json
import asyncio
import uuid
import logging

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.multiagent_commentary.states import GraphStateParallel
from src.multiagent_commentary.tool_instances import (
    rulesAgentInstance, ibNodeInstance, summerizationNodeInstance
)

logger = logging.getLogger("CommentaryAgent")

class FrsGraphAgent:
    def __init__(self):
        self.memory = MemorySaver()
        self.graph = self.graph_builder()
        self.graph_compiled = self.graph.compile(checkpointer=self.memory)

    async def RulesInterpretation_Node(self, state: GraphStateParallel) -> GraphStateParallel:
        logger.info("=== Running Rules Interpretation ===")
        try:
            rules = await rulesAgentInstance(state["user_query"], state["user_id"])
            return {**state, "rules": rules}
        except Exception as e:
            logger.error(f"Rules agent failed: {e}")
            return {**state, "ai_response": "Error in rules interpretation", "next": END}

    async def IB_Node(self, state: GraphStateParallel) -> GraphStateParallel:
        logger.info("=== Running IB Agent ===")
        try:
            ib_results = await ibNodeInstance(state["rules"], state["user_id"])
            return {**state, "ib_results": ib_results}
        except Exception as e:
            logger.error(f"IB agent failed: {e}")
            return {**state, "ai_response": "Error in IB agent", "next": END}

    async def Summarisation_Node(self, state: GraphStateParallel) -> GraphStateParallel:
        logger.info("=== Running Summarisation Agent ===")
        try:
            final_commentary = await summerizationNodeInstance(state["ib_results"], state["user_query"])
            return {**state, "ai_response": final_commentary}
        except Exception as e:
            logger.error(f"Summarisation failed: {e}")
            return {**state, "ai_response": "Error in summarisation", "next": END}

    def graph_builder(self):
        builder = StateGraph(GraphStateParallel)
        builder.add_node("RulesInterpretation", self.RulesInterpretation_Node)
        builder.add_node("IBAgent", self.IB_Node)
        builder.add_node("Summarisation", self.Summarisation_Node)

        builder.add_edge(START, "RulesInterpretation")
        builder.add_edge("RulesInterpretation", "IBAgent")
        builder.add_edge("IBAgent", "Summarisation")
        builder.add_edge("Summarisation", END)

        return builder

    async def run(self, user_question, user_id=None):
        computed_thread_id = f"{user_id}::{uuid.uuid4()}"
        initial_state = GraphStateParallel(user_query=user_question, user_id=user_id)
        config = {
            "configurable": {
                "thread_id": computed_thread_id
            }
        }
        result = await self.graph_compiled.ainvoke(initial_state, config)
        return result


if __name__ == "__main__":
    agent = FrsGraphAgent()
    while True:
        try:
            user_input = input("\nUser: ")
            user_email = input("Email: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
            result = asyncio.run(agent.run(user_input, user_email))
            print("\n=== Final Output ===")
            print("User Query:", result.get("user_query", ""))
            print("Rules:", result.get("rules", ""))
            print("IB Results:", result.get("ib_results", ""))
            print("Final Commentary:", result.get("ai_response", ""))
        except Exception as e:
            print(f"Error occurred: {e}")
            break
