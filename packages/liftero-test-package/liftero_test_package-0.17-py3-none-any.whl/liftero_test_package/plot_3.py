
from HLAPI import *

import enum
import matplotlib.pyplot as plt
from matplotlib import rcParams
import itertools

# This file plots:
# b) temperature measurements for multiple tests - interpolated
#

plt.rcParams['font.family'] = 'sans-serif'

rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.axisbelow'] = True
plt.rcParams.update({'font.size': 10})
plt.rcParams["lines.linewidth"] = 1.2
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["axes.titleweight"] = 'bold'
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["figure.figsize"] = (7, 4)
rcParams['axes.linewidth'] = 1.3
rcParams["mathtext.default"] = 'regular'

marker = itertools.cycle(('D', 'o', 's'))
# colors = itertools.cycle(('royalblue', 'seagreen', 'tomato', 'goldenrod', 'hotpink', 'brown'))


# ustaw folder /wykresy/ jako docelowy do eksportowania wykresów
SetExportFolder("wykresy")

# wskazuje folder z danymi
dataFolder = ""
#A
test_name = "E2/E231"

# zaladuj wszystkie dane z folderu i nazwij zestaw danych "Test 1"

test_list = ["E2/E242", "E2/E244", "E2/E245", "E2/E246", "E1/E193"]

d_list = [LoadTestDataSetFromSingleFile(dataFolder, t+".txt", source="NI") for t in test_list]
# d3 = LoadTestDataSetFromSingleFile(dataFolder, test_name+".txt", source="NI")
#B

for d in d_list:
    for df in d:
        df.adjust_time(-2)

# new file header:
#  - ts
#  - Purge pressure
#  - OX tank pressure
#  - OX injector pressure
#  - CC pressure
#  - Fuel tank pressure
#  - Fuel injector pressure
#  - Fuel storage pressure
#  - Fuel Flow
#  - OX tank mass
#  - Thrust
#  - Bridge 3
#  - Bridge 4
#  - TC 1
#  - TC 2
#  - TC 3
#  - TC 4

class IdV2(enum.IntEnum):
    Purge_pressure = 0
    OX_tank_pressure = enum.auto()
    OX_injector_pressure = enum.auto()
    CC_pressure = enum.auto()
    Fuel_tank_pressure = enum.auto()
    Fuel_injector_pressure = enum.auto()
    Fuel_storage_pressure = enum.auto()
    Fuel_Flow = enum.auto()
    OX_tank_mass = enum.auto()
    Thrust = enum.auto()
    Bridge_3 = enum.auto()
    Bridge_4 = enum.auto()
    OMV = enum.auto()
    FMV = enum.auto()
    TC_1 = enum.auto()
    TC_2 = enum.auto()
    TC_3 = enum.auto()
    TC_4 = enum.auto()

colors = {
    IdV2.Thrust : "black",
    IdV2.CC_pressure : 'orangered',
    IdV2.OX_tank_pressure : 'blue',
    IdV2.OX_injector_pressure : 'royalblue',
    IdV2.Fuel_tank_pressure : 'darkgreen',
    IdV2.Fuel_injector_pressure : 'green',
    IdV2.TC_2: "red"
}

names = {
    IdV2.Thrust : "Thrust",
    IdV2.CC_pressure : 'Combustion chamber',
    IdV2.OX_tank_pressure : 'N2O Tank',
    IdV2.OX_injector_pressure : 'N2O Injector',
    IdV2.Fuel_tank_pressure : 'Fuel Tank',
    IdV2.Fuel_injector_pressure : 'Fuel Injector',
    IdV2.TC_2 : "Sidewall temperature"
}

Id = IdV2  # select log headers version

for d3 in d_list:
    FilterDataSet(d3, 1000)

elements = [
    Id.TC_2,
    ]

fig = plt.figure()
lines = []
for d3 in d_list:
    for element in elements:
        index = element.value
        x, y = d3[index].get_data()
        if d3.name != "E1/E193.txt":
            line = plt.plot(x, y, linewidth=1.2, color=colors[element.value], label=names[element.value], alpha=0.5)
        else:
            line = plt.plot(x, y, linewidth=1.2, color="royalblue", label=names[element.value], alpha=0.8)
        lines.extend(line)


plt.grid(True, which="major", color='lightgray', linewidth=0.3)
plt.xlabel('Time [s]', fontsize=12, fontweight='bold')
plt.ylabel(r'Sidewall temperature [$\degree C$]', fontsize=12, fontweight='bold')
plt.tick_params(axis='both', direction='in', width=1.3, top=True, right=True)
plt.xlim([0, 8])
plt.title("")
# plt.legend()


plt.tight_layout()
plt.savefig("export.tif", dpi=300)

plt.grid(True, which="major", color='lightgray', linewidth=0.3)
plt.show()
