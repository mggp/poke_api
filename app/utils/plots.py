import io
from typing import Iterable

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def get_histogram(frequency, xlabel=None, ylabel=None) -> bytes:
    """Generate a histogram from frequency data."""

    labels = list(frequency.keys())
    values = list(frequency.values())

    fig, ax = plt.subplots()

    plot_bar_chart(ax, labels, values, xlabel=xlabel, ylabel=ylabel)
    buf = get_buffer(plt)

    plt.close(fig)

    return buf.read()


def plot_bar_chart(
    ax: Axes, labels: Iterable, values: Iterable, xlabel: str = None, ylabel: str = None
) -> bytes:
    """Generate a bar chart from data."""
    ax.bar(labels, values)
    ax.set_xlabel(xlabel or "X-axis")
    ax.set_ylabel(ylabel or "Y-axis")


def get_buffer(fig: Figure, output_format: str = "png") -> io.BytesIO:
    """Get the buffer from the current figure."""
    buf = io.BytesIO()
    fig.savefig(buf, format=output_format)
    buf.seek(0)

    return buf
