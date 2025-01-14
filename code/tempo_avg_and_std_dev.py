from music21 import converter, tempo, meter
import os
import warnings
import numpy as np  # For calculating standard deviation

#not relevant to this because only tempo matters, not the harmonic or instrumental content
warnings.filterwarnings("ignore", category=UserWarning, message="Unable to determine instrument")

# Function to process a single MIDI file and return its average BPM, standard deviation of BPM
def process_midi_file(midi_file_path, save_folder, failed_files_file):
    try:
        file = converter.parse(midi_file_path)

        total_duration = 0
        weighted_tempo_sum = 0

        # start_offset, end_offset, BPM
        beat_changes = file.metronomeMarkBoundaries()

        bpm_values = []
        offset_values = []

        # Only one beat change; for example -> (0.0, 80) 
        if len(beat_changes) == 1:
            start_offset, end_offset, metronome_mark = beat_changes[0]
            tempo1 = metronome_mark.getQuarterBPM()

            # All beats have same BPM 
            beats_in_section = end_offset - start_offset
            if beats_in_section > 0:  # Just in case
                weighted_tempo_sum += tempo1 * beats_in_section
                total_duration += beats_in_section
                bpm_values.append(tempo1)
                offset_values.append(start_offset)
        else:
            for start_offset, end_offset, metronome_mark in beat_changes:
                tempo1 = metronome_mark.getQuarterBPM()

                # Calculate the duration of this section in beats
                beats_in_section = end_offset - start_offset

                if beats_in_section > 0:  # Only process valid sections
                    # Weight tempo by the number of beats in the section
                    weighted_tempo_sum += tempo1 * beats_in_section
                    total_duration += beats_in_section

                    # Append the BPM and offset of the current section for plotting
                    bpm_values.append(tempo1)
                    offset_values.append(start_offset)

        # Average tempo calculation
        if total_duration > 0:
            average_tempo = weighted_tempo_sum / total_duration
        else:
            average_tempo = 0

        # Calculate the standard deviation of BPM values
        bpm_std_dev = np.std(bpm_values) if len(bpm_values) > 1 else 0

        # Normalize the BPM and BPM std dev relative to the file's average BPM
        normalized_bpm = [bpm / average_tempo * 100 for bpm in bpm_values] if average_tempo != 0 else []
        normalized_bpm_std_dev = bpm_std_dev / average_tempo * 100 if average_tempo != 0 else 0

        # Return the average tempo, BPM standard deviation, normalized BPMs, and normalized BPM std dev
        return average_tempo, bpm_std_dev, normalized_bpm, normalized_bpm_std_dev
    
    except Exception as e:
        # Log the file path if it fails to parse
        with open(failed_files_file, 'a') as failed_file:
            failed_file.write(f"Failed to process: {midi_file_path} - Error: {str(e)}\n") #for debug and checking later
        return None, None, None, None

# Function to process a folder of MIDI files
def process_folder(folder_path, save_folder):
    # Ensure the output folder for saving results exists
    os.makedirs(save_folder, exist_ok=True) #

    # Path to log failed files
    failed_files_file = os.path.join(save_folder, 'failed_files.txt') #check this for failed files later

    # Clear the failed files log if it already exists
    open(failed_files_file, 'w').close()

    # Collect all file paths using os.walk()
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mid") or file.endswith(".midi"):  # Only process MIDI files
                file_paths.append(os.path.join(root, file))

    # Open files to save the results
    results_filename = os.path.join(save_folder, 'average_bpm_results.txt')
    normalized_bpm_filename = os.path.join(save_folder, 'normalized_bpm.txt')  # File for normalized BPMs
    normalized_bpm_std_dev_filename = os.path.join(save_folder, 'normalized_bpm_std_dev.txt')  # File for normalized BPM std dev

    with open(results_filename, 'w') as results_file, open(normalized_bpm_filename, 'w') as normalized_bpm_file, \
         open(normalized_bpm_std_dev_filename, 'w') as normalized_bpm_std_dev_file:
        
        # clarity headers
        results_file.write("Filename, Average BPM, BPM Standard Deviation\n")
        normalized_bpm_file.write("Filename, Normalized BPMs\n")
        normalized_bpm_std_dev_file.write("Filename, Normalized BPM Std Dev\n")

        # Process each MIDI file in the list of file paths
        for midi_file_path in file_paths:
            normalized_bpm, normalized_bpm_std_dev = process_midi_file(midi_file_path, save_folder, failed_files_file)

            # filename has commas and spaces, get rid
            clean_filename = os.path.basename(midi_file_path).replace(" ", "").replace(",", "")

            # If the file was successfuL
            if average_bpm is not None:
                # BPM + STD DEV
                results_file.write(f"{clean_filename}, {average_bpm}, {bpm_std_dev}\n")
                # Save the result to the second file (just the filename and average BPM)
                normalized_bpm_file.write(f"{clean_filename}, {', '.join([f'{bpm}' for bpm in normalized_bpm])}\n")
                # Save the normalized BPM std dev
                normalized_bpm_std_dev_file.write(f"{clean_filename}, {normalized_bpm_std_dev}\n")

                print(f"Processed {clean_filename}, Average BPM: {average_bpm}, BPM Std Dev: {bpm_std_dev}, Normalized BPM Std Dev: {normalized_bpm_std_dev}")
            else:
                print(f"Failed to process {clean_filename}")

    # Ensure the output folder for saving results exists
    os.makedirs(save_folder, exist_ok=True)

    # Path to log failed files
    failed_files_file = os.path.join(save_folder, 'failed_files.txt')

    # Clear the failed files log if it already exists
    open(failed_files_file, 'w').close()

    # Collect all file paths using os.walk()
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mid") or file.endswith(".midi"):  # Only process MIDI files
                file_paths.append(os.path.join(root, file))

    # Open files to save the results
    results_filename = os.path.join(save_folder, 'average_bpm_results.txt')
    filenames_bpm_filename = os.path.join(save_folder, 'filenames_and_bpm.txt')
    bpm_std_dev_filename = os.path.join(save_folder, 'bpm_std_dev.txt')  # File for BPM standard deviation

    with open(results_filename, 'w') as results_file, open(filenames_bpm_filename, 'w') as filenames_bpm_file, open(bpm_std_dev_filename, 'w') as bpm_std_dev_file:
        # Write headers
        results_file.write("Filename, Average BPM, BPM Standard Deviation\n")
        filenames_bpm_file.write("Filename, Average BPM\n")
        bpm_std_dev_file.write("Filename, BPM Standard Deviation\n")

        # Process each MIDI file in the list of file paths
        for midi_file_path in file_paths:
            average_bpm, bpm_std_dev = process_midi_file(midi_file_path, save_folder, failed_files_file)

            # Clean the filename by removing spaces and commas
            clean_filename = os.path.basename(midi_file_path).replace(" ", "").replace(",", "")

            # If the file was processed successfully
            if average_bpm is not None:
                # Save the result to the first file
                results_file.write(f"{clean_filename}, {average_bpm:.2f}, {bpm_std_dev:.2f}\n")
                # Save the result to the second file (just the filename and average BPM)
                filenames_bpm_file.write(f"{clean_filename}, {average_bpm:.2f}\n")
                # Save the BPM standard deviation to the third file
                bpm_std_dev_file.write(f"{clean_filename}, {bpm_std_dev:.2f}\n")

                print(f"Processed {clean_filename}, Average BPM: {average_bpm:.2f}, BPM Std Dev: {bpm_std_dev:.2f}")
            else:
                print(f"Failed to process {clean_filename}")

# Folder path containing the MIDI files
folder_path = r'C:\Users\aiden\OneDrive\Desktop\Feature_Modeling\MIDI_unknown'  # Modify this path
save_folder = r'C:\Users\aiden\OneDrive\Desktop\Feature_Modeling\part3data'  # Modify this to the desired save folder path

# Process the folder
process_folder(folder_path, save_folder)
