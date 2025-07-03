import sys
import os

applicationPath = os.path.abspath(os.path.join(os.path.dirname(sys.argvl0)), '.'.'..'))
# parent_dir = os.path.abspath(' .. ')
if applicationPath not in sys.path: 
 sys.path.append(applicationPath)
import json 
import asyncio
from typing import List 
import vvid
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END 
import os
from src.multiagent_commentary.states import GraphState, GraphStateParallel 
from src.multiagent_commentary.tool_instances import (chat_history, graph_history, ibNodeinstance, gwmNodeInstance, rephraseNodeInstance, decomposeNodeInstance, summerizationNodeInstance, rulesAgentInstance)
from langraph.checkpoint.memory import MemorySaver
import logging 

logger = logging.getLogger("talk2frs.FrsGraphAgent")

class FrsGraphAgent:
  def __init__(self):
    self.memory = MemorySaver)
    self.graph = self.graph_builder()
    self.graph_complied = self.graph.compile(checkpointer=self.memory)

  async def Queryphrase_Node(self, state: GraphStateParalLel) -> GraphStateParallel:
    logger.info("\n\n==================== Running Queryphrase Agent ====================") 
    try:
       result, user_preference, division_linked_ques = await rephraseNodeInstance(state["user_query"], state["user_id"], graph_history)
       # print(division_linked_ques)
       return {
       "user_query": result,
       "rephrased_query": result, # TBD - Link rephrased query properly
       "user_based_reference": user_prefenence,
       "independent_ques": division_linked_ques,
       }
    except Exception as err:
      err_msg = f"""We apologize for the inconvenience. It seems our application has encountered an error"""
      graph_history.add_entry(
      user_query=state["user_query"],
      ai_response = err_msg,
      sql_query=None, 
      sql_data=None,
      sql_data_string=None, 
      sql_citation=None,
      routing_type=None,
     )
  
    return {
     "user_query": state["user_query"],
     "ai_response": err_msg,
     "next": END
    }

  async def Decompose_Node(self, state: GraphStateParalLel) -> GraphStateParallel:

  async def Router_Node(self, state: GraphStateParalLel) -> GraphStateParallel:

  async def ibNode(self, state: GraphStateParalLel) -> GraphStateParallel:

  async def gwmNode(self, state: GraphStateParalLel) -> GraphStateParallel:

  async def summerizationNode(self, state: GraphStateParalLel) -> GraphStateParallel:

  async def business_division_parrallel_router(self, state: GraphStateParalLel) -> GraphStateParallel:

  
def graph_builder(self) -> GraphStateParallel:
## Parallel execution
graph_builder = StateGraph(GraphStateParallel)
graph_builder.add_node("Querynephnase", self. Qureyrephrase_Node)
graph_builder.add_node("Decompose", self.Decompose_Node) graph_builder.add_node("Router_Node", self.Router _Node)
graph_builder.add_node("ibFrsBot"
, self. ibNode)
graph_builder.add_node("gwmFrsBot", self. gwmNode)
graph_builder. add_node ("Summenization", self. summerization_Node)
# Error handling
graph_builder. add_edge(START, end key: "Querynephrase")
# graph_builder. add_edge("Querynephnase", "Decompose")
graph_builder.add_conditional_edges( source "Querynephnase". Lambda state: state.get("next", "Decompose*)) graph_builder.add_conditional_edges( source: "Decompose", Lambda state: state.get("next", "Router _Node"))
graph_builder.add_conditional_edges( source: "Router_Node"
self.business_division_parallel_router,
path_map: {
"Investment Banking": "ibFrsBot"
"Global Wealth Management": "gwmFrsBot",
"Summerization": "Summenization".
"END": END
)
graph_builder.add_edge( start_key: "ibFrsBot'
end_key;
"Summenization")
graph_builder, add_edge( start_key: 'gwmFrsBot'
•end_ key:
"Summerization")
graph_builder.add_edge ( start.key:
"Summenization"
• END)
return graph_builder

async def run(self, user_question, user_id=None):
#
computed_thread_id_tmp = "'-join(str(ord(st)) for st in user_id)
computed_thread_id_tmp = f"{user_id}::{uuid.Uid4O}*
print("computed temp thread_id", computed_thread_id_tmp)
input_data = t
"user_query": user_question,
"user_id": user_id
}
initial_state = GraphStateParallel(user_query-user-question, user_id=user_id)
config = 1
"configurable" : {
"thread_id": computed_thread_id_tmp
}
result = await self.graph_complied.ainvoke(initial_state, config)
# print("Final result", result)
return result

Fif -_name__ == "__main__":
agent_obj = FrsGraphAgent)
while True:
try:
user_input = input("\n\nUser: ")
user_email = input("\nEmail: *)
if user_input. lower() in ["quit", "exit", "q"]:
print ("Goodbye!")
break
# graphResult = asyncio.run(agent_obj.run(user_input, "miguel.mendes-pena@ubs.com*))
graphResult = asyncio.run(agent_obj.run(user_input, user_email))
# print(" --- History ----", graph_history -messages[-1])
print("User Query:")
print(graphResult["user_query"] if graphResult.get("user_query") else **)
print("\n")
print("SQL Query:")
print(graphResult["sql_query"] if graphResult.get("sql_query") else **)
print("\n")
print("AI response:")
print(graphResult["ai_response"] if graphResult,get("ai_response") else "*)

except Exception as err:
print("Error occurred----import traceback
print(traceback. print_exc()
break
  














'''
async def Decompose Mode(self, state: GraphStateParallel) -> GraphStateParallel:
Logger.info("\n\n========
=ssess Running Decompose Agent ====sssssessestessss)
try:
decomposed_question = await decomposeNodeInstance(state[*rephrased_query*],
statel user_based_reference"]["business_division_access*])
decomposed_question_formatted = json.dumps (decomposed_question, indent=4)
logger.info(f" Rephrased query was decomposed as below ...- \n {decomposed_question_formatted}*) if decomposed_question == (}:
return {**state}
any (keyDiv. lower()
err_msg = "•
== "clarification_needed". lower() for keyDiv in decomposed_question):
keyDiv in decomposed_ question:
if keyDiv. lower() = clarification_needed".Lower():
err_msg = decomposed_ question [keyDiv]
raise Exception(err_msg)
elif all(len(val) == 0
raise
Exception(
for keyDiv, val in decomposed_question.items()):
"We were not
able to break down the question properly to trigger subsequent agents which could be due to incorrect measure name provided in the user question.")
eLse:
return {
"independent_ques": {div: ques for div, ques in decomposed_question.items() if
(div not in ["dependent", "clarification_needed"])},
"dependent_ques": {div: ques for div, ques in decomposed_question.items() if (div == 'dependent')}
except Exception as err:
err_msg = f***We apologize for the inconvenience. It seems
graph_history.add_entryC
user _query=statel*user_query"], ai_response=err_msg,
sql_query=None, sql_data=None,
sql_data_string=None, sql_citation=None, routing_type=None,
I
return {
"user-query": statel "user _query"],
"ai_response": err_msg,
"next": END
}
'''
  
