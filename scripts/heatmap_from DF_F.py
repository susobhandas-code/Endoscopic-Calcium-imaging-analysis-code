# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 17:40:56 2025

@author: Student
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_excel(r"F:\analysis\dfoverf.xlsx")
df_z = (df - df.mean(axis=1).values.reshape(-1,1)) / df.std(axis=1).values.reshape(-1,1)
df_z['avg'] = df_z.mean(axis=1)
df_sorted = df_z.sort_values('avg').drop('avg', axis=1)

plt.figure(figsize=(10,6))
sns.heatmap(df_sorted, cmap='viridis', cbar_kws={'label': 'Z-scored ΔF/F'})
plt.axvline(30, color='red', linestyle='--')
plt.axvline(50, color='red', linestyle='--')
plt.axvline(90, color='red', linestyle='--')
plt.axvline(110, color='red', linestyle='--')
plt.xlabel('Time (frames)')
plt.ylabel('Trials')
plt.title('ΔF/F Heatmap')
plt.tight_layout()
plt.show()
