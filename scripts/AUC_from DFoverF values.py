# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 15:01:09 2025

@author: Student
"""

import pandas as pd
import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt
import os

# Load the Excel file
file_path = r"E:\suso\multimodal_integration\headrestrained\calcium Imaging\GCaMP_MMD_IAA_grp2\anesthetized\Airflow\airflow_Anesthetized.xlsx"
excel_data = pd.ExcelFile(file_path)

# Get the directory of the input file
output_dir = os.path.dirname(file_path)

# Define constants
FRAME_DURATION = 0.1  # Each column represents 100 ms
START_TIME = 0  # Start time for AUC calculation
END_TIME = 4  # End time for AUC calculation
START_FRAME = int(START_TIME / FRAME_DURATION)  # Start frame for AUC calculation
END_FRAME = int(END_TIME / FRAME_DURATION)  # End frame for AUC calculation

# Function for z-score normalization
def z_score_normalize(df):
    df_mean = np.expand_dims(df.mean(axis=1).values, axis=1)  # Convert to NumPy and expand dimensions
    df_std = np.expand_dims(df.std(axis=1).values, axis=1)    # Convert to NumPy and expand dimensions
    return (df - df_mean) / df_std

# DataFrame to store AUC results for all sheets
summary_auc = []
trial_auc_sheets = {}  # Dictionary to store trial-wise AUC for each sheet

# Iterate through each sheet and calculate AUC
for sheet in excel_data.sheet_names:
    # Load the sheet data
    df = excel_data.parse(sheet)

    # Ensure only numeric data is used
    numeric_df = df.select_dtypes(include=[np.number])

    # Perform z-score normalization
    z_normalized_df = z_score_normalize(numeric_df)

    # Calculate the baseline (mean over the first 1 second of the trial)
    baseline = z_normalized_df.iloc[:, :int(1 / FRAME_DURATION)].mean(axis=1)

    # Calculate AUC for each trial relative to the baseline
    auc_values = []
    for index, row in z_normalized_df.iterrows():
        time = np.arange(0, len(row) * FRAME_DURATION, FRAME_DURATION)  # Time vector
        # Subtract baseline from the curve
        baseline_corrected = row.iloc[START_FRAME:END_FRAME] - baseline[index]
        # Integrate the baseline-corrected curve
        auc = simps(baseline_corrected, dx=FRAME_DURATION)
        auc_values.append(auc)

    # Store trial-wise AUCs in a DataFrame
    trial_auc_df = pd.DataFrame({
        'Trial': numeric_df.index,
        'AUC': auc_values
    })
    trial_auc_sheets[sheet] = trial_auc_df  # Store DataFrame in dictionary

    # Calculate mean and SEM for the current sheet
    mean_auc = np.mean(auc_values)
    sem_auc = np.std(auc_values) / np.sqrt(len(auc_values))

    # Store the results
    summary_auc.append({'Sheet': sheet, 'Mean AUC': mean_auc, 'SEM AUC': sem_auc})

# Convert summary results to a DataFrame
summary_df = pd.DataFrame(summary_auc)

# Plot average AUC with standard error
plt.figure(figsize=(10, 6))
plt.bar(summary_df['Sheet'], summary_df['Mean AUC'], yerr=summary_df['SEM AUC'], capsize=5, color='skyblue', edgecolor='black')
plt.title("Average Baseline-Corrected AUC (0-4 seconds) with Standard Error Across Sheets", fontsize=16)
plt.xlabel("Sheets", fontsize=12)
plt.ylabel("Average AUC (Baseline-Corrected, 0-4 seconds)", fontsize=12)
plt.tight_layout()
output_plot_path = os.path.join(output_dir, "Average_Baseline_Corrected_AUC_0_to_4_seconds_with_SEM.png")
plt.savefig(output_plot_path, dpi=300)
plt.show()

# Save the summary results to an Excel file
summary_output_path = os.path.join(output_dir, "Summary_Baseline_Corrected_AUC_0_to_4_seconds.xlsx")
summary_df.to_excel(summary_output_path, index=False)

# Save trial-wise AUC values to separate sheets in an Excel file
trial_auc_output_path = os.path.join(output_dir, "Trial_Wise_AUC_Values.xlsx")
with pd.ExcelWriter(trial_auc_output_path, engine='xlsxwriter') as writer:
    for sheet_name, auc_df in trial_auc_sheets.items():
        auc_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Baseline-Corrected AUC analysis (0-4 seconds) complete. Summary results saved to '{summary_output_path}'.")
print(f"Trial-wise AUC values saved to separate sheets in '{trial_auc_output_path}'.")
