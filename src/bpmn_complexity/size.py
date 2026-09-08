# PM4Py - Objects
from pm4py.objects.bpmn.obj import BPMN


def compute_size(bpmn: BPMN,) -> int:
    """Calculates the size of a BPMN model.

    Args:
        bpmn (BPMN): The BPMN model to analyze.
        from_petrinet (bool): If BPMN model was generated from a PMP4Py Petri Net.

    Returns:
        int: The total number of nodes in the model.

    References:
        - Mendling, J., et al. (2007). Error Metrics for Business Process Models.
        - Fenton, N. E., & Pfleeger, S. L. (1997). Software Metrics: A Rigorous
          and Practical Approach.
    """
    return len(bpmn.get_nodes())
#enddef