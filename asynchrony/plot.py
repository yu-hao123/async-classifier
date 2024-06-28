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
    The pressure, flow and pmus waveforms are plotted in sequence.
    The user still needs to apply/manage plt.show()

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

    # Set x-ticks every second
    # axs[-1].xaxis.set_major_locator(ticker.MultipleLocator(base=1))

    # Set x-tick labels every 10 seconds
    #axs[-1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: int(x) if int(x) % 10 == 0 else ''))

    # Set ticks every 10 seconds
    axs[-1].set_xticks(np.arange(time[0], time[-1], 10))
    # Set non-labeled ticks every 1 second
    axs[-1].set_xticks(np.arange(time[0], time[-1], 1), minor=True)

    for ax in axs:
        ax.yaxis.grid(True)
        ax.xaxis.grid(True, which='major', linestyle='-')
        ax.xaxis.grid(True, which='minor', linestyle=':', color=[0.5, 0.5, 0.5])

    fig.align_ylabels(axs)

    # Adjust layout to prevent overlap
    plt.tight_layout()

    return fig, axs