import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = r"F:\analysis\dfoverf.xlsx"
df = pd.read_excel(file_path)

df = df.iloc[:, :90]

mean_dff = df.mean(axis=0).values
time_axis = np.arange(len(mean_dff)) * 0.1

peak_idx = np.argmax(mean_dff)
peak_amplitude = mean_dff[peak_idx]
time_to_peak = time_axis[peak_idx]

baseline = mean_dff[:12].mean()
one_third_height = baseline + (peak_amplitude - baseline) / 3

decay_idx = None
for i in range(peak_idx, len(mean_dff)):
    if mean_dff[i] <= one_third_height:
        decay_idx = i
        break

if decay_idx is not None:
    decay_time = time_axis[decay_idx] - time_axis[peak_idx]
else:
    decay_time = np.nan

plt.figure(figsize=(10, 5))
plt.plot(time_axis, mean_dff, label="Mean ΔF/F", color='blue')
plt.scatter(time_axis[peak_idx], peak_amplitude, color='red', zorder=5)
plt.axvline(x=time_axis[peak_idx], color='red', linestyle='--', label=f"Peak ({time_to_peak:.2f}s)")
if decay_idx is not None:
    plt.axvline(x=time_axis[decay_idx], color='green', linestyle='--', label=f"Decay ({time_axis[decay_idx]:.2f}s)")

text_x = time_axis[peak_idx] + 1
text_y = peak_amplitude

text = (
    f"Peak Amplitude: {peak_amplitude:.3f}\n"
    f"Time to Peak: {time_to_peak:.3f} s\n"
    f"Decay Time: {decay_time:.3f} s"
)
plt.text(text_x, text_y, text, fontsize=10, bbox=dict(facecolor='white', edgecolor='black'))

plt.xlabel("Time (s)")
plt.ylabel("ΔF/F")
plt.title("Mean ΔF/F with Peak and Decay Info")
plt.legend()
plt.tight_layout()
plt.show()
