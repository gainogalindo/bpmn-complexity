# PM4Py - Objects
from pm4py.objects.bpmn.obj import BPMN

# Auxiliary functions for BPMN

# Get Outgoing Flows (BPMN Node)
def get_outgoing_flows_bpmn(bpmn: BPMN, node_id: str):
    return [f for f in bpmn.get_flows() if f.source.id == node_id]
#enddef

# Get Incoming Flows (BPMN Node)
def get_incoming_flows_bpmn(bpmn: BPMN, node_id: str):
    return [f for f in bpmn.get_flows() if f.target.id == node_id]
#enddef