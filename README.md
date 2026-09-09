# bpmn-complexity

A compact Python library for computing BPMN complexity metrics, integrated with [PM4Py](https://processintelligence.solutions/pm4py).

Currently implemented metrics:

- **Control-Flow Complexity (CFC)**
- **Size**
- **Structuredness**

Structuredness relies on Java code accessed from Python through [JPype](https://jpype.readthedocs.io/).

## Usage

Load a BPMN diagram with PM4Py and compute the available complexity metrics:

```python
import pm4py
import bpmn_complexity

bpmn_diagram = pm4py.read_bpmn("model.bpmn")

size = bpmn_complexity.compute_size(bpmn_diagram)
cfc = bpmn_complexity.compute_cfc(bpmn_diagram)
struct = bpmn_complexity.compute_structuredness(bpmn_diagram)

print(f"Size: {size}")
print(f"CFC: {cfc}")
print(f"Structuredness: {struct['structuredness']:.2f}")
```

Example output:

```text
Size: 14
CFC: 4
Structuredness: 0.36
```

## Metrics

### Control-Flow Complexity (CFC)

The implementation of Control-Flow Complexity is based on:

> Cardoso, J. (2005). *Control-flow Complexity Measurement of Processes and Weyuker’s Properties.*

### Size

The Size metric is based on:

> Mendling, J., et al. (2007). *Error Metrics for Business Process Models.*

### Structuredness

The Structuredness computation is based on the implementation available in Split Miner:

https://github.com/nemo-91/bpmtk/blob/master/src/au/edu/qut/bpmn/metrics/ComplexityCalculator.java

To compute Structuredness, the implementation requires the construction of a Refined Process Structure Tree (RPST).

For this purpose, a standalone `rpst.jar` containing the required RPST functionality is bundled with this library. The source code used to build the JAR is available at:

https://github.com/gainogalindo/rpst

The Java implementation is accessed from Python through JPype.

## Event Log

The examples in this repository use the publicly available **Repair Example** event log.

It can be downloaded from:

http://www.promtools.org/prom6/downloads/example-logs.zip

## Generating the BPMN Files

The BPMN diagrams used in the examples were generated from the Repair Example event log using **Split Miner** and **Split Miner 2.0**.

Split Miner 2.0 is available from the Apromore Research Lab:

https://apromore.com/research-lab

Java 8 is required to run the Split Miner versions used in these examples.

### Split Miner

Example command in Windows PowerShell:

```powershell
& "C:\Program Files (x86)\Java\jre1.8.0_491\bin\java.exe" `
    -cp "sm2.jar;lib\*" `
    au.edu.unimelb.services.ServiceProvider `
    SMD 0.4 0.1 false false false `
    .\repair.xes.gz `
    .\repair_sm
```

### Split Miner 2.0

Example command in Windows PowerShell:

```powershell
& "C:\Program Files (x86)\Java\jre1.8.0_491\bin\java.exe" `
    -cp "sm2.jar;lib\*" `
    au.edu.unimelb.services.ServiceProvider `
    SM2 `
    .\repair.xes.gz `
    .\repair_sm2 `
    0.05
```

## Expected Output

For `repair_sm.bpmn`:

```text
File: repair_sm.bpmn
Size: 14, CFC: 4, Struc.: 0.36
```

For `repair_sm2.bpmn`:

```text
File: repair_sm2.bpmn
Size: 16, CFC: 5, Struc.: 0.50
```

## Checking the Results

The expected Structuredness results can be compared with the results reported in:

https://arxiv.org/abs/2105.06016

See **Table 3 on page 10**, particularly the results for the **R-Log**.

### Additional BPMN models

Additional BPMN models used for validation are available in `src/bpmn/exp-results/SM/default-models`. These models were obtained from the [reproducibility dataset](https://doi.org/10.6084/m9.figshare.11413794) of the paper [Optimization framework for DFG-based automated process discovery approaches](https://link.springer.com/article/10.1007/s10270-020-00846-x).

The complexity results can be compared against the default Split Miner (`SM`) models reported in [Table 2](https://link.springer.com/article/10.1007/s10270-020-00846-x/tables/2). Below are the results found using `bpmn-complexity`: 

| Model | Size | CFC | Structuredness |
|---|---:|---:|---:|
| BPIC12 | 51 | 41 | 0.69 |
| BPIC14_f | 20 | 14 | 1.00 |
| BPIC15_1f | 111 | 45 | 0.51 |
| BPIC15_2f | 129 | 49 | 0.36 |
| BPIC15_3f | 96 | 35 | 0.49 |
| BPIC15_4f | 101 | 37 | **0.29** |
| BPIC15_5f | 110 | 38 | 0.34 |
| RTFMP | 22 | 17 | 0.46 |
| SEPSIS | 32 | 23 | 0.94 |

For `BPIC15_4f`, `bpmn-complexity` obtains a Structuredness value of `0.287129` (`0.29` when rounded to two decimal places), while [Table 2](https://link.springer.com/article/10.1007/s10270-020-00846-x/tables/2) reports `0.27`. Size (`101`) and CFC (`37`) match exactly, suggesting that the Structuredness value reported in this table may contain a typographical error.

## Requirements

The library requires:

- Python
- [PM4Py](https://processintelligence.solutions/pm4py) for BPMN handling
- [JPype](https://jpype.readthedocs.io/) for Python–Java integration
- Java, required for Structuredness computation
- The required `rpst.jar` is bundled with this library. Its source code is available in the [`rpst`](https://github.com/gainogalindo/rpst) repository

### Java Configuration

JPype must be able to locate a valid Java Virtual Machine (JVM). The recommended approach is to configure the `JAVA_HOME` environment variable. Alternatively, the JVM path can be provided explicitly when starting JPype.

For example, on Windows:

```text
JAVA_HOME=C:\Program Files\Java\jdk-21
```

Note that the Java version required to run the Split Miner 2.0 examples is independent of the Java version used by `bpmn-complexity` through JPype.
