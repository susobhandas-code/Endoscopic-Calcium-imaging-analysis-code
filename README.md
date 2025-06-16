# Endoscopic-Calcium-imaging-analysis-code
## Tiff file analysis recorded from endoscopic calcium imaging experiment

Endoscpic calcium imaging from mice brain: Endoscopic calcium imaging enables high-resolution recording of neural activity from deep brain structures in behaving animals. This technique employs genetically encoded calcium indicators (such as GCaMP) to detect intracellular calcium transients associated with neuronal activity. A gradient-index (GRIN) lens is surgically implanted to relay fluorescence signals from the targeted brain region to a head-mounted miniature epifluorescence microscope (miniscope). The resulting time-series data allows for the analysis of population dynamics of identified neurons during naturalistic behaviors, offering a powerful approach for dissecting circuit-level mechanisms underlying sensory processing, learning, and decision-making.

TIFF File Info: The calcium imaging TIFF file contains multiple grayscale frames acquired at 10 Hz with a 100 ms exposure per frame using GCaMP6f in the mouse olfactory bulb. Image dimensions are 512×512 pixels, and acquisition was performed using Doric Neuroscience Studio software. No preprocessing was applied before ΔF/F analysis.

Scripts: 
1. dfoverf_calculation.py
This script computes trial-wise ΔF/F (delta F over F) values from calcium imaging TIFF stacks. It segments the entire recording into trials based on fixed duration, calculates baseline fluorescence (F₀) from a pre-stimulus period, and normalizes the signal accordingly. The resulting ΔF/F traces are exported to Excel for downstream analysis.

2. heatmap_plot.py
This script loads the ΔF/F data and visualizes trial-wise activity as a heatmap. Each row represents one trial, and color intensity reflects fluorescence changes over time. This allows quick visual assessment of stimulus-evoked population responses across trials.

3. auc_analysis.py
This script calculates the area under the ΔF/F curve (AUC) during specific time windows (e.g., 3–5 s, 5–9 s, 9–11 s) for each trial. It normalizes AUC per second and plots grouped bar plots for comparative analysis. Statistical comparisons (paired t-test) are included to evaluate differences across time windows.

4. peak_parameters.py
This script extracts peak-related parameters from the averaged ΔF/F trace across all trials. It computes:

Peak amplitude

Time to peak

Decay time to one-third peak height
