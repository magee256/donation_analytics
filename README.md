
## Donation Analytics
This repository contains code to generate statistics on contributions from individuals to political entities such as political action committees (PACs) and campaign funds. A description of the input and output follows. 

### File descriptions

#### Input

- a data file matching the format described [here](https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml)
- a file containing one number in range (0, 100]. This number represents the donation percentile to be output.

#### Output
- Output data file containing the following fields:
	- Political Entity ID
	- Zip code of repeat donor
	- Year of donation
	- Nth percentile donation value
	- Sum of donations
	- Number of donations

- Repeat donor - A donor who has donated in a previous year from the same zip code. 
- Donation values, sums and counts are tracked separately for each political entity, zip code and donation year. 
- Data is output whenever a repeat donor is seen. The input is parsed line-by-line in streaming fashion, so a donor will need to have appeared at least twice before anything is output. 

### Running the code
- The code requires Python 2.7 or Python 3.6
- The code may be run using command:```
	python src/calculate_running_percentile.py [input data] [percentile file] [output data]```
- Alternatively the input data and percentile file may be placed in the `input` folder and named `itcont.txt` and `percentile.txt` respectively. Then running `run.sh` will produce the output file `output/repeat_donors.txt`. 

### Code Description
For details on the source code and solution approach see the `src` directory's README.
