import csv
import matplotlib.pyplot as plt
import numpy as np

from asynchronyClassifier import plot_raw_data

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


def main():
    csv_data = read_csv('coletavcv_adequate.csv')
    plot_raw_data(
        csv_data['time'],
        csv_data['pressure'],
        csv_data['flow'],
        csv_data['pmus']
    )


if __name__ == "__main__":
    main()