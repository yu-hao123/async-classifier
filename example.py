import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from asynchronyClassifier import plot_raw_data, find_ineffective_effort, find_auto_trigger

def write_ventilation_csv(
        time : list,
        pressure : list,
        flow : list,
        volume : list,
        pmus : list,
        file_path : str
        ) -> bool:
    """
    Write time, pressure, flow, volume and pmus samples to a CSV file.
    The first line of the CSV will be the dataset fieldnames.

    Returns:
    - bool: True if successfully written to the file, False otherwise.
    """
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['time', 'pressure', 'flow', 'volume', 'pmus'])  # Write header
            for t, p, f, v, pm in zip(time, pressure, flow, volume, pmus):
                writer.writerow([t, p, f, v, pm])
        print(f'Data successfully written to {file_path}')
        return True
    except Exception as e:
        print(f'Error: {e}')
        return False


def read_csv(file_path : str) -> dict:
    """
    Read data from a CSV file and store it in NumPy arrays within a dictionary.
    The first line of the CSV should be the dataset fieldnames.

    Parameters:
    - file_path: The path to the CSV file.

    Returns:
    - dict: A dictionary containing NumPy arrays with fieldnames as keys.
    """
    data = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)  # Automatically uses the first row as fieldnames
        for key in reader.fieldnames:
            data[key] = []
        for row in reader:
            for key in reader.fieldnames:
                data[key].append(float(row[key]))
    for key in data:
        data[key] = np.array(data[key])
    return data


def retrieve_parity_marks(volume_times_ten : np.ndarray):
    """
    Analyze parity of a volume waveform in order to determine the respiratory
    inspiration and expiration marks.
    This is a particularity of the FlexiMag ventilator.

    Parameters:
    - volume_times_ten: The array that stores all the volume samples multiplied by ten
                        The parity will be analyzed in integer values

    Returns:
    - ins_marks (np.ndarray) : Array conteining the waveform inspiration marks.
    - exp_marks (np.ndarray) : Array conteining the waveform expiration marks.
    """
    ins_marks = []
    exp_marks = []

    v = [int(el) for el in volume_times_ten]

    parity = v[0] % 2
    for i in range(1, len(v)):
        new_parity = v[i] % 2
        if (new_parity != parity and parity == 0):
            ins_marks.append(i)
        elif (new_parity != parity and parity == 1):
            exp_marks.append(i)
        parity = new_parity

    return ins_marks, exp_marks

# HARDCODED CONSTANTS, WILL BE REFACTORED LATER
def retrieve_pmus_marks(pmus : np.ndarray):
    """
    Calculates the start, peak and finish cycle marks of a pmus waveform.

    Parameters:
    - pmus: The array that stores all the pmus samples

    Returns:
    - start_marks (np.ndarray) : Array conteining the pmus start indexes.
    - peak_marks (np.ndarray) : Array conteining the pmus peak indexes.
    - finish_marks (np.ndarray) : Array conteining the pmus finish indexes.
    """
    start_marks = [1]
    finish_marks = [1]
    peak_marks = []

    for i in range(len(pmus) - 15):
        if (-pmus[i] < 0.1 and -pmus[i + 10] > 0.2 and (i - start_marks[-1]) > 50):
            start_marks.append(i)
        if (-pmus[i] > 0.2 and -pmus[i + 10] < 0.1 and (i - finish_marks[-1]) > 50):
            finish_marks.append(i + 10)

    start_marks = start_marks[1:]
    finish_marks = finish_marks[1:]

    # The first mark as a convention is the inspiration mark
    if (finish_marks[0] <= start_marks[0]):
        finish_marks = finish_marks[1:]

    # guarantee that marks array have the same size
    if (len(start_marks) > len(finish_marks)):
        start_marks = start_marks[1:-1]

    for i in range(len(start_marks)):
        index = np.argmin(pmus[start_marks[i]:finish_marks[i]])
        peak_marks.append(start_marks[i] + index)

    return start_marks, peak_marks, finish_marks

def main():
    csv_data = read_csv('coletavcv_adequate.csv')
    vtable = pd.DataFrame(csv_data)
    interval = np.arange(55400, 60800)
    cut_table = vtable.iloc[interval]

    time = cut_table['time'].values
    pressure = cut_table['pressure'].values
    flow = cut_table['flow'].values
    pmus = cut_table['pmus'].values
    volume = cut_table['volume'].values

    fig, axs = plot_raw_data(time, pressure, flow, pmus)
    plt.show(block=False)

    ins_marks, exp_marks = retrieve_parity_marks(volume * 10)
    pmus_start_marks, pmus_peak_marks, pmus_finish_marks = retrieve_pmus_marks(pmus)

    fig, axs = plot_raw_data(time, pressure, flow, pmus)
    fmin = min(flow)
    fmax = max(flow)
    for mark in ins_marks:
        axs[1].plot([time[mark], time[mark]], [fmin, fmax], 'b--', linewidth=1.5)

    for mark in exp_marks:
        axs[1].plot([time[mark], time[mark]], [fmin, fmax], 'r--', linewidth=1.5)

    axs[2].scatter(
        [time[i] for i in pmus_start_marks],
        [pmus[i] for i in pmus_start_marks],
        color='b',
        marker='^',
        s=64
    )
    axs[2].scatter(
        [time[i] for i in pmus_peak_marks],
        [pmus[i] for i in pmus_peak_marks],
        color='k',
        marker='*',
        s=64
    )
    axs[2].scatter(
        [time[i] for i in pmus_finish_marks],
        [pmus[i] for i in pmus_finish_marks],
        color='r',
        marker='v',
        s=64
    )

    iee_indexes = find_ineffective_effort(ins_marks, exp_marks, pmus_start_marks, pmus_finish_marks)
    for iee in iee_indexes:
        axs[2].text(time[iee], -5.0, 'IEE', color='black', fontsize=14, fontweight='semibold')

    att_indexes = find_auto_trigger(ins_marks, exp_marks, pmus_start_marks, pmus_finish_marks)
    for att in att_indexes:
        axs[1].text(time[att], -5.0, 'ATT', color='black', fontsize=14, fontweight='semibold')

    plt.show()


if __name__ == "__main__":
    main()