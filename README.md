# Speaker Attribution in Parliamentary Debates (GePaDe-SpkAtt)


This repository contains the data and supplementary materials for our [LREC-COLING-2024 paper](https://github.com/umanlp/spkatt/blob/master/doc/GePaDe-SpkAtt-LREC-COLING-2024.pdf):

``` 
@inproceedings{rehbein-etal-2024-speaker-attribution,
    title = "Out of the mouths of {MP}s: {S}peaker Attribution in Parliamentary Debates",
    author = "Rehbein, Ines  and
      Ruppenhofer, Josef  and
      Brunner, Annelen  and
      Ponzetto, Simone Paolo",
    editor = " ",
    booktitle = "Proceedings of the Thirteenth Language Resources and Evaluation Conference",
    month = may,
    year = "2024",
    address = "Torino, Italia",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/",
    pages = " ",
}
```

### Out of the mouths of MPs:
### Speaker Attribution in Parliamentary Debates
 

### Content of this repository:

```
- data
	- gold
		- train.json
		- dev.json
		- test.json
	- system_output
		- dev
			- pred_dev_seed313.json
			- pred_dev_seed42.json
			- pred_dev_seed8.json
		- test
			- pred_test_seed313.json
			- pred_test_seed42.json
			- pred_test_seed8.json
	- eval.py
- doc
	- GePaDe-SpkAtt-LREC-COLING-2024.pdf
	- Guidelines_SpeakerAttribution_in_Parliamentary_Debates_german.pdf  
	- SpkAtt-Debates-Datasheet_COLING-2024.pdf

- README.md (this readme file)
```

### Description

The data folder contains the training, dev and test splits for the GePaDe-SpkAtt Corpus.
The data is in json format. Meta-information on the speakers, their party affiliation 
and the data of the speech are included in the dictionary keys for each sentence in the data.

The doc folder includes the paper, the annotation guidelines (in German) and the datasheet for our corpus.

The system_output folder includes the system output (or dev and test sets) for the BERT-large model
(see the description in the paper) for three independent runs with different initialisations (seeds: 8, 42, 313).



More detailed instructions on how to train/test the model will be added later.


