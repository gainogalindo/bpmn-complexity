# PM4Py - Objects
from pm4py.objects.bpmn.obj import BPMN

# Other Python Libraries
import math

# Simplicity Utils
from bpmn_complexity import utils


def compute_cfc(bpmn: BPMN) -> int:
    """Calculates the Control-Flow Complexity (CFC) of a BPMN model.

    Args:
        bpmn (BPMN): The BPMN model to analyze.

    Returns:
        int: The Control-Flow Complexity score.

    References:
        - Cardoso, J. (2005). Control-flow Complexity Measurement of Processes
          and Weyuker’s Properties.
        - McCabe, T. J. (1976). A Complexity Measure.
    """
    cfc_value = 0

    for node in bpmn.get_nodes():
        if isinstance(node, (BPMN.ExclusiveGateway, BPMN.EventBasedGateway, BPMN.InclusiveGateway, BPMN.ParallelGateway)):
            outgoing_edges = utils.get_outgoing_flows_bpmn(bpmn, node.id)
            num_outgoing = len(outgoing_edges)

            if num_outgoing > 1:
                if isinstance(node, (BPMN.ExclusiveGateway, BPMN.EventBasedGateway)):
                    cfc_value += num_outgoing
                elif isinstance(node, BPMN.InclusiveGateway):
                    cfc_value += int(math.pow(2, num_outgoing) - 1)
                elif isinstance(node, BPMN.ParallelGateway):
                    cfc_value += 1
                #endif
            #endif
        #endif
    #endfor

    return cfc_value
#enddef