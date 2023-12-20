import pandas as pd

def cut_frequency_range_and_save(csv_file):
    ecg_data = pd.read_csv(csv_file)
    time = ecg_data.iloc[:, 0].values
    signal = ecg_data.iloc[:, 1].values
    signal += 1

    output_data = pd.DataFrame({'Time': time, 'Signal': signal})
    output_data.to_csv("dataset\ECG\\normal_output.csv", index=False)
    print("output")

ecg_csv_file = "dataset\ECG\\normal.csv"
cut_frequency_range_and_save(ecg_csv_file)

