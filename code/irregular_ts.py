import os
from music21 import *

# Define the folder containing the MIDI files
midi_folder_path = r'C:\Users\aiden\OneDrive\Desktop\Feature_Modeling\MIDI_unknown'

# the regular ts, very usual in music (simple and compound meters)
common_time_signatures = ['4/4', '3/4', '2/4', '6/8', '9/8', '12/8', '2/2']

results = []


for filename in os.listdir(midi_folder_path):
    if filename.endswith('.mid') or filename.endswith('.midi'):
        midi_file_path = os.path.join(midi_folder_path, filename)


        midi = converter.parse(midi_file_path)

        total_bars = 0
        irregular_bars = 0
        last_time_signature = None

        # Loop through each measure in the MIDI file
        for measure in midi.parts[0].getElementsByClass('Measure'):
            total_bars += 1  # Increment the total bar count

            # Get the time signature for the current measure
            current_time_signature = measure.timeSignature

                # If the time signature is None, use the last valid time signature
                
            if current_time_signature is None:
                    if last_time_signature is not None:
                        measure.timeSignature = last_time_signature
            else:
                    # Update last_time_signature with the current one
                    last_time_signature = current_time_signature

                # Get the string representation of the time signature
            time_signature_str = (measure.timeSignature.ratioString)

                # Check if the time signature is common
            if time_signature_str not in common_time_signatures:
                    irregular_bars += 1

            # Calculate the percentage of irregular bars
            if total_bars > 0:
                irregular_percentage = (irregular_bars / total_bars) * 100
            else:
                irregular_percentage = 0

            # Append the result to the list
            results.append(f'{filename}\t{irregular_percentage:.2f}')

    print(filename, ": done")


# Write the results to a text file
output_file_path = 'irregular.txt'

with open(output_file_path, 'w') as f:
    for result in results:
        f.write(result + '\n')

print(f'Results have been written to {output_file_path}')
