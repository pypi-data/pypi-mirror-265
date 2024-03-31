from dataclasses import dataclass
import matplotlib.pyplot as plt
from pathlib import Path
from ..types import Vector, Array
import numpy as np
from typing import TypeVar
from .config import COLOR_CYCLE


# TODO: Optional argument in plot method to prevent postprocessing
@dataclass
class PlotSetup:
    """Plot configuration.

    :param figsize: Size of the figure [(10, 6)]
    :param subplots: Number of subplots as rows and columns [(1, 1)]
    :param right_axis: If True, show right axis [False]
    :param parasite_axis: If True, show parasite axis [False]
    :param top_axis: If True, show top axis [False]
    :param title: Title of the figure [None]
    :param axtitle: Title of the axis [None]
    :param xlabel: Label for the x-axis [None]
    :param tlabel: Label for the top x-axis [None]
    :param ylabel: Label for the y-axis [None]
    :param rlabel: Label for the right y-axis [None]
    :param plabel: Label for the parasite y-axis [None]
    :param zlabel: Label for the z-axis [None]
    :param legend: If True, show legend [False]
    :param xscale: Scale for the x-axis [None]
    :param tscale: Scale for the top x-axis [None]
    :param yscale: Scale for the y-axis [None]
    :param rscale: Scale for the right y-axis [None]
    :param pscale: Scale for the parasite y-axis [None]
    :param zscale: Scale for the z-axis [None]
    :param xlim: Limits for the x-axis [None]
    :param tlim: Limits for the top x-axis [None]
    :param ylim: Limits for the y-axis [None]
    :param rlim: Limits for the right y-axis [None]
    :param plim: Limits for the parasite y-axis [None]
    :param zlim: Limits for the z-axis [None]
    :param grid: If True, show grid [False]
    :param show: If True, show the plot [True]
    :param save: If True, save the plot [False]
    :param dir: Directory to save the plot ["plots"]
    :param name: Name of the file to save with extension [""]
    """

    # Basic figure configuration
    figsize: tuple[float, float] = (8, 4.8)
    subplots: tuple[int, int] = (1, 1)

    # Selection of alternative axes
    right_axis: bool = False
    parasite_axis: bool = False
    top_axis: bool = False

    # Title and labels
    title: str | None = None
    axtitle: str | None = None
    xlabel: str | None = None
    tlabel: str | None = None
    ylabel: str | None = None
    rlabel: str | None = None
    plabel: str | None = None
    zlabel: str | None = None
    legend: bool = True

    # Scales
    xscale: str | None = None
    tscale: str | None = None
    yscale: str | None = None
    rscale: str | None = None
    pscale: str | None = None
    zscale: str | None = None

    # Limits
    xlim: tuple[float, float] | None = None
    tlim: tuple[float, float] | None = None
    ylim: tuple[float, float] | None = None
    rlim: tuple[float, float] | None = None
    plim: tuple[float, float] | None = None
    zlim: tuple[float, float] | None = None

    # Aesthetics
    grid: bool = False

    # Save and show configuration
    show: bool = True
    save: bool = False
    dir: str = "plots"
    name: str = ""

    def copy(self) -> "PlotSetup":
        return PlotSetup(
            figsize=self.figsize,
            subplots=self.subplots,
            right_axis=self.right_axis,
            parasite_axis=self.parasite_axis,
            top_axis=self.top_axis,
            title=self.title,
            axtitle=self.axtitle,
            xlabel=self.xlabel,
            tlabel=self.tlabel,
            ylabel=self.ylabel,
            rlabel=self.rlabel,
            plabel=self.plabel,
            zlabel=self.zlabel,
            legend=self.legend,
            xscale=self.xscale,
            tscale=self.tscale,
            yscale=self.yscale,
            rscale=self.rscale,
            pscale=self.pscale,
            zscale=self.zscale,
            xlim=self.xlim,
            tlim=self.tlim,
            ylim=self.ylim,
            rlim=self.rlim,
            plim=self.plim,
            zlim=self.zlim,
            grid=self.grid,
            show=self.show,
            save=self.save,
            dir=self.dir,
            name=self.name,
        )


T = TypeVar("T", bound="BasePlot")


class BasePlot:

    def __init__(self, setup: PlotSetup = PlotSetup(), _fig=None, _ax=None) -> None:

        self.COLOR_CYCLE = iter(
            [
                "#1f77b4",
                "#aec7e8",
                "#ff7f0e",
                "#ffbb78",
                "#2ca02c",
                "#98df8a",
                "#d62728",
                "#ff9896",
                "#9467bd",
                "#c5b0d5",
                "#8c564b",
                "#c49c94",
                "#e377c2",
                "#f7b6d2",
                "#7f7f7f",
                "#c7c7c7",
                "#bcbd22",
                "#dbdb8d",
                "#17becf",
                "#9edae5",
            ]
        )

        self.setup: PlotSetup = setup

        # Create figure and left axis
        if _fig is None and _ax is None:
            self.fig, self.ax = plt.subplots(
                figsize=self.setup.figsize,
                layout="tight",
            )
        elif _fig is not None and _ax is not None:
            self.fig = _fig
            self.ax = _ax
        else:
            raise ValueError("Provide both figure and axis or none of them")

        # Set title and labels
        if self.setup.title is not None:
            self.fig.suptitle(
                self.setup.title,
                fontsize="x-large",
            )

        if self.setup.axtitle is not None:
            self.ax.set_title(self.setup.axtitle)

        if self.setup.xlabel is not None:
            self.ax.set_xlabel(self.setup.xlabel)
        if self.setup.xscale is not None:
            self.ax.set_xscale(self.setup.xscale)
        if self.setup.xlim is not None:
            self.ax.set_xlim(self.setup.xlim)

        if self.setup.ylabel is not None:
            self.ax.set_ylabel(self.setup.ylabel)
        if self.setup.yscale is not None:
            self.ax.set_yscale(self.setup.yscale)
        if self.setup.ylim is not None:
            self.ax.set_ylim(self.setup.ylim)

        self.path: str = ""

        return None

    def _formatter(self, x, pos):

        if x == 0.0:
            return f"{x:.0f}"
        elif (np.abs(x) > 0.01) and (np.abs(x) < 1e2):
            return f"{x:.1f}"
        else:
            a, b = f"{x:.0e}".split("e")
            bsign = "-" if a[0] == "-" else ""
            esign = "-" if b[0] == "-" else ""
            exp = int(b[1:])
            n = int(a[0]) if bsign == "" else int(a[1])
            return f"{bsign}{n}e{esign}{exp}"
            return f"${bsign}{n}" + r"\cdot 10^{" + f"{esign}{exp}" + r"}$"

    def _postprocess(self) -> None:

        for line in self.ax.get_lines():
            line.set_color(next(self.COLOR_CYCLE))

        return None

    def postprocess(self) -> None:

        self._postprocess()

        # self.ax.yaxis.set_major_formatter(self._formatter)

        labels = self.ax.get_legend_handles_labels()[1]
        if self.setup.legend and len(labels) > 0:
            self.ax.legend()

        if self.setup.grid:
            self.ax.grid()

        if self.setup.save:
            Path(self.setup.dir).mkdir(parents=True, exist_ok=True)
            self.path = f"{self.setup.dir}/{self.setup.name}"
            self.fig.savefig(self.path)

        if self.setup.show:
            plt.show(block=True)
            plt.close(self.fig)

        return None

    def _plot(
        self,
        x: Array,
        y: Array,
        fmt: str | None = "-",
        label: str | None = None,
        axis: str | None = None,
    ) -> None:
        raise NotImplementedError

    def add_line(
        self,
        x: Array,
        y: Array,
        fmt: str | None = "-",
        label: str | None = None,
        axis: str | None = "left",
    ) -> None:
        self._plot(x, y, fmt, label=label, axis=axis)
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.postprocess()

    def __call__(self) -> str:
        self.postprocess()
        return self.path


class SinglePlot(BasePlot):

    def _plot(
        self,
        x: Array,
        y: Array,
        fmt: str | None = "-",
        label: str | None = None,
        axis: str | None = None,
    ) -> None:
        self.ax.plot(x, y, fmt, label=label)
        return None

    def plot(
        self, x: Array, y: Array, fmt: str | None = "-", label: str | None = None
    ) -> str:
        self._plot(x, y, fmt=fmt, label=label)
        return self.__call__()


class DoubleAxis(BasePlot):

    def __init__(self, setup: PlotSetup = PlotSetup(), _fig=None, _ax=None) -> None:

        setup.right_axis = True

        super().__init__(setup, _fig, _ax)

        self.left = self.ax
        self.right = self.left.twinx()

        if self.setup.rlabel is not None:
            self.right.set_ylabel(self.setup.rlabel)
        if self.setup.rscale is not None:
            self.right.set_yscale(self.setup.rscale)
        if self.setup.rlim is not None:
            self.right.set_ylim(self.setup.rlim)

        return None

    def _postprocess(self) -> None:

        super()._postprocess()

        for line in self.right.get_lines():
            line.set_color(next(self.COLOR_CYCLE))
        right_line = self.right.get_lines()[0]
        self.right.yaxis.label.set_color(right_line.get_color())
        self.fig.subplots_adjust(left=0.1, right=0.8)
        self.right.yaxis.set_major_formatter(self._formatter)

        return None

    def _plot(
        self,
        x: Array,
        y: Array,
        fmt: str | None = "-",
        label: str | None = None,
        axis: str | None = None,
    ) -> None:

        if axis == "left":
            self.ax.plot(x, y, fmt, label=label)
        elif axis == "right":
            self.right.plot(x, y, fmt, label=label)
        else:
            raise ValueError("Axis must be either 'left' or 'right'")
        return None

    def plot(self, x: Vector, y_left: Vector, y_right: Vector) -> str:

        self._plot(x, y_left, axis="left")
        self._plot(x, y_right, axis="right")
        return self.__call__()


class ParasiteAxis(BasePlot):

    def __init__(self, setup: PlotSetup = PlotSetup(), _fig=None, _ax=None) -> None:

        setup.right_axis = True
        setup.parasite_axis = True

        super().__init__(setup, _fig, _ax)

        self.left = self.ax
        self.right = self.left.twinx()

        if self.setup.rlabel is not None:
            self.right.set_ylabel(self.setup.rlabel)
        if self.setup.rscale is not None:
            self.right.set_yscale(self.setup.rscale)
        if self.setup.rlim is not None:
            self.right.set_ylim(self.setup.rlim)

        self.parax = self.left.twinx()
        self.parax.spines.right.set_position(("axes", 1.13))

        if self.setup.plabel is not None:
            self.parax.set_ylabel(self.setup.plabel)
        if self.setup.pscale is not None:
            self.parax.set_yscale(self.setup.pscale)
        if self.setup.plim is not None:
            self.parax.set_ylim(self.setup.plim)

        return None

    def _postprocess(self) -> None:

        super()._postprocess()

        for line in self.right.get_lines():
            line.set_color(next(self.COLOR_CYCLE))
        right_line = self.right.get_lines()[0]
        self.right.yaxis.label.set_color(right_line.get_color())
        self.fig.subplots_adjust(left=0.1, right=0.8)
        self.right.yaxis.set_major_formatter(self._formatter)

        for line in self.parax.get_lines():
            line.set_color(next(self.COLOR_CYCLE))
        parax_line = self.parax.get_lines()[0]
        self.parax.yaxis.label.set_color(parax_line.get_color())
        self.parax.yaxis.set_major_formatter(self._formatter)

        return None

    def _plot(
        self,
        x: Array,
        y: Array,
        fmt: str | None = "-",
        label: str | None = None,
        axis: str | None = None,
    ) -> None:

        if axis == "left":
            self.ax.plot(x, y, fmt, label=label)
        elif axis == "right":
            self.right.plot(x, y, fmt, label=label)
        elif axis == "parax":
            self.parax.plot(x, y, fmt, label=label)
        else:
            raise ValueError("Axis must be either 'left', 'right' or 'parax'")
        return None

    def plot(self, x: Vector, y_left: Vector, y_right: Vector, y_parax: Vector) -> str:

        self._plot(x, y_left, axis="left")
        self._plot(x, y_right, axis="right")
        self._plot(x, y_parax, axis="parax")
        return self.__call__()


class MultiPlot:

    def __init__(self, setup: PlotSetup) -> None:

        self.setup = setup

        if self.setup.subplots == (1, 1):
            raise ValueError("Requesting a single plot with MultiPlot")

        self.rows, self.cols = self.setup.subplots

        self.fig, self.axes = plt.subplots(
            self.rows, self.cols, figsize=self.setup.figsize, layout="tight"
        )

        self.ax_list = iter(self.axes.ravel())

        if self.setup.title is not None:
            self.fig.suptitle(self.setup.title, fontsize="x-large")

        self.path = ""

        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.postprocess()
        return None

    def add_plot(self, setup: PlotSetup = PlotSetup(), type: type[T] = SinglePlot) -> T:
        setup.show = False
        setup.save = False
        setup.legend = True if self.setup.legend else False
        return type(setup, _fig=self.fig, _ax=next(self.ax_list))

    def postprocess(self) -> str:

        if self.setup.save:
            Path(self.setup.dir).mkdir(parents=True, exist_ok=True)
            self.path = f"{self.setup.dir}/{self.setup.name}"
            self.fig.savefig(self.path)
            if not self.setup.show:
                plt.close(self.fig)

        if self.setup.show:
            plt.show(block=True)
            plt.close(self.fig)

        return self.path

    def __call__(self) -> str:
        self.postprocess()
        return self.path


class Base3D:

    def __init__(self, setup: PlotSetup = PlotSetup()) -> None:

        self.setup = setup

        # Create figure and axis
        self.fig = plt.figure(figsize=self.setup.figsize)
        self.ax = self.fig.add_subplot(
            projection="3d", proj_type="ortho", box_aspect=(1, 1, 1)
        )

        # Set title and labels
        if self.setup.title is not None:
            self.fig.suptitle(self.setup.title, fontsize="x-large")

        if self.setup.xlabel is not None:
            self.ax.set_xlabel(self.setup.xlabel)
        if self.setup.xscale is not None:
            self.ax.set_xscale(self.setup.xscale)
        if self.setup.xlim is not None:
            self.ax.set_xlim(self.setup.xlim)

        if self.setup.ylabel is not None:
            self.ax.set_ylabel(self.setup.ylabel)
        if self.setup.yscale is not None:
            self.ax.set_yscale(self.setup.yscale)
        if self.setup.ylim is not None:
            self.ax.set_ylim(self.setup.ylim)

        if self.setup.zlabel is not None:
            self.ax.set_zlabel(self.setup.zlabel)  # type: ignore
        if self.setup.zscale is not None:
            self.ax.set_zscale(self.setup.zscale)  # type: ignore
        if self.setup.zlim is not None:
            self.ax.set_zlim(self.setup.zlim)  # type: ignore

        self.path = ""

        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.postprocess()

    def add_line(
        self, x: Array, y: Array, z: Array, fmt: str = "-", label: str | None = None
    ) -> None:

        self.ax.plot(x, y, z, fmt, label=label)

        return None

    def postprocess(self) -> str:

        original_limits = np.array(
            [
                self.ax.get_xlim(),
                self.ax.get_ylim(),
                self.ax.get_zlim(),  # type: ignore
            ]
        ).T

        homogeneous_limits = (np.min(original_limits[0]), np.max(original_limits[1]))

        self.ax.set_xlim(homogeneous_limits)
        self.ax.set_ylim(homogeneous_limits)
        self.ax.set_zlim(homogeneous_limits)  # type: ignore

        labels = self.ax.get_legend_handles_labels()[1]
        if self.setup.legend and len(labels) > 0:
            self.ax.legend()

        if self.setup.save:
            Path(self.setup.dir).mkdir(parents=True, exist_ok=True)
            self.path = f"{self.setup.dir}/{self.setup.name}"
            self.fig.savefig(self.path)

        if self.setup.show:
            plt.show(block=True)
            plt.close(self.fig)

        return self.path


class Plot3D(Base3D):

    def plot(
        self, x: Array, y: Array, z: Array, fmt: str = "-", label: str | None = None
    ) -> str:
        self.add_line(x, y, z, fmt=fmt, label=label)
        self.postprocess()
        return self.path
