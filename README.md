# Speaker Attribution in Parliamentary Debates (GePaDe-SpkAtt)


This repository contains the data and supplementary materials for the anonymous paper submission to LREC-COLING-2024:

### Out of the mouths of MPs:
### Speaker Attribution in Parliamentary Debates

### Content of this repository:

```
- data
	- train.json
	- dev.json
	- test.json
- doc
	- Guidelines_SpeakerAttribution_in_Parliamentary_Debates_german.pdf  
	- SpkAtt-Debates-Datasheet_COLING-2024.pdf
- system_output
	- dev_predicted_seed17.json  
	- dev_predicted_seed313.json  
	- dev_predicted_seed42.json  
	- test_predicted_seed17.json  
	- test_predicted_seed313.json  
	- test_predicted_seed42.json
	- hyperparameters.json
- README.md (this readme file)
```

### Description

The data folder contains the training, dev and test splits for the GePaDe-SpkAtt Corpus.
The data is in json format. Meta-information on the speakers, their party affiliation 
and the data of the speech are included in the dictionary keys for each sentence in the data.

The doc folder includes the annotation guidelines (in German) and the datasheet for our corpus.

The system_output folder includes the system output (dev and test set) for the BERT-large model
(see the description in the paper) for three independent runs with different initialisations.
The file hyperparameters.json in the same folder includes the hyperparameters used to train
the model.

More detailed instructions on how to train/test the model will be added later.


