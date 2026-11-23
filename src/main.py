import glob
import os
import sys
sys._pm4py_welcome_shown = True # supress welcome message from PM4Py
import pm4py

# BPMN Complexity
import bpmn_complexity


def analyze_complexity_file(file: str, rounding:int=2):
    print(f"\nFile: {os.path.basename(file)}")

    # Read BPMN file using PM4Py
    bpmn_diagram = pm4py.read_bpmn(file)

    # Compute Complexity Metrics
    size = bpmn_complexity.compute_size(bpmn_diagram)
    cfc = bpmn_complexity.compute_cfc(bpmn_diagram)
    struct = bpmn_complexity.compute_structuredness(bpmn_diagram)
    # Same rounding of Java's implementation
    struct_val = float(f"{struct['structuredness']:.3f}")

    # Print output
    print(f"Size: {size}, CFC: {cfc}, Struc.: {struct_val:.{rounding}f}")

    # Used for test purposes
    print_structuredness = False
    if print_structuredness:
        print(struct)
    #endif
#enddef

def analyze_complexity_dir(dir: str):
    # Scan for .bpmn files
    bpmn_files = glob.glob(os.path.join(dir, '*.bpmn'))

    if not bpmn_files:
        print("No .bpmn file found.")
        return
    #endif

    # Calculate complexity metrics for every BPMN diagram
    for file in bpmn_files:
        analyze_complexity_file(file)
    #endfor
#enddef

if __name__ == "__main__":
    dir = 'bpmn'
    analyze_complexity_dir(dir)

    dir = 'bpmn/exp-results/SM/default-models'
    analyze_complexity_dir(dir)

    file = 'bpmn/BPIC12.bpmn'
    analyze_complexity_file(file, 3)
#endif