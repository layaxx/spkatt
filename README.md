# Out of the mouths of MPs: Speaker Attribution in Parliamentary Debates
## (GePaDe-SpkAtt Corpus)


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

 

### Content of this repository:

```
- data
	- GePaDe
		- train.json
		- dev.json
		- test.json

- predictions
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

- run_train.sh
- run_predict.sh

- README.md (this readme file)
```

### Description

The data folder contains the training, dev and test splits for the GePaDe-SpkAtt Corpus.
The data is in json format. Meta-information on the speakers, their party affiliation 
and the data of the speech are included in the dictionary keys for each sentence in the data.

The doc folder includes the paper, the annotation guidelines (in German) and the datasheet for our corpus.

The predictions folder includes the system output (for dev and test sets) for the BERT-large model
(see the description in the paper) for one run with seed .

You can use the evaluation script (predictions/eval.py) to evaluate the system output against the gold data:

```
python eval.py <gold filename> <system output filename>

e.g.:

cd predictions

python eval.py ../data/GePaDe/test.json test/pred_test_seed8.json
```

### Model

Our baseline system is the one of Conia & Navgili (2020):

```
Simone Conia and Roberto Navigli. 2020. Bridging the gap in
multilingual semantic role labeling: a language-agnostic approach. 
In Proceedings of the 28th International Conference on 
Computational Linguistics, pages 1396–1410, Barcelona, Spain 
(Online). International Committee on Computational Linguistics.
```

To run the model, first download and install the SRL system. Follow the instructions provided on the authors' [github page](https://github.com/SapienzaNLP/multi-srl).

Then download our pretrained [model for speaker attribution in parliamentary debates](https://data.dws.informatik.uni-mannheim.de/spkatt/spkatt_large_seed42.tgz), put it in the models folder and decompress it (`cd models; tar -xzf spkatt_large_seed42.tgz`).

You can now use the model to predict speech events in unlabelled data. The input file should have the same format as the example file in 
the folder `example/unlabelled_data.json`.














