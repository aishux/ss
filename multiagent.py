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
  
