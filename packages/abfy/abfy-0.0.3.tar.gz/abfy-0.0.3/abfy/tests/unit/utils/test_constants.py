from abfy.src.utils.constants import Constants


def test_imbalance_threshold_config():
    """Check for inadvertent changes to imbalance thresholds"""
    assert Constants.IMBALANCE_BINOMIAL_THRESHOLD == 0.01, "Config threshold does not match expected change."
    assert Constants.IMBALANCE_CHI_SQUARE_THRESHOLD == 0.01, "Config threshold does not match expected change."
