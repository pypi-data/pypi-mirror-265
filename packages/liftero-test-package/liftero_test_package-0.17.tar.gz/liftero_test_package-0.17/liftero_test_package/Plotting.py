import matplotlib.pyplot as plt
from matplotlib import rcParams
import itertools
import matplotlib.ticker as plticker
from matplotlib import font_manager
# rcParams['font.family'] = 'sans-serif'
# rcParams['font.sans-serif'] = ['Arial']
# plt.rcParams['axes.axisbelow'] = True
# plt.rcParams.update({'font.size': 11})
# plt.rcParams["lines.linewidth"] = 1.2
# plt.rcParams["axes.titleweight"] = 'bold'
# plt.rcParams["axes.titlesize"] = 10
# plt.rcParams["figure.figsize"] = (7, 6)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.axisbelow'] = True
plt.rcParams.update({'font.size': 12})
plt.rcParams["lines.linewidth"] = 1.2
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["axes.titleweight"] = 'bold'
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["figure.figsize"] = (7, 4)
rcParams['axes.linewidth'] = 1.3
rcParams["mathtext.default"] = 'regular'


markers = itertools.cycle(('D', 'D', 'D', 'o', 'o', 'o'))
colors = itertools.cycle(('royalblue', 'tomato', 'seagreen', 'goldenrod', 'brown', 'hotpink', 'brown'))

# directory for exported figures
_exportFolder = "figures"


def init_plot():
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Tahoma']
    plt.rcParams['axes.axisbelow'] = True
    plt.rcParams.update({'font.size': 11})
    plt.rcParams["figure.figsize"] = (10, 6)


def plot_and_show(x, y, legend="", title="", xlabel="", ylabel=""):
    plt.figure()
    plt.plot(x, y)
    plt.legend([legend])
    plt.title(title, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")
    plt.ylabel(ylabel, fontweight="bold")
    plt.minorticks_on()
    plt.grid(which="both")
    plt.tight_layout()
    plt.show()


def plot(x, y, legend="", title="", xlabel="", ylabel=""):
    plt.figure()
    plt.plot(x, y)
    plt.legend([legend])
    plt.title(title, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")
    plt.ylabel(ylabel, fontweight="bold")
    plt.minorticks_on()
    plt.grid(which="both")
    plt.tight_layout()


def new_figure(size=(10, 7), dpi=72):
    f = plt.figure(figsize=size, dpi=dpi)
    return f


def set_legend(figure, legend):
    figure.legend(legend)


def save_figure(name):
    try:
        plt.savefig(_exportFolder +"/" + name + ".png")
    except FileNotFoundError:
        plt.savefig(name+".png")


def add_to_subplot(figure, i, x, y, name, xlabel="", ylabel=""):

    axis = figure.add_subplot(2, 1, i + 1)
    plt.minorticks_on()
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    plt.grid(which="both")
    axis.plot(x, y, label=name)
    axis.legend(fontsize='x-small', loc='upper center', bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True)
    plt.subplots_adjust(hspace=0.4)


def add_to_plot(figure, x, y, name, title="", xlabel="", ylabel="", scatter=False):
    plt.figure(figure)
    if scatter:
        plt.scatter(x, y, s=3)
    else:
        plt.plot(x, y)
    plt.title(title, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")
    plt.ylabel(ylabel, fontweight="bold")
    # plt.minorticks_on()
    # plt.grid(which="both")
    plt.tight_layout()


def show():
    plt.show()


def plot_customized(data_files1, data_files2=None, title='', xlabel='', ylabel='', ylabel2='', legend=[], scatter=False):
    fig, ax1 = plt.subplots()

    lines = []
    labels = []
    # marker=markers.__next__(), markevery=300

    for i, data_file in enumerate(data_files1):
        x_data, y_data = data_file.get_data()
        if scatter:
            line = ax1.scatter(x_data, y_data, label=legend[i] if i < len(legend) else None, linewidth=1, color = colors.__next__())
        else:
            line = ax1.plot(x_data, y_data, label=legend[i] if i < len(legend) else None, linewidth=1.8, color = colors.__next__(), marker = markers.__next__(), markersize=5.5, markerfacecolor="white",  markevery=250)
        lines.append(line)
        labels.append(legend[i] if i < len(legend) else None)
    # ax1.set_ylim(0, 55)
    ax1.set_xlabel(xlabel, fontweight="bold")
    ax1.set_ylabel(ylabel, fontweight="bold")
    #ax1.set_title(title, fontweight="bold")
    #loc = plticker.MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
    #ax1.xaxis.set_major_locator(loc)
    # ax1.minorticks_on()
    # ax1.grid(which="both")

    if data_files2 is not None:
        ax2 = ax1.twinx()
        for i, data_file in enumerate(data_files2):
            x_data, y_data = data_file.get_data()
            if scatter:
                line = ax2.scatter(x_data, y_data,
                                   label=legend[i + len(data_files1)] if i + len(data_files1) < len(legend) else None, linewidth=1, color = colors.__next__())
            else:
                line = ax2.plot(x_data, y_data,
                                label=legend[i + len(data_files1)] if i + len(data_files1) < len(legend) else None, linewidth=1, color = colors.__next__())
            lines.append(line)
            labels.append(legend[i + len(data_files1)] if i + len(data_files1) < len(legend) else None)
        ax2.set_ylabel(ylabel2, fontweight="bold")
        # ax2.set_ylim([0, 50])
    fig.legend(loc='upper right', bbox_to_anchor=(0.95, 0.94))
    ax1.grid(True, which="major", color='lightgray', linewidth=0.3)
    ax1.tick_params(axis='both', direction='in', width=1.3, top=True, right=True)

    # ax1.set_xlim(-2, 9)
    # plt.minorticks_on()
    # plt.grid(which="both")
    plt.tight_layout()
    plt.savefig("out/"+title+".tif", dpi=300)
    plt.show()