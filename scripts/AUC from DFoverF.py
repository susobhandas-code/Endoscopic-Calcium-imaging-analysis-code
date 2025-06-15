# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 17:44:23 2025

@author: Student
"""

import pandas as pd
import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt

file = r"path_to_your_saved_df_f_excel.xlsx"
df = pd.read_excel(file)

frame_duration = 0.1
start_time = 0
end_time = 4
start_frame = int(start_time / frame_duration)
end_frame = int(end_time / frame_duration)

auc_list = []
for i in range(df.shape[0]):
    row = df.iloc[i, start_frame:end_frame]
    auc = simps(row, dx=frame_duration)
    auc_list.append(auc)

auc_df = pd.DataFrame()
auc_df['Trial'] = np.arange(1, len(auc_list)+1)
auc_df['AUC'] = auc_list

plt.figure(figsize=(8,5))
plt.bar(auc_df['Trial'], auc_df['AUC'], color='skyblue', edgecolor='black')
plt.xlabel("Trial")
plt.ylabel("AUC")
plt.title("AUC of ΔF/F from 0 to 4 seconds")
plt.tight_layout()
plt.show()

auc_df.to_excel("AUC_results.xlsx", index=False)
