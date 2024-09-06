""" Created on Fri Sep 09 14:59:34 2024 @author: Doris Santiago"""
#https://support.moleculardevices.com/s/article/Membrane-Test-Algorithms .
#This code was generated as pyabf.tools.memtest wasnt functioning as needed 

import pyabf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

fn = r'your file path.abf'
# print(abf.headerText) 
abf = pyabf.ABF(fn)
fs = abf.sampleRate
channel = abf.sweepChannel
time = abf.sweepX
current = abf.sweepY
membranepotential =abf.sweepC
samp_fs = abf.dataRate 
DigOutput = abf.sweepD(0)

#Extract epochs from the dataset
sweep_epochs = str(abf.sweepEpochs)
pattern = r"Step ([\-\d\.]+) \[(\d+):(\d+)\]"           # Extract all matches for Step value and [start:end] positions
matches = re.findall(pattern, sweep_epochs)

# Create a list of dictionaries for the DataFrame
data1 = []
for match in matches:
    step_value = float(match[0])
    start_value = int(match[1])
    end_value = int(match[2])
    difference = end_value - start_value
    data1.append({"step": step_value, "start": start_value, "end": end_value, "difference(ms)": difference})

# new DataFrame for digital output
df_D0 = pd.DataFrame(data1)
print(df_D0)

#Extracting timepoint with Step Current
extracted_df_D0 = df_D0[df_D0['step'] == -10.0]      # -10mV is the pulse given in my system
# Extract the start and end values
start_end_values = extracted_df_D0[['step','start', 'end']]
print(start_end_values)


#Define Parameters for MEMBRANE TEST
PulseWidth1 = start_end_values.iloc[0]['end']-start_end_values.iloc[0]['start']
PulseWidth2 = start_end_values.iloc[1]['end']-start_end_values.iloc[1]['start']

# Pulse Period is defined as Analysis Window
AnalysisWindow1_start = start_end_values.iloc[0]['start']
AnalysisWindow1_end = start_end_values.iloc[0]['end'] + PulseWidth1
AnalysisWindow2_start = start_end_values.iloc[1]['start']
AnalysisWindow2_end = start_end_values.iloc[1]['end'] + PulseWidth2

PulsePeriod1 = time[int(start_end_values.iloc[0]['start']): int(AnalysisWindow1_end)]
PulsePeriod2 = time[int(start_end_values.iloc[1]['start']): int(AnalysisWindow2_end)]

CurrentInPulsePeriod1 = current[int(start_end_values.iloc[0]['start']): int(AnalysisWindow1_end)]
CurrentInPulsePeriod2 = current[int(start_end_values.iloc[1]['start']): int(AnalysisWindow2_end)]

StimulusInPulsePeriod1 = membranepotential[int(start_end_values.iloc[0]['start']): int(AnalysisWindow1_end)]
StimulusInPulsePeriod2 = membranepotential[int(start_end_values.iloc[1]['start']): int(AnalysisWindow2_end)]

# #VISULIZE WHAT YOU EXTRACT:  Check the data with plots
# =============================================================================
# #METHOD 1 : INDIVIDUAL PLOTS
# =============================================================================
'''AT THE START'''
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
plt.title ('Membrane Test ')
axs[0, 0].plot(PulsePeriod1, StimulusInPulsePeriod1, label='Stimulus', color='orange')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Stimulus')
axs[0, 0].set_title('Stimulus vs Time (Start)')
axs[0, 0].legend()
axs[0, 0].grid(True)

axs[0, 1 ].plot(PulsePeriod1, CurrentInPulsePeriod1, label='Current')
axs[0, 1 ].set_xlabel('Time (s)')
axs[0, 1 ].set_ylabel('Current')
axs[0, 1 ].set_title('Current vs Time (Start)')
axs[0, 1 ].legend()
axs[0, 1 ].grid(True)

'''AT THE END'''
axs[1, 0].plot(PulsePeriod2, StimulusInPulsePeriod2, label='Stimulus', color='orange')
axs[1, 0].set_xlabel('Time (s)')
axs[1, 0].set_ylabel('Stimulus')
axs[1, 0].set_title('Stimulus vs Time (End)')
axs[1, 0].legend()
axs[1, 0].grid(True)
          
axs[1, 1].plot(PulsePeriod2, CurrentInPulsePeriod2, label='Current')
axs[1, 1].set_xlabel('Time (s)')
axs[1, 1].set_ylabel('Current')
axs[1, 1].set_title('Current vs Time (End)')
axs[1, 1].legend()
axs[1, 1].grid(True)

# =============================================================================
# #METHOD 2 : OVERLAPPING PLOTS
# =============================================================================
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Membrane Test', fontsize=16)

# Plot Current and Stimulus at the start (overlap them on axs[0])
axs[0].plot(PulsePeriod1, CurrentInPulsePeriod1, label='Current', color='blue')
axs[0].plot(PulsePeriod1, StimulusInPulsePeriod1, label='Stimulus', color='orange', linestyle='--')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Current / Stimulus')
axs[0].set_title('Current and Stimulus vs Time (Start)')
axs[0].legend()
axs[0].grid(True)

# Plot Current and Stimulus at the end (overlap them on axs[1])
axs[1].plot(PulsePeriod2, CurrentInPulsePeriod2, label='Current', color='cyan')
axs[1].plot(PulsePeriod2, StimulusInPulsePeriod2, label='Stimulus', color='orange', linestyle='--')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Current / Stimulus')
axs[1].set_title('Current and Stimulus vs Time (End)')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
