import os
import matplotlib.pyplot as plt
from music21 import *
import numpy as np

# Directory paths
midi_folder = r'path'  # Replace with your folder path
output_txt_file = r'path2'  # Output text file for average densities
output_graphs_folder = r'path3'  # Folder to save graphs

#make output folder 
if not os.path.exists(output_graphs_folder):
    os.makedirs(output_graphs_folder)

#compute average rhythmic density 
def calculate_average_density(midi_file):
    
    score = converter.parse(midi_file)
    scorechords = score.chordify()

    start_times = []

    # all parts in the score
    for part in score.parts:
        #all note objects in the score
        for note in part.flatten().notes:
            # note's start time (offset) and its duration (in quarterLengths)
            start_time = note.offset - 1  # offset of 1 is equal to a start time of 0 because bar 1 starts at offset1
            if start_time not in start_times: #append each UNIQUE start time
                start_times.append(start_time)

    # into ascending order for ease 
    sorted_times = sorted(start_times) 

    # Interval length in quarter notes (4 beats)
    interval_length = 4 # (density per 4 note interval)

    # Initialize an empty list to store counts of notes per 4 beat interval 
    note_counts = []

    # min max of times, min should be 0 (but may not be if there are unusual rests at the beginning,\ 
    # max is the last note of the piece 
    min_time = min(sorted_times)
    max_time = max(sorted_times)

    # Loop 
    current_interval_start = min_time // interval_length * interval_length
    while current_interval_start <= max_time:
        # Count how many start_times fall within the current 4-beat interval
        count = 0
        for time in sorted_times:
            if current_interval_start <= time < current_interval_start + interval_length: #+4 
                count+=1
        
        note_counts.append(count) 
        #next four beat interval, etc 
        current_interval_start += interval_length

    # total unique offsets in the entire piece
    total_notes = sum(note_counts)

    # average rhythmic density per 4 beats
    if len(note_counts) > 0:
        average_density = total_notes / len(note_counts)  
    else: 0

    return average_density, note_counts

# Process all MIDI files in the folder
with open(output_txt_file, 'a') as txt_file:
    # Write headers in the text file if it's empty
    if os.stat(output_txt_file).st_size == 0:
        txt_file.write("File Name\tAverage Density\n")

    for midi_file in os.listdir(midi_folder):
        if midi_file.endswith('.mid'):
            midi_path = os.path.join(midi_folder, midi_file)

            # Calculate the average rhythmic density and note counts for the MIDI file
            average_density, note_counts = calculate_average_density(midi_path)

            # Save the results in the text file
            txt_file.write(f"{midi_file}\t{average_density:.2f}\n")

            # Print the file name and average density
            print(f"File: {midi_file} - Average Density: {average_density:.2f}")

            # Plot the graph for this file
            plt.figure(figsize=(10, 6))
            plt.bar(np.arange(len(note_counts)), note_counts, width=0.8, color='blue', alpha=0.7)

            # Add labels and title
            plt.xlabel('4-beat Intervals')
            plt.ylabel('Note Count')
            plt.title(f'Note Occurrences per 4-beat Interval\n{midi_file}')

            # Add a horizontal line for average rhythmic density
            plt.axhline(y=average_density, color='red', linestyle='--', label=f'Avg Density = {average_density:.2f} notes/4-beat')

            # Display the legend
            plt.legend()

            # Save the plot as a PNG image in the output folder
            graph_filename = f"{os.path.splitext(midi_file)[0]}.png"  # Use the MIDI filename for the graph
            graph_path = os.path.join(output_graphs_folder, graph_filename)
            plt.tight_layout()
            plt.savefig(graph_path)
            plt.close()  # Close the plot to free memory

print("Processing complete. Results saved in:", output_txt_file)
