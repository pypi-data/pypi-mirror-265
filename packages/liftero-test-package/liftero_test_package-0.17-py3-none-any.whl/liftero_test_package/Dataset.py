from .Datafile import *
from . import Plotting as plot


class Dataset:
    """ this class operates on multiple Datafiles (e.g. all test data from the folder ) """
    name = ""
    _data = []

    def __init__(self, name=""):
        self.name = name
        self._data = []

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __str__(self):
        out = "Dataset: " + self.name + "\n"
        for x in self._data:
            out += x.__str__()
            out += "\n"
        return out

    def add_datafile(self, data):
        data.set_data_title(self.name)
        self._data.append(data)

    def get_datafile_by_name(self, name):
        for df in self._data:
            if df.name == name:
                return df
        return None

    def plot_all_on_separate_figures(self):
        for d in self._data:
            d.plot()
        plot.show()

    def plot_all(self):
        f = plot.new_figure()
        for idx, d in enumerate(self._data):
            x, y = d.get_data()
            plot.add_to_subplot(f, idx, x, y, d.name, d.xlabel, d.ylabel)
        plot.show()

    def save_plot(self):
        f = plot.new_figure((15, 10), 150)
        for idx, d in enumerate(self._data):
            x, y = d.get_data()
            plot.add_to_subplot(f, idx, x, y, d.name, d.xlabel, d.ylabel)

    def adjust_x_vector_from(self, x_start_from):
        for df in self:
            old_x, old_y = df.get_data()
            x_index = min(range(len(old_x)), key=lambda i: abs(old_x[i] - x_start_from))
            x_value = old_x[x_index]
            new_x = [x - x_value for x in old_x]
            df.set_data(new_x[x_index:], old_y[x_index:])

    def adjust_x_vector_to(self, x_start_to):
        for df in self:
            old_x, old_y = df.get_data()
            x_index = min(range(len(old_x)), key=lambda i: abs(old_x[i] - x_start_to))
            x_value = old_x[x_index]
            new_x = [x for x in old_x]
            df.set_data(new_x[:x_index], old_y[:x_index])

