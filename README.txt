The contents of the data are described in the following.

In the folder “music” there are two files. The “file_names” file contains all of the MIDI file names that were used in the paper, unmodified from the original download from the public website. 

The list of composers are then given in the “composer_names” and “composer_names_with_date” files. 

These three files are also contained within the “data” folder. 

The “data” folder contains all of the feature information that was extracted from the MIDI files and then used to train the Random Forest Classifier. 

The four files that begin with “normalized” contain two columns, the first being the file name and the second being the point of normalized data indicated by the file name. 

The “bpm_std_dev” file contains the standard deviation of the tempo for each file. 

The “velocity_std_dev” file contains the standard deviation of the velocity for each file. 

The file “all_features” contains all of the features together in a normalized state in a single txt file, and it was the dataset that was used to train the Random Forest Classifier. The features did not have to be feature scaled to each other because Random Forest does not require feature scaling. 





