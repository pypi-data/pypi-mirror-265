"""This module is made to make graphs of all sorts, and standardize them so i can use them everywhere. The library
will always be available to copy the code from anyway. So i can always modify the code, but atleast there will be a
set template of all the graphs that I may need. I will use any module that I think looks good here."""

import numpy as np
import matplotlib.pyplot as plt


class ColorScheme:
    """Contains color scheme data."""

    def __init__(self, name, primary, secondary, accent, background, text) -> None:
        self.primary = primary
        self.secondary = secondary
        self.accent = accent
        self.background = background
        self.text = text
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} color scheme"


class ColorSchemes:
    """
    This class contains different color schemes that have a primary, secondary, accent, background and text color. Each Scheme has a name.
    """

    def __init__(self):
        self.schemes = [
            ColorScheme("Dark", "#1F1F1F", "#2D2D2D", "#FFD700", "#000000", "#FFFFFF"),
            ColorScheme("Light", "#FFFFFF", "#F0F0F0", "#FFD700", "#FFFFFF", "#000000"),
            ColorScheme("Blue", "#0000FF", "#0000A0", "#FFD700", "#FFFFFF", "#000000"),
            ColorScheme("Green", "#00FF00", "#00A000", "#FFD700", "#FFFFFF", "#000000"),
            ColorScheme("Red", "#FF0000", "#A00000", "#FFD700", "#FFFFFF", "#000000"),
            ColorScheme(
                "Yellow", "#FFFF00", "#A0A000", "#FFD700", "#FFFFFF", "#000000"
            ),
            ColorScheme(
                "Purple", "#800080", "#600060", "#FFD700", "#FFFFFF", "#000000"
            ),
            ColorScheme(
                "Orange", "#FFA500", "#A06000", "#FFD700", "#FFFFFF", "#000000"
            ),
            ColorScheme("Cyan", "#00FFFF", "#00A0A0", "#FFD700", "#FFFFFF", "#000000"),
            ColorScheme("Pink", "#FFC0CB", "#A06070", "#FFD700", "#FFFFFF", "#000000"),
            ColorScheme("Brown", "#A52A2A", "#802020", "#FFD700", "#FFFFFF", "#000000"),
            ColorScheme("Grey", "#808080", "#606060", "#FFD700", "#FFFFFF", "#000000"),
            ColorScheme("Black", "#000000", "#000000", "#FFD700", "#FFFFFF", "#000000"),
            ColorScheme("White", "#FFFFFF", "#FFFFFF", "#FFD700", "#FFFFFF", "#000000"),
            ColorScheme(
                "Default", "#FFFFFF", "#F0F0F0", "#FFD700", "#FFFFFF", "#000000"
            ),
        ]
        self.dark = self.schemes[0]
        self.light = self.schemes[1]
        self.blue = self.schemes[2]
        self.green = self.schemes[3]
        self.red = self.schemes[4]
        self.yellow = self.schemes[5]
        self.purple = self.schemes[6]
        self.orange = self.schemes[7]
        self.cyan = self.schemes[8]
        self.pink = self.schemes[9]
        self.brown = self.schemes[10]
        self.grey = self.schemes[11]
        self.black = self.schemes[12]
        self.white = self.schemes[13]
        self.default = self.schemes[14]
        self.random = np.random.choice(self.schemes)

    def get_schemes(self):
        return self.schemes

    def get_scheme(self, name):
        for scheme in self.schemes:
            if scheme.name == name:
                return scheme

    def get_random(self):
        return np.random.choice(self.schemes)


class Basics:
    def __init__(
        self,
        matplotlib_style="default",
        code_font_family="Jetbrains Mono",
        text_font_family="PT Sans",
        color_scheme="default",
    ):
        self.good_fonts_for_text = [
            "PT Sans",
            "Open Sans",
            "Caecilia Light",
            "Product Sans Light",
        ]  # these are font families, not fonts

        # get all color schemes from ColorSchemes.py
        self.color_schemes = ColorSchemes()

        # now for this class, and this instance, set the color scheme that was specified by the user.
        self.color_scheme = self.color_schemes.get_scheme(color_scheme)

        plt.style.use(matplotlib_style)
        self.matplotlib_style = matplotlib_style
        self.code_font_family = code_font_family
        self.text_font_family = text_font_family
        if code_font_family == "random":
            self.code_font_family = np.random.choice(self.good_fonts_for_text)
        if text_font_family == "random":
            self.text_font_family = np.random.choice(self.good_fonts_for_text)

        plt.rcParams["font.family"] = self.text_font_family

    # getters
    def get_fonts(self):
        print(plt.rcParams["font.family"])
        return plt.rcParams["font.family"]


class BasicGraphs(Basics):
    """Contains graphs for Line, Bar, Pie, and Scatter plots"""

    def __init__(
        self,
        matplotlib_style="default",
        code_font_family="Jetbrains Mono",
        text_font_family="PT Sans",
        color_scheme="default",
    ):
        print("Thank you for using KPT Graphs!")
        super().__init__(
            matplotlib_style,
            code_font_family=code_font_family,
            text_font_family=text_font_family,
            color_scheme=color_scheme,
        )

    def line_plot(
        self, x, y, title, subtitle, xlabel, ylabel, color_scheme, size=(10, 6)
    ) -> tuple:
        """Creates a line plot with the given data
        and then returns the figure and axis objects.
        """

        # first create the line plot
        fig, ax = plt.subplots(figsize=size)
        ax.plot(x, y, color=self.color_scheme.primary)

        # now formatting

        # axes

        # tilt the x-axis labels by 45 degrees
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)

        # set the font size of the tick labels
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(16)
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(16)

        # title

        # add title + subtitle to plot
        plt.text(
            x=0.125,
            y=0.90,
            s=title,
            fontname=self.text_font_family,
            fontsize=24,
            ha="left",
            transform=fig.transFigure,
        )

        plt.text(
            x=0.125,
            y=0.86,
            s=subtitle,
            fontname=self.text_font_family,
            fontsize=18,
            ha="left",
            transform=fig.transFigure,
        )

        # line between titles and chart
        plt.gca().plot(
            [0.125, 0.9],  # x co-ords
            [0.80, 0.80],  # y co-ords
            transform=fig.transFigure,
            clip_on=False,
            color="k",
            linewidth=1.5,
        )

        # set the x and y labels
        ax.tick_params(axis="both", which="major", labelsize=16)
        plt.xlabel(xlabel, fontsize=20, fontname=self.text_font_family)
        plt.ylabel(ylabel, fontsize=20, fontname=self.text_font_family)

        # grid lines
        # keep only toned down vertical lines
        plt.grid(axis="y", alpha=0.4)
        plt.grid(axis="x", alpha=0.2)

        # turn off spines
        plt.gca().spines[["left", "right", "top"]].set_visible(False)

        # change space on top of chart we are actually adjusting the scale of the plot as well.
        plt.subplots_adjust(top=0.8, wspace=0.3)

        # return everything to the user
        return fig, ax

    def test(self):
        print("This is a test")
        return 1


def test():
    print("This is a test")
    return 1
