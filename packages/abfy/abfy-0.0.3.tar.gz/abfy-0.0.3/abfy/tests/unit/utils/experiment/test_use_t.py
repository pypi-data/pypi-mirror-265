from abfy.src.utils.experiment.use_t import adjust_result_using_t


class TestUseT:
    def test_adjust_result_using_t(self):

        est = 3
        se = 1
        num_data = 100
        num_predictor = 5
        p_value, ci_left, ci_right = adjust_result_using_t(est, se, num_data, num_predictor, alpha=0.05)
        assert ci_right > ci_left
        assert ci_left > 0
        assert p_value <= 0.05
