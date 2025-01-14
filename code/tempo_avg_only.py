from music21 import converter, tempo, meter
import math

e = r'MIDI_popular/1_voicesofspring.mid'

# parse file 
file = converter.parse(e)

#tracker variables
total_duration = 0
weighted_tempo_sum = 0 

# Extract tempo changes
beat_changes = file.metronomeMarkBoundaries()

# extract time signatures 
time_signatures =[]
current_time_signature = None

for part in file.parts:
    # Iterate over the measures in the part
    for measure in part.getElementsByClass('Measure'):
        if (measure.timeSignature is None): # if none / backup 
            current_time_signature = current_time_signature or meter.TimeSignature('4/4')
        else: #update current ts
            current_time_signature = measure.timeSignature
        time_signatures.append(current_time_signature)
    break #just need to do it once

#getting measures inside file.parts
measures = []
for p in file.parts:
    elements = p.getElementsByClass('Measure')
    for m in elements:
        measures.append(m) # all measures in all parts

for start_measure, end_measure, metronome_mark in beat_changes:
    measure_duration = end_measure - start_measure  # Duration in which the tempo applies in measures
    tempo1 = metronome_mark.getQuarterBPM()  # Tempo (quarter note speed)

    measure_beats = 0
    
    #if measure in = measure out
    if start_measure < 1 or end_measure > len(measures) or start_measure >= end_measure: #skip instances where start = end measure (no measures for some reason)
        continue
    
    for measure in measures[math.floor(start_measure-1):math.floor(end_measure)]: #iterate through start til end measure (without counting end measure)
        time_signature = time_signatures[measure.measureNumber - 1]
        if time_signature is not None:
            beats_in_measure = time_signature.barDuration.quarterLength
            measure_beats += beats_in_measure
        else:
        # In case there's no time signature, default to 4 beats (common in unmetered music)
            measure_beats += 4


    time_duration = measure_beats * (60 / tempo1) 
    weighted_tempo_sum += tempo1 * time_duration
    total_duration += time_duration

#average calculation
if total_duration > 0:
    average_tempo = weighted_tempo_sum / total_duration
else:
    average_tempo = 0

print("Average Tempo: ", average_tempo)