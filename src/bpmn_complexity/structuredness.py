# Imports
import jpype
from collections import deque
from pathlib import Path

# PM4Py - Objects
from pm4py.objects.bpmn.obj import BPMN


def compute_structuredness(bpmn:BPMN):
    # Start JVM
    if not jpype.isJVMStarted():
        jar_path = Path(__file__).parent / "lib" / "rpst.jar"

        if not jar_path.exists():
            raise FileNotFoundError(f"RPST JAR not found: {jar_path}")
        #endif

        jpype.startJVM(
            jpype.getDefaultJVMPath(),
            classpath=[str(jar_path)]
        )
    #endif

    # Instantiate objects from JClass
    MultiDirectedGraph = jpype.JClass('org.jbpt.graph.MultiDirectedGraph')
    Vertex = jpype.JClass('org.jbpt.hypergraph.abs.Vertex')
    RPST = jpype.JClass('org.jbpt.algo.tree.rpst.RPST')
    TCType = jpype.JClass('org.jbpt.algo.tree.tctree.TCType')

    # Python dictionaries replace the Java HashMaps
    mapping = {}
    gates = {}

    # Instantiate the Java multi-directed graph via JPype
    graph = MultiDirectedGraph()

    # Iterate over the BPMN edges/flows
    for flow in bpmn.get_flows():
        source_node = flow.get_source()
        target_node = flow.get_target()

        source_id = str(source_node.get_id())
        target_id = str(target_node.get_id())

        # Retrieve or create the source vertex
        if source_id not in mapping:
            src = Vertex(source_id)
            mapping[source_id] = src
            graph.addVertex(src)

            if isinstance(source_node, BPMN.Gateway):
                gates[source_id] = source_node
            #endif
        else:
            src = mapping[source_id]
        #endif

        # Retrieve or create the target vertex
        if target_id not in mapping:
            tgt = Vertex(target_id)
            mapping[target_id] = tgt
            graph.addVertex(tgt)

            if isinstance(target_node, BPMN.Gateway):
                gates[target_id] = target_node
            #endif
        else:
            tgt = mapping[target_id]
        #endif

        # Connect the vertices while preserving parallel edges
        graph.addEdge(src, tgt)
    #endfor

    # Compute the RPST
    rpst = RPST(graph)

    root = rpst.getRoot()
    if not root:
        # Handle empty graphs
        structuredness = 1.0 if graph.getEdges().isEmpty() else 0.0
        nodes_count = 0
        structured_size = 0
    else:
        # deque replaces Java's LinkedList
        to_analyze = deque([(None, root)])

        # create sets
        rigids_set = set()
        bonds_set = set()
        structured = set()

        # analyze structure
        count = True
        while to_analyze:
            parent_node, current_node = to_analyze.popleft()

            if (parent_node is not None and
                current_node.getType() == TCType.POLYGON and
                parent_node.getType() == TCType.BOND
            ):
                try:
                    entry_name = str(parent_node.getEntry().getName())
                    exit_name = str(parent_node.getExit().getName())

                    entry_gate = gates.get(entry_name)
                    exit_gate = gates.get(exit_name)

                    count = (
                        entry_gate is not None and
                        exit_gate is not None and
                        type(entry_gate) is type(exit_gate)
                    )

                except Exception:
                    count = False
                #endtry
            #endif

            # Iterate over the child nodes
            for child_node in rpst.getChildren(current_node):
                c_type = child_node.getType()

                match c_type:

                    # Rigid
                    case TCType.RIGID:
                        to_analyze.append((current_node, child_node))
                        rigids_set.add(child_node)

                    # Trivial
                    case TCType.TRIVIAL:
                        if count:
                            child_entry = child_node.getEntry()
                            child_exit = child_node.getExit()

                            if child_entry is not None:
                                e_name = str(child_entry.getName())
                                if e_name not in gates:
                                    structured.add(e_name)
                                #endif
                            #endif

                            if child_exit is not None:
                                ex_name = str(child_exit.getName())
                                if ex_name not in gates:
                                    structured.add(ex_name)
                                #endif
                            #endif
                        #endif

                    # Polygon
                    case TCType.POLYGON:
                        to_analyze.append((current_node, child_node))

                    # Bond
                    case TCType.BOND:
                        child_entry = child_node.getEntry()
                        child_exit = child_node.getExit()

                        if child_entry is not None:
                            structured.add(str(child_entry.getName()))
                        #endif
                        if child_exit is not None:
                            structured.add(str(child_exit.getName()))
                        #endif

                        to_analyze.append((current_node, child_node))
                        bonds_set.add(child_node)
                #endmatch
            #endfor

            count = False
        #endwhile

        # Calculate the final Structuredness Score
        nodes_count = len(bpmn.get_nodes())
        structured_size = len(structured)

        if nodes_count == 0:
            structuredness = 1.0  # An empty diagram is perfectly structured
        else:
            structuredness = structured_size / nodes_count
        #endif
    #endif

    # Format the result
    result_json = {
        "structuredness": structuredness,
        "bpmn_nodes": nodes_count,
        "structured": structured_size,
        "polygon": rpst.getRPSTNodes(TCType.POLYGON).size() if root else 0,
        "trivial": rpst.getRPSTNodes(TCType.TRIVIAL).size() if root else 0,
        "rigid": rpst.getRPSTNodes(TCType.RIGID).size() if root else 0,
        "bond": rpst.getRPSTNodes(TCType.BOND).size() if root else 0
    }

    return result_json
#enddef