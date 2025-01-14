import os
import numpy as np
from music21 import *

# Directory paths
midi_folder = r'C:\Users\aiden\OneDrive\Desktop\Feature_Modeling\MIDI_unknown'  # Replace with your folder path
output_txt_file = r'C:\Users\aiden\OneDrive\Desktop\Feature_Modeling\velocity_std_dev.txt'  # Output text file for average velocities and normalized standard deviation

# Function to compute average velocity, normalized standard deviation, and store results
def calculate_velocity_stats(midi_file):
    # Load the score
    score = converter.parse(midi_file)

    # Initialize a dictionary to hold the sum of velocities at each time point
    time_to_velocity = {}

    # Iterate over all parts in the score
    for part in score.parts:
        # Get all notes in this part
        for note in part.flatten().notes:
            # Get the note's start time (offset) and its duration (quarterLength)
            start_time = note.offset - 1  # Adjusting the offset by -1
            duration = note.quarterLength

            # Get note velocity
            velocity = note.volume.velocity if note.volume.velocity is not None else 64  # Default velocity is 64

            # Apply velocity to all time points the note occupies
            current_time = start_time
            while current_time < start_time + duration:
                if current_time in time_to_velocity:
                    time_to_velocity[current_time] += velocity
                else:
                    time_to_velocity[current_time] = velocity
                current_time += 0.25  # Increment by quarter length for each tick (assuming we use quarter-length precision)

    # Sort the times
    sorted_times = sorted(time_to_velocity.keys())

    # Prepare lists for velocity values
    velocities = [time_to_velocity[time] for time in sorted_times]

    # Calculate the average velocity and standard deviation
    average_velocity = np.mean(velocities) if velocities else 0
    std_deviation = np.std(velocities) if velocities else 0

    # Calculate normalized standard deviation
    normalized_std = std_deviation / average_velocity if average_velocity > 0 else 0

    return average_velocity, normalized_std

# Process all MIDI files in the folder
with open(output_txt_file, 'a') as txt_file:
    # Write headers in the text file if it's empty
    if os.stat(output_txt_file).st_size == 0:
        txt_file.write("File Name\tAverage Velocity\tNormalized Standard Deviation\n")

    for midi_file in os.listdir(midi_folder):
        if midi_file.endswith('.mid'):
            midi_path = os.path.join(midi_folder, midi_file)

            # Calculate the average velocity and normalized standard deviation for the MIDI file
            average_velocity, normalized_std = calculate_velocity_stats(midi_path)

            # Save the results in the text file
            txt_file.write(f"{midi_file}\t{average_velocity:.2f}\t{normalized_std:.2f}\n")

            # Print the file name, average velocity, and normalized standard deviation
            print(f"File: {midi_file} - Average Velocity: {average_velocity:.2f}, Normalized Standard Deviation: {normalized_std:.2f}")

print("Processing complete. Results saved in:", output_txt_file)
