## Source Code Description

The files in this repository are as follows:

- `calculate_running_percentile.py` - Implements command line interface for running analytics and high level logic.  
- `data_handler.py` - Defines code to handle reading and sanitizing data from input data file.
- `percentile_tracker.py` - Defines data structures and logic necessary to calculate percentile values.  
- `unit_tests` - directory containing unit tests. Meant to be run with `pytest`.

### Requirements
The code is written using only Python standard library modules. The code was tested to work with Python 2.7 or 3.6, though earlier versions are likely compatible.

The unit tests require pytest to be installed.

### Summary of Approach
The `StreamingDataframe` class allows for simple line-by-line iteration of the input data file. It returns only the necessary columns and ensures no fields have invalid entries. If an invalid field is found it automatically moves to the next line in the input. 

The `PercentileTracker` contains the data structures and logic necessary for calculating percentile statistics. It holds two data structures: 

- `donor_dict` - A dictionary mapping donor ID: `int(str(hash(donor name)) + str(zip_code))` to the earliest year that donor donated. 
- `recipient_dict` - Nested dictionary storing sorted contribution values for each recipient, zip_code, year triplet. Recipient ID is hashed before use as key to save memory. 

`PercentileTracker` also implements several methods for external use:
- `is_repeat_donor` - checks whether a given name, zip code combination has donated in a previous year (and updates `donor_dict` if not). 
- `calculate_percentile_stats` - updates the `recipient_dict` with a new transaction and then calculates the Nth percentile, sum of transactions and transaction count.

`calculate_running_percentile.py` reads input data using the `SreamingDataframe` object and operates on it using a `PercentileTracker` object. It also implements the command line interface for the program. 

### Assumptions
- No (or negligible) hash collisions occur between names in the same zip code when using the built-in Python hash function. 
- No (or negligible) hash collisions between CMTE_ID's
- Sum of contributions are rounded half-up to nearest integer. This was unspecified in the README, but it seemed strange to round the percentile value and not the sum. Displaying zeros after the decimal also caused the provided test to fail. 
- Contributions donated more than one day after the system date will be rejected. (Extra day allowed in case of timezone issues)
- Contributions before 1975 will be rejected (1975 was first year of data recording).
- Only those who donated in an earlier year are repeat donors. Multiple times in one year doesn't count. 



