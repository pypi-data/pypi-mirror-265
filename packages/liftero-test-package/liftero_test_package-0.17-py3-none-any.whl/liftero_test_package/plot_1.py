
from HLAPI import *

import enum
import matplotlib.pyplot as plt
from matplotlib import rcParams
import itertools

# This file plots:
# a) basic single test plot with: chamber pressure, injector pressures, thrust
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
test_name = "H2/H228"

# zaladuj wszystkie dane z folderu i nazwij zestaw danych "Test 1"



d3 = LoadTestDataSetFromSingleFile(dataFolder, test_name+".txt", source="NI")
#B

for df in d3:
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
    IdV2.Fuel_injector_pressure : 'green'
}

names = {
    IdV2.Thrust : "Thrust",
    IdV2.CC_pressure : 'Combustion chamber',
    IdV2.OX_tank_pressure : 'N2O Tank',
    IdV2.OX_injector_pressure : 'N2O Injector',
    IdV2.Fuel_tank_pressure : 'Fuel Tank',
    IdV2.Fuel_injector_pressure : 'Fuel Injector'
}

Id = IdV2  # select log headers version

FilterDataSet(d3, 10)

elements = [
    Id.CC_pressure,
    Id.OX_tank_pressure,
    Id.OX_injector_pressure,
    Id.Fuel_injector_pressure
    ]

fig = plt.figure()
lines = []
for element in elements:
    index = element.value
    x, y = d3[index].get_data()
    line = plt.plot(x, y, linewidth=1.2, color=colors[element.value], label=names[element.value])
    lines.extend(line)


plt.grid(True, which="major", color='lightgray', linewidth=0.3)
plt.xlabel('Time [s]', fontsize=12, fontweight='bold')
plt.ylabel('Pressure [bar]', fontsize=12, fontweight='bold')
plt.tick_params(axis='both', direction='in', width=1.3, top=True, right=True)
plt.xlim([-1, 6])
plt.ylim([-0.5, 5.5])
# plt.legend()


plt.tight_layout()
plt.savefig("plot_1_out.png", dpi=300)
plt.savefig("plot_1_out.pdf", dpi=300)
plt.grid(True, which="major", color='lightgray', linewidth=0.3)
plt.show()
