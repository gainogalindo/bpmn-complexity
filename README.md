# bpmn-complexity

A compact Python library for computing BPMN complexity metrics, integrated with [PM4Py](https://pm4py.fit.fraunhofer.de/).

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
structuredness = bpmn_complexity.compute_structuredness(bpmn_diagram)

print(f"Size: {size}")
print(f"CFC: {cfc}")
print(f"Structuredness: {structuredness:.2f}")
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

The Structuredness implementation is based on the implementation available in SplitMiner:

https://github.com/nemo-91/bpmtk/blob/master/src/au/edu/qut/bpmn/metrics/ComplexityCalculator.java

To compute Structuredness, the implementation requires the construction of a Refined Process Structure Tree (RPST).

For this purpose, a standalone `rpst.jar` containing the required RPST functionality was created and is available at:

https://github.com/gainogalindo/rpst

The Java implementation is accessed from Python through JPype.

## Event Log

The examples in this repository use the publicly available **Repair Example** event log.

It can be downloaded from:

http://www.promtools.org/prom6/downloads/example-logs.zip

## Generating the BPMN Files

The BPMN diagrams used in the examples were generated from the Repair Example event log using **SplitMiner** and **SplitMiner 2.0**.

SplitMiner is available from the Apromore Research Lab:

https://apromore.com/research-lab

Java 8 is required to run the SplitMiner versions used in these examples.

### SplitMiner

Example command in Windows PowerShell:

```powershell
& "C:\Program Files (x86)\Java\jre1.8.0_491\bin\java.exe" `
    -cp "sm2.jar;lib\*" `
    au.edu.unimelb.services.ServiceProvider `
    SMD 0.4 0.1 false false false `
    .\repair.xes.gz `
    .\repair_sm
```

### SplitMiner 2.0

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

## Requirements

The library requires:

- Python
- [PM4Py](https://pm4py.fit.fraunhofer.de/) for BPMN handling
- [JPype](https://jpype.readthedocs.io/) for Python–Java integration
- Java, required for Structuredness computation
- The RPST JAR provided by the [`rpst`](https://github.com/gainogalindo/rpst) project

### Java Configuration

JPype must be able to locate a valid Java Virtual Machine (JVM).

The Java installation can be made available through the `JAVA_HOME` environment variable, through the system `PATH`, or by explicitly providing the JVM path when starting JPype.

For example, on Windows:

```text
JAVA_HOME=C:\Program Files\Java\jdk-21
```

The `bin` directory may also be added to `PATH`:

```text
C:\Program Files\Java\jdk-21\bin
```

Note that the Java version required to run the SplitMiner examples is independent of the Java version used by `bpmn-complexity` through JPype.
