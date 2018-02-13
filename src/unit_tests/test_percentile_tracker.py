import pytest
from percentile_tracker import PercentileTracker


@pytest.fixture(scope='module', autouse=True)
def patch_percentile_tracker():
    # Allow PercentileTracker to be initialized with float
    PercentileTracker._read_percentile = lambda self, x: x


def test_nearest_rank_percentile():
    tracker = PercentileTracker(.5)
    trans_list = list(range(100))

    tracker.percentile_fraction = 0.001
    assert tracker._nearest_rank_percentile(trans_list) == 0

    tracker.percentile_fraction = .0101
    assert tracker._nearest_rank_percentile(trans_list) == 1

    tracker.percentile_fraction = 1
    assert tracker._nearest_rank_percentile(trans_list) == 99

    tracker.percentile_fraction = .23
    assert tracker._nearest_rank_percentile(trans_list) == 22


def test_is_repeat_donor():
    tracker = PercentileTracker(.5)

    # 'Nobody' not in dictionary yet
    assert not tracker.is_repeat_donor('Nobody', '32523', 2004)

    # Now 'Nobody' is in dictionary
    assert tracker.is_repeat_donor('Nobody', '32523', 2005)

    # Donations in same year as earliest don't count
    assert not tracker.is_repeat_donor('Nobody', '32523', 2004)

    # Different zip code
    assert not tracker.is_repeat_donor('Nobody', '1111', 2008)

def test_calculate_percentile_stats():
    tracker = PercentileTracker(.5)

    stats = tracker.calculate_percentile_stats(
            'MURICA', '2135', 1776, 2.7)

    # Check ordering of attributes correct
    lst = [x for x in stats]
    assert lst[0] == stats.percentile
    assert lst[1] == stats.transaction_sum
    assert lst[2] == stats.transaction_count


    stats = tracker.calculate_percentile_stats(
            'MURICA', '2135', 1776, 0.5)

    # Check stats fields for accuracy 
    assert stats.percentile == 1
    assert stats.transaction_sum == 3
    assert stats.transaction_count == 2
