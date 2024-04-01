from . import LAPI
from . import Plotting
from .Datafile import *
from .Dataset import *
import numpy as np
import scipy.signal
import scipy.signal as sci
import matplotlib.pyplot as plt


def InitializePlotting():
    Plotting.init_plot()

def LoadTestDataSetFromSingleFile(folder, file, name="", source="NI"):
    """ loads all data from the given file and returns DataSet object with array of Datafiles
        use to load all measurements from single test
        IF source=NI, then loads all data from single file """

    if name == "":
        name = file
    dataset = Dataset(name)
    #print("init dataset " + name)
    path = LAPI.get_path_to_file(folder, file)

   # print(path)

    if source == "NI":
        try:
            dfs = LoadMultipleDataFilesFromSingleFile(path)
            for df in dfs:
                dataset.add_datafile(df)
        except TypeError:
            print("Error loading the file!")

    else:
        dataset.add_datafile(LoadSingleDataFile(path))

    return dataset


def LoadTestDataSet(folder, name="", source="NI", delimiter="\t", x_column=0):
    """ loads all files from the folder and returns DataSet object with array of Datafiles
    use to load all measurements from single test
    IF source=NI, then loads all data from single file in that folder """

    if name == "":
        name = folder


    paths = LAPI.load_filepaths_from_folder(folder)
    #print(paths)
    dataset = Dataset(name)
    #print("init dataset " + name)

    if source=="NI":
        try:
            dfs = LoadMultipleDataFilesFromSingleFile(paths[id], delimiter, x_column)
        except TypeError:
            print("Error loading the file!")
        for df in dfs:
            dataset.add_datafile(df)
    elif source=="SZAFA":
        for p in paths:
            dataset.add_datafile(LoadSingleDataFile(p))

    return dataset


def LoadSingleDataFile(filepath):
    """ loads single data file and returns Datafile object with raw data"""
    x, y, name = LAPI.load_data_from_file(filepath)
    data = Datafile(x, y, name)
    return data

def LoadMultipleDataFilesFromSingleFile(filepath, delimiter="\t", x_column=0):
    """ loads multiple data files from single multi column file and returns Datafiles object with raw data"""
    set = LAPI.load_multicolumn_data_from_file(filepath, delimiter, x_column)
    datafiles = []
    for data in set:
        datafiles.append(Datafile(data[1], data[2], data[0]))

    return datafiles

def TrimSingleDataFile(datafile, show_plot=True):
    """ asks user for bounds input, and trims single data file from lower to upper boundary (x-axis value)
        additionally returns lower, upper bounds for use
    """
    x, y = datafile.get_raw_data()
    is_ok = False
    while not is_ok:
        print("Plotting data for quick view")
        if show_plot:
            datafile.plot(True) # always plot raw data here

        lower = LAPI.get_bound_input_from_user("Please input lower value (from): ")
        upper = LAPI.get_bound_input_from_user("Please input upper value (to): ")

        new_x, new_y = LAPI.trim_data(x, y, lower, upper)
        datafile.set_parsed_data(new_x, new_y)
        datafile.plot()
        is_ok = LAPI.ask_yes_no_question("Is that ok?")

    return lower, upper


def TrimDataSet(dataset,  lower, upper):
    """ trim function for the entire dataset  """
    for df in dataset:
        x, y = df.get_raw_data()
        new_x, new_y = LAPI.trim_data(x, y, lower, upper)
        df.set_parsed_data(new_x, new_y)


def FixCleanDatafile(datafile, bound_X=5):
    x1, y1 = datafile.get_raw_data()
    x2, y2 = LAPI.fix_remove_zeros(x1, y1)
    x3, y3 = LAPI.fix_remove_outliers(x2, y2,bound_X)
    datafile.set_parsed_data(x3, y3)


def FixCleanDataSet(dataset, bound_X = 20):
    for df in dataset:
        FixCleanDatafile(df, bound_X)


def FixZerosDatafile(datafile):
    x1, y1 = datafile.get_raw_data()
    x2, y2 = LAPI.fix_remove_zeros(x1, y1)
    datafile.set_parsed_data(x2, y2)


def FixZerosDataSet(dataset):
    for df in dataset:
        FixZerosDatafile(df)


def FixRemoveFromAreaDatafile(datafile, xa1, xa2, ya1, ya2):
    X1, Y1 = datafile.get_data()
    X2, Y2 = LAPI.fix_remove_from_area(X1, Y1, xa1, xa2, ya1, ya2)
    datafile.set_parsed_data(X2, Y2)


def FilterDataSet(dataset, window_length=51, polyorder=1):
    for df in dataset:
        FilterSingleDataFile(df, window_length=window_length, polyorder=polyorder)


def AssignValueInRange(datafile, value, start=None, stop=None):
    x, y = datafile.get_data()
    x_array = np.array(x)  # Convert x to a NumPy array, leaving original x unchanged

    # If both start and stop are provided, assign the value within the specified range
    if start is not None and stop is not None:
        mask = (x_array >= start) & (x_array <= stop)
        y[mask] = value

    datafile.set_parsed_data(x, y)

def FilterSingleDataFile(datafile, window_length=51, polyorder=1, start=None, stop=None):
    x, y = datafile.get_data()
    x_array = np.array(x)  # Convert x to a NumPy array, leaving original x unchanged

    # If both start and stop are provided, filter only the specified range
    if start is not None and stop is not None:
        mask = (x_array >= start) & (x_array <= stop)
        y_filtered = y[mask]
        filtered_y_filtered = scipy.signal.savgol_filter(y_filtered, window_length=window_length, polyorder=polyorder,
                                                         deriv=0)
        y[mask] = filtered_y_filtered
    else:  # If start and stop are not provided, filter the entire y array
        y = scipy.signal.savgol_filter(y, window_length=window_length, polyorder=polyorder, deriv=0)

    datafile.set_parsed_data(x, y)


def FindDerivativeSingleDataFile(datafile, window_length=3, polyorder=1):
    x, y = datafile.get_data()
    smooth_y = scipy.signal.savgol_filter(y, window_length=window_length, polyorder=polyorder, deriv=0)
    # Check if x is uniformly spaced
    dx = np.mean(np.diff(x))
    if dx == 0:
        raise ValueError("Time vector must be uniformly spaced to compute derivative.")

    filtered_y = np.gradient(smooth_y, dx)
    datafile.set_parsed_data(x, filtered_y)


def LowPassFilterSingleDataFile(datafile, fs, cutoff, order=1):
    nyq = fs / 2
    low_cutoff = cutoff / nyq
    b, a = sci.butter(order, low_cutoff, btype='low', analog=False)
    x, y = datafile.get_data()
    filtered_y = sci.lfilter(b, a, y)
    datafile.set_parsed_data(x, filtered_y)


def LowPassFilterDataSet(dataset, fs, cutoff, order=1):
    for df in dataset:
        LowPassFilterSingleDataFile(df, fs, cutoff, order=1)


def BandStopFilterSingleDataFile(datafile, fs, low_cutoff, high_cutoff, order=2):
    nyq = fs / 2
    low_cutoff = low_cutoff / nyq
    high_cutoff = high_cutoff / nyq
    b, a = sci.butter(order, [low_cutoff, high_cutoff], btype='bandstop', analog=False)
    x, y = datafile.get_data()
    filtered_y = sci.lfilter(b, a, y)
    datafile.set_parsed_data(x, filtered_y)


def FFTAnalysisSingleDataFile(datafile, fs):
    x, y = datafile.get_data()
    n = len(y)
    y = y - np.mean(y)
    # Perform FFT and calculate the magnitude
    yf = np.fft.fft(y)
    magnitude = 2.0 / n * np.abs(yf[:n // 2])

    # Calculate the corresponding frequency values
    freq = np.fft.fftfreq(n, 1 / fs)[:n // 2]

    plt.plot(freq, magnitude)
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.show()

    return freq, magnitude



def InterpolateSingleDataFile(datafile, samples=0, x_vector=[], show_plot=False):
    x, y = datafile.get_data()
    if samples <= 0:
        samples = (x[-1] * 100).__int__() # default number of samples is 100 Hz

    new_x, new_y = LAPI.interpolate_data(x, y, samples, x_vector)
    datafile.set_interpolated_data(new_x, new_y)
    if show_plot:
        datafile.plot()


def InterpolateDataSet(dataset, samples=0):
    x_min = max([(df.get_data()[0])[0] for df in dataset])
    x_max = min([(df.get_data()[0])[-1] for df in dataset])
    if samples <= 0:
        samples = (x_max * 100).__int__()  # default number of samples is 100 Hz
    x_vector = np.linspace(x_min, x_max, samples)

    for df in dataset:
        InterpolateSingleDataFile(df, samples, x_vector)


def SetPlotParamsForDatafile(datafile, name="", title="", xlabel="", ylabel=""):
    datafile.set_plot_params(name, title, xlabel, ylabel)


def PlotSingleDatafile(datafile):
    datafile.plot()


def PlotMultipleDatafiles(datafiles, scatter=False):
    f = Plotting.new_figure()
    legend = []
    for df in datafiles:
        Plotting.add_to_plot(f, df.get_data()[0], df.get_data()[1], name=df.name, title=df.data_title, xlabel=df.xlabel, ylabel=df.ylabel, scatter=scatter)
        legend.append(df.name)
    Plotting.set_legend(f, legend)
    Plotting.plt.grid(which='both')
    Plotting.plt.minorticks_on()
    Plotting.show()


def PlotDataset(dataset):
    dataset.plot_all()


def SetExportFolder(folder):
    Plotting._exportFolder = folder


def ExportSingleDatafilePlot(datafile, name=""):
    if name == "":
        name = datafile.name
    datafile.save_plot(name)
    Plotting.save_figure(name)
    print("EXPORTED PLOT: " + name)


def ExportDatasetPlots(dataset):
    print("EXPORTING DATASET: " + dataset.name)
    for df in dataset:
        ExportSingleDatafilePlot(df)


def ExportDatasetSubplot(dataset):
    dataset.save_plot()
    Plotting.save_figure(dataset.name)


def SaveSingleDatafileToFile(datafile, suffix="_parsed"):
    with open(datafile.name+suffix+".md", "w") as f:
        data = datafile.get_data()
        x = data[0]
        y = data[1]
        for i in range(0, len(x)):
            f.write(x[i].__str__() +", "+ y[i].__str__()  +"\n")


def PlotCustomized(data_files1, data_files2=None, title='', xlabel='', ylabel='', legend=[], scatter=False, ylabel2=''):
    Plotting.plot_customized(data_files1, data_files2=data_files2, title=title, xlabel=xlabel, ylabel=ylabel, legend=legend, scatter=scatter, ylabel2=ylabel2)


def FindAreaUnderCurve(datafile):
    x = datafile.get_data()[0]
    y = datafile.get_data()[1]
    area = np.trapz(y,x)
    return area


def SaveDataSetToFileDelimited(dataset, delimiter='\t', suffix="_parsed"):
    header = ""
    length = len(dataset[0].get_data()[0])
    time_vec = dataset[0].get_data()[0]
    header = dataset[0].name
    for file in dataset:
        header+=delimiter+file.name

    filename = dataset.name[:-4]

    with open("export/"+filename+suffix+".txt", "w") as f:
        f.write(header)
        for i in range(0, length):
            line = ""
            line += f"{time_vec[i]:.5f}"
            for file in dataset:
                line += delimiter + f"{file.get_y()[i]:.5f}"
            line = line.replace(".",",")
            f.write(line+"\n")
