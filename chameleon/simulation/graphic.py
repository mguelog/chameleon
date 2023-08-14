from chameleon import CYCLE_LOG
from pandas import read_csv
from numpy import isnan
from matplotlib import pyplot as plt


class Graphic:

    def __init__(self, title, x_axis, y_axes):
        self.generated = False
        self.title = title
        self.x_axis = x_axis
        self.y_axes = y_axes

    def draw(self):
        data = read_csv(CYCLE_LOG)

        x = data[[self.x_axis[0]]].values
        x = (x[~isnan(x).any(axis=1)])

        y = [None] * len(self.y_axes)

        for i in range(len(self.y_axes)):
            y[i] = data[[self.y_axes[i][0]]]
            y[i] = (y[i][~isnan(y[i]).any(axis=1)])
            plt.plot(x, y[i], self.y_axes[i][1], label=self.y_axes[i][2])

        if not self.generated:
            plt.title(self.title)
            plt.xlabel(self.x_axis[2])
            plt.legend(loc="upper left")

        plt.ion()
        plt.show(block=False)
        plt.pause(0.1)

        self.generated = True
