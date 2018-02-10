import bisect
from collections import defaultdict, namedtuple
import math


class PercentileTracker:
    def __init__(self, percentile_file):
        self.percentile_file = percentile_file
        self.percentile_fraction = self._read_percentile(percentile_file)
        self.PercentileStats = namedtuple('PercentileStats', 
                                          'percentile transaction_sum transaction_count')
        self.donor_dict = {}
        self.recipient_dict = defaultdict(  # Indexed by recipient hash
            lambda: defaultdict(  # Indexed by zip code
                lambda: defaultdict(  # Indexed by year
                    lambda: [])))  # Holds transaction values
        
    @staticmethod
    def _read_percentile(percentile_file):
        with open(percentile_file, 'r') as percentilef:
            percentile = next(percentilef)
            percentile_fraction = int(percentile)/100
        return percentile_fraction
        
    def _nearest_rank_percentile(self, transaction_list):
        """Calculates the transaction value for the nearest"""
        index = math.ceil(self.percentile_fraction*len(transaction_list)) - 1
        value = int(transaction_list[index] + .5)
        return value
        
    def is_repeat_donor(self, name, zip_code, year):
        # Hash collision between two names in same zip code causes error.
        # Assume collision rare enough to not greatly affect results. 
        hashed_id = int(str(hash(name)) + zip_code)
        earliest_year = self.donor_dict.get(hashed_id, year + 1)
        if year <= earliest_year:
            self.donor_dict[hashed_id] = year
            return False
        return True

    def calculate_percentile_stats(self, recipient, zip_code, year, transaction_amt):
        """
        Insert the new transaction and get percentile statistics.
        
        :return stats: PercentileStats namedtuple instance
        """
        recipient_hash = hash(recipient)
        transaction_list = self.recipient_dict[recipient_hash][int(zip_code)][year]
        insert_index = bisect.bisect(transaction_list, transaction_amt)
        transaction_list.insert(insert_index, transaction_amt)

        percentile_value = self._nearest_rank_percentile(transaction_list)
        transaction_sum = int(sum(transaction_list) + .5)
        stats = self.PercentileStats(
            percentile=percentile_value, 
            transaction_sum=transaction_sum,
            transaction_count=len(transaction_list))
        return stats
