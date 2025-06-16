# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 23:02:44 2025

@author: susob
"""

import pandas as pd
import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt

tiff_file = ""
save_df_f = ""
trial_time = 10 
frame_duration = .1
frame_per_trial = int(trial_time/frame_duration)
baseline_duration = 1.2
frame_during_baseline = int(baseline_duration/frame_duration)

image_information = tiff.imread(tiff_file)
total_frame = image_information.shape[0]
number_of_trial = int(total_frame/frame_per_trial)

dff_trials= []
for i in range(number_of_trial):
    start_trial_frmes = i*frame_per_trial
    end_trial_frames = start_trial_frmes + start_trial_frmes
    stack_of_trials = image_information[start_trial_frmes:end_trial_frames]
    
    trial_pixel_mean = stack_of_trials.mean(axis=(1,2))
    baseline_mean = trial_pixel_mean[:frame_during_baseline].mean()
    dff = (trial_pixel_mean - baseline_mean) / baseline_mean
    dff_trials.append(dff)
    
df_dff = pd.DataFrame(dff_trials)
df_dff.to_excel(save_df_f, index=False)
mean_dff = np.mean(dff_trials, axis=0)
sem_dff = np.std(dff_trials, axis=0) / np.sqrt(len(dff_trials))

time_axis = np.arange(0, frame_per_trial) * frame_duration
plt.figure(figsize=(10, 5))
plt.plot(time_axis, mean_dff, label='Mean ΔF/F', color='blue')
plt.fill_between(time_axis, mean_dff - sem_dff, mean_dff + sem_dff, alpha=0.3, color='blue', label='SEM')

# Mark stimulus window
plt.axvline(x=1.2, color='red', linestyle='--', label='Stimulus Onset (1.2s)')
plt.axvline(x=3.2, color='green', linestyle='--', label='Stimulus End (3.2s)')

plt.title("Average ΔF/F Trace (200 ms trimmed)")
plt.xlabel("Time (s)")
plt.ylabel("ΔF/F")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()