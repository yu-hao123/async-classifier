import matplotlib.pyplot as plt
import matplotlib.figure
import numpy as np


def plot_raw_data(
        time : list,
        pressure : list,
        flow : list,
        pmus : list
        ):
    """
    Creates a 3-subplot figure using Matplotlib to visualize the raw ventilation data.

    Returns:
    - fig (matplotlib.figure.Figure): The top-level container representing the whole figure.
    - axs (numpy.ndarray): A 1-D array of Axes objects representing the individual subplots.

    """

    # Plotting
    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(12, 6))  # 3 rows, 1 column

    axs[0].plot(time, pressure)
    axs[0].set_ylabel('Pressure')

    axs[1].plot(time, flow)
    axs[1].set_ylabel('Flow')

    axs[2].plot(time, pmus)
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Pmus')

    for ax in axs:
        ax.grid(True)
    fig.align_ylabels(axs)

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()

    return fig, axs