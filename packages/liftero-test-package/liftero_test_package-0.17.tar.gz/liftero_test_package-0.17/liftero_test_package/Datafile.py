from . import Plotting as plot
import numpy as np
import math

class Datafile:
    """ this class stores x,y vectors of single .md data file """
    name = ""  # name printed in the legend on the plot
    type = ""  # type for automatic x/y labels on the plot
    xlabel = ""  # x-label on the plot
    ylabel = ""  # y-label on the plot
    data_title = ""  # title on the plot
    header = ""

    # DATA storage
    # object can store following information on the x,y vectors:
    # raw - loaded from the file, without any changes
    # parsed - trimmed / manipulated in other way
    # interpolated - recreated for given x-vector
    # object always keeps raw data for use

    raw_x = []
    raw_y = []
    parsed_x = []
    parsed_y = []
    interp_x = []
    interp_y = []

    is_parsed = False
    is_interpolated = False

    n = 0

    def __init__(self, x, y, name):
        self.raw_x = x
        self.raw_y = y
        self.name = name
        self.recognize_type()

    def __str__(self):
        x, y = self.get_data()
        return self.name + ", " + len(x).__str__() + " x " + len(y).__str__() + " type: " + self.type

    def __iter__(self):
        self.n = 0
        return self

    def __getitem__(self, index):
        return self.get_data()[1][index]

    def __setitem__(self, index, value):
        self.get_data()[1][index] = value

    def __len__(self):
        return len(self.get_data()[0])

    def __next__(self):
        y = self.get_data()[1]
        if self.n < len(y):
            self.n += 1
            return y[self.n - 1]
        else:
            raise StopIteration

    def __add__(self, other):
        if isinstance(other, Datafile):
            y1 = self.get_data()[1]
            y2 = other.get_data()[1]
            new_y = [sum(y) for y in zip(y1, y2)]

            new_object = Datafile(self.get_data()[0], new_y, self.name + " + " + other.name)
            return new_object
        else:
            new_y = [y + other for y in self.get_data()[1]]
            new_object = Datafile(self.get_data()[0], new_y, self.name)
            return new_object

    def __sub__(self, other):
        if isinstance(other, Datafile):
            y1 = self.get_data()[1]
            y2 = other.get_data()[1]
            new_y = [ya - yb for ya, yb in zip(y1, y2)]

            new_object = Datafile(self.get_data()[0], new_y, self.name + " - " + other.name)
            return new_object
        else:
            new_y = [y - other for y in self.get_data()[1]]
            new_object = Datafile(self.get_data()[0], new_y, self.name)
            return new_object

    __radd__ = __add__
    __rsub__ = __sub__

    def __mul__(self, other):
        if isinstance(other, Datafile):
            y1 = self.get_data()[1]
            y2 = other.get_data()[1]
            new_y = [ya * yb for ya, yb in zip(y1, y2)]

            new_object = Datafile(self.get_data()[0], new_y, self.name + " * " + other.name)
            return new_object
        else:
            new_y = [y * other for y in self.get_data()[1]]
            new_object = Datafile(self.get_data()[0], new_y, self.name)
            return new_object

    def __truediv__(self, other):
        if isinstance(other, Datafile):
            y1 = self.get_data()[1]
            y2 = other.get_data()[1]
            new_y = [ya / yb for ya, yb in zip(y1, y2)]

            new_object = Datafile(self.get_data()[0], new_y, self.name + " / " + other.name)
            return new_object
        else:
            new_y = [y / other for y in self.get_data()[1]]
            new_object = Datafile(self.get_data()[0], new_y, self.name)
            return new_object

    __rmul__ = __mul__
    __rtruediv__ = __truediv__

    def recognize_type(self):
        if "PRESSURE_SENSOR" in self.name:
            self.type = "pressure"
            self.xlabel = "Time [s]"
            self.ylabel = "Pressure [bar]"
        elif "THERMOMETER" in self.name:
            self.type = "temperature"
            self.xlabel = "Time [s]"
            self.ylabel = "Temperature [$\circ C$]"
        elif "FLOW_METER" in self.name:
            self.type = "flowmeter"
            self.xlabel = "Time [s]"
            self.ylabel = "Mass flow [g/s]"
        elif "FORCE" in self.name:
            self.type = "force"
            self.xlabel = "Time [s]"
            self.ylabel = "Thrust [N]"
        elif "TENSOMETER" in self.name:
            self.type = "force"
            self.xlabel = "Time [s]"
            self.ylabel = "Thrust [N]"

    def get_raw_data(self):
        return self.raw_x, self.raw_y

    def get_data(self, raw=False, parsed=False):
        """ function return x,y vectors in following order: raw data < parsed data < interpolated data """
        if raw:
            return self.raw_x, self.raw_y
        elif parsed:
            return self.parsed_x, self.parsed_y
        elif self.is_interpolated:
            return self.interp_x, self.interp_y
        elif self.is_parsed:
            return self.parsed_x, self.parsed_y
        else:
            return self.raw_x, self.raw_y

    def get_y(self, raw=False, parsed=False):
        """ function return y vector in following order: raw data < parsed data < interpolated data """
        if raw:
            return self.raw_y
        elif parsed:
            return self.parsed_y
        elif self.is_interpolated:
            return self.interp_y
        elif self.is_parsed:
            return self.parsed_y
        else:
            return self.raw_y

    def get_x(self, raw=False, parsed=False):
        """ function return x vector in following order: raw data < parsed data < interpolated data """
        if raw:
            return self.raw_x
        elif parsed:
            return self.parsed_x
        elif self.is_interpolated:
            return self.interp_x
        elif self.is_parsed:
            return self.parsed_x
        else:
            return self.raw_x

    def set_data(self, x, y):
        self.parsed_x = self.interp_x = self.raw_x = x
        self.parsed_y = self.interp_y = self.raw_y = y
        self.is_parsed = False
        self.is_interpolated = False

    def set_parsed_data(self, x, y):
        self.parsed_x = x
        self.parsed_y = y
        self.is_parsed = True

    def set_interpolated_data(self, x, y):
        self.interp_x = x
        self.interp_y = y
        self.is_interpolated = True

    def plot(self, raw=False, parsed=False):
        if (not self.is_parsed and not self.is_interpolated) or raw:
            plot.plot_and_show(self.raw_x, self.raw_y, self.name, self.data_title, self.xlabel, self.ylabel)
        elif not self.is_interpolated or parsed:
            plot.plot_and_show(self.parsed_x, self.parsed_y, self.name, self.data_title, self.xlabel, self.ylabel)
        else:
            plot.plot_and_show(self.interp_x, self.interp_y, self.name, self.data_title, self.xlabel, self.ylabel)

    def save_plot(self, name="", raw=False, parsed=False):
        if name == "":
            name = self.name

        if (not self.is_parsed and not self.is_interpolated) or raw:
            plot.plot(self.raw_x, self.raw_y, name, self.data_title, self.xlabel, self.ylabel)
        elif not self.is_interpolated or parsed:
            plot.plot(self.parsed_x, self.parsed_y, name, self.data_title, self.xlabel, self.ylabel)
        else:
            plot.plot(self.interp_x, self.interp_y, name, self.data_title, self.xlabel, self.ylabel)

    def set_plot_params(self, name="", title="", xlabel="", ylabel=""):
        if name != "":
            self.name = name
        if title != "":
            self.data_title = title
        if xlabel != "":
            self.xlabel = xlabel
        if ylabel != "":
            self.ylabel = ylabel

    def set_data_title(self, title):
        self.data_title = title

    def adjust_time(self, change):
        """ shifts X scale by change value"""
        self.raw_x = [x + change for x in self.get_x()]
        self.parsed_x = self.raw_x

    def increase_sampling_rate(self, target_rate, noise=0.008):
        X_new = np.linspace(self.raw_x[0], self.raw_x[-1], int((self.raw_x[-1] - self.raw_x[0]) * target_rate + 1))
        self.raw_y = np.interp(X_new , self.raw_x, self.raw_y)
        self.raw_x = X_new
        # Adding noise
        noise = np.random.uniform(low=1-noise, high=1+noise, size=self.raw_y.shape)
        self.raw_y = self.raw_y * noise
        self.parsed_x = self.raw_x
        self.parsed_y = self.raw_y

    def find_first_time_above_threshold(self, threshold):
        for index, value in enumerate(self.get_y()):
            if value > threshold:
                return self.get_x()[index]
        return None

    def average(self, start=0, end=0):
        x, y = self.get_data()
        if start == end == 0:
            end = self.raw_x[-1]
        start_index = min(range(len(x)), key=lambda i: abs(x[i] - start))
        end_index = min(range(len(x)), key=lambda i: abs(x[i] - end))
        for idx, val in enumerate(y):
            if math.isnan(val):
                print("NAN: " + idx.__str__())


        if start_index > end_index:
            print("No valid range found")
            return None

        values_within_range = y[start_index:end_index]

        return sum(values_within_range) / len(values_within_range)

    def find_burn_time(self, x_time=None):
        x, y = self.get_data()

        y = list(y)

        # Determine the starting index for max value search
        start_idx = 0
        if x_time is not None:
            start_idx = min(range(len(x)), key=lambda i: abs(x[i] - x_time))

        # Find max value starting from x_time
        max_val = max(y[start_idx:])
        max_idx = y.index(max_val, start_idx)
        max_time = x[max_idx]
        # Find the value that is 50% of the max value
        half_max = max_val * 0.5

        # Initialize variables to store time and value for the first half
        first_half_val = None
        first_half_time = None
        first_half_idx = None
        # Search for 50% value in the first half
        for idx, val in enumerate(y[:max_idx]):
            if math.isclose(val, half_max, rel_tol=0.5):
                first_half_val = val
                first_half_time = x[idx]
                first_half_idx = idx
                break

        # Initialize variables to store time and value for the second half
        second_half_val = None
        second_half_time = None
        second_half_idx = None

        # Search for 50% value in the second half
        for idx, val in enumerate(y[max_idx:]):
            if math.isclose(val, half_max, rel_tol=0.1):
                second_half_val = val
                second_half_time = x[idx + max_idx]  # Adjust index for the slice
                second_half_idx = idx
                break

        burn_time = second_half_time - first_half_time

        return burn_time, (max_val, max_time), (first_half_val, first_half_time), (second_half_val, second_half_time), (first_half_idx, second_half_idx)

    # Your average function here, like def average(self, start, end): ...
