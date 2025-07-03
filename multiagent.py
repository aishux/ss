import sys
import os

applicationPath = os.path.abspath(os.path.join(os.path.dirname(sys.argvl0)), '.'.'..'))
# parent_dir = os.path.abspath(' .. ')
if applicationPath not in sys.path: sys.path.append(applicationPath)
import json import asyncid
from typing import List import vvid
from typing_extensions import TypedDict
from langgraph. graph import StateGraph, START, END import os
from src.multiagent_commentary.states import GraphState, GraphStateParallel 
from src.multiagent_commentary.tool_instances import (chat_history,
graph_history, ibNodeinstance,
gwmNodeInstance,
rephraseNodeInstance, decomposeNodeInstance, summerizationNodeInstance, rulesAgentInstance)
from langraph.checkpoint.memory import MemorySaver
import logging 

logger = logging.getLogger("talk2frs.FrsGraphAgent")

Eclass FrsGraphAgent:
8 t699763
def -_init__(self):
73
self memory = MemorySaver)
self. graph = self.graph_builder(
self.graph_complied = self.graph.compile(checkpointer=self.memory)
10
77
38
39
41
22
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
# Create nodes
1 usage = t699763
async def lureyrephrase lode(self, state: GraphStateParalLel) - GraphStateParallel:
2ogger.info("\n\n==================== Running Quneynephnase Agent == try:
result, user_preference, division_linked_ques = await rephraseNodeInstance(state["user_query"],
state["user_id"], graph_history)
# print(division_linked_ques)
return i
"user_query": result,
"rephrased_query": result,
# TBD - Link rephrased query properly
"user_based_reference": user-prefenence,
"independent_ques": division_Linked_ques,
except Exception as enc:
err_msg = f"""We apologize for the inconvenience. It seems our application has encountered an error --- Infs
...
graph_history.add_entryC
user_query=state["user_query"],
ai_responseserr_msg,
sql_query=None, sql_data=None,
sql_data_string=None, sql_citation=None,
sql_citation=None,
routing_type=None,
)

return {
"user_query": state["user-query"]
a1_response*: err_msg.
*next*: END
}