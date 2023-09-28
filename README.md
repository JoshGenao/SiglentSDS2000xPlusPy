# SiglentSDS2000xPlusPy
Control a Siglent SDS2000X Plus oscilloscope from python. This package allows the ability to create python scripts to automate testing receive trace data from an oscilloscope. 

![oscilloscope screenshot](https://siglentna.com/wp-content/uploads/2019/12/580-470-1.png)

## Installation
To install this package:
```
pip install git+https://github.com/JoshGenao/SiglentSDS2000xPlusPy.git
```
Or:
1. Clone repository
2. Install requirements 
```
pip install -r requirements.txt
```
3. pip install
```
pip install -e .
```
## Usage
Example:
```Python
from SiglentSDS2000xPlusPy.siglentsds2000xplus import *
import matplotlib.pyplot as plt

HOST = '192.168.1.blah'

scope = SiglentSDS2000XPlus(HOST)
scope.arm()
traces = scope.capture(SiglentSDS2000XChannel.C1)

# Plot traces
plt.plot(traces)
plt.show()
```