import argparse
from data_handler import StreamingDataframe
from percentile_tracker import PercentileTracker


def build_arg_dict(arg_list):
    arg_dict = {
        'percentile_file': arg_list.percentile_file[0],
        'contributions_file': arg_list.contributions_file[0],
        'out_file': arg_list.out_file[0],
    }
    return arg_dict


def write_output(output_stream, *args):
    delim = '|'
    output_entries = [str(x) for x in args]
    output_stream.write(delim.join(output_entries)+'\n')


def calculate_running_percentile(arg_dict):
    tracker = PercentileTracker(arg_dict['percentile_file'])
    with open(arg_dict['out_file'], 'w') as output_stream, \
         StreamingDataframe(arg_dict['contributions_file']) as data_stream:
        for record in data_stream:
            transaction_year = record['TRANSACTION_DT'].year
            if tracker.is_repeat_donor(record['NAME'],
                                       record['ZIP_CODE'],
                                       transaction_year):
                percentile_stats = \
                    tracker.calculate_percentile_stats(record['CMTE_ID'],
                                                       record['ZIP_CODE'],
                                                       transaction_year,
                                                       record['TRANSACTION_AMT'])
                write_output(
                    output_stream, 
                    record['CMTE_ID'],
                    record['ZIP_CODE'],
                    transaction_year,
                    *percentile_stats)

    from collections import Counter
    import pdb
    c = Counter()
    for k, v in tracker.recipient_dict.items():
        for z in v.keys():
            c[z] += 1
    pdb.set_trace()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Given a CSV file formatted according to this data'
            ' dictionary:\nhttps://classic.fec.gov/finance/disclosure/'
            'metadata/DataDictionaryContributionsbyIndividuals.shtml\n'
            'output information on contribution percentiles as outlined'
            ' in the README')
    parser.add_argument(
        'contributions_file', nargs=1,
        help='Path to file containing contribution data.')
    parser.add_argument(
        'percentile_file', nargs=1,
        help='Path to file containing a single number 1-100.'
        ' Marks the contribution percentile to output.')
    parser.add_argument(
        'out_file', nargs=1,
        help='File percentile information will be written to.')
    args = parser.parse_args()

    arg_dict = build_arg_dict(args)
    calculate_running_percentile(arg_dict)
