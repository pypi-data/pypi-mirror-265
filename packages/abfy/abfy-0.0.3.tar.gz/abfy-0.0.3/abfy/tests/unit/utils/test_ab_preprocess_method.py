import pathlib
import tempfile

import pytest

from abfy.src.models.data_model import DataLoader
from abfy.src.pipeline.experiment_pipelines.ab_pipeline import ABPipeline
from abfy.tests.unit.data import (
    get_imbalance_check_input,
    get_input_for_flicker_test,
    get_preprocess_test_input,
    get_test_input,
)


class TestAbPreprocessMethod:
    @pytest.fixture
    def ab_sample_data(self):
        data, config = get_test_input()
        return {"data": data, "config": config}

    def test_flicker(self):
        data, config = get_input_for_flicker_test()
        # remove flickers
        config["experiment_settings"]["is_remove_flickers"] = True
        pl = ABPipeline(data, config)
        pl.run()
        assert pl.preprocess_result.does_flicker_exists is True
        assert len(pl.preprocess_result.processed_data) == 4
        # don't remove flickers
        config["experiment_settings"]["is_remove_flickers"] = False
        pl = ABPipeline(data, config)
        pl.run()
        assert pl.preprocess_result.does_flicker_exists is True
        assert len(pl.preprocess_result.processed_data) == len(data)

    def test_flicker_multiple_experiment_groups(self):
        data, config = get_preprocess_test_input()
        # when is_remove_flickers flag is True
        pl = ABPipeline(data, config)
        pl.run()
        assert pl.preprocess_result.does_flicker_exists is False
        assert len(pl.preprocess_result.processed_data) == 10
        # when is_remove_flickers flag is False
        config["experiment_settings"]["is_remove_flickers"] = False
        pl = ABPipeline(data, config)
        pl.run()
        assert pl.preprocess_result.does_flicker_exists is False
        assert len(pl.preprocess_result.processed_data) == 22

    def test_preprocess_imbalance(self):
        data, config, config_w_cluster = get_imbalance_check_input()
        # no cluster
        pl = ABPipeline(data, config)
        pl.run()
        assert pl.preprocess_result.are_buckets_imbalanced is True
        # with cluster
        pl = ABPipeline(data, config_w_cluster)
        pl.run()
        assert pl.preprocess_result.are_buckets_imbalanced is True

    def test_process_distribution(self):
        data, config = get_preprocess_test_input()
        # Run whole pipeline
        ABPipeline(data, config).run()


class TestLowMemPreprocessMethod:
    @pytest.fixture
    def ab_sample_data(self):
        data, config = get_test_input()
        return {"data": data, "config": config}

    def test_flicker(self):
        data, config = get_test_input()
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = pathlib.Path(temp_dir)
            data.iloc[: data.shape[0] // 2, :].to_parquet(folder / "raw_data.parquet")
            data.iloc[data.shape[0] // 2 :, :].to_parquet(folder / "raw_data2.parquet")
            data_loader = DataLoader(data_folder=folder)
            pl = ABPipeline(data_loader, config)
            pl.run()
            assert pl.preprocess_result.does_flicker_exists is False
            assert len(pl.preprocess_result.processed_data) == len(data)

    def test_flicker_multiple_experiment_groups(self):
        data, config = get_preprocess_test_input()
        config["experiment_settings"]["is_remove_flickers"] = False
        config["columns"]["metric1"]["check_distribution"] = False
        config["columns"]["metric2"]["check_distribution"] = False

        with tempfile.TemporaryDirectory() as temp_dir:
            folder = pathlib.Path(temp_dir)
            data.iloc[: data.shape[0] // 2, :].to_parquet(folder / "raw_data.parquet")
            data.iloc[data.shape[0] // 2 :, :].to_parquet(folder / "raw_data2.parquet")
            data_loader = DataLoader(data_folder=folder)
            pl = ABPipeline(data_loader, config)
            pl.run()
            assert pl.preprocess_result.does_flicker_exists is False
            assert len(pl.preprocess_result.processed_data) == 22

    def test_preprocess_imbalance(self):
        data, config, config_w_cluster = get_imbalance_check_input()

        with tempfile.TemporaryDirectory() as temp_dir:
            folder = pathlib.Path(temp_dir)
            data.iloc[: data.shape[0] // 2, :].to_parquet(folder / "raw_data.parquet")
            data.iloc[data.shape[0] // 2 :, :].to_parquet(folder / "raw_data2.parquet")
            data_loader = DataLoader(data_folder=folder)

            # no cluster
            pl = ABPipeline(data_loader, config)
            pl.run()
            assert pl.preprocess_result.are_buckets_imbalanced is True
            # with cluster
            pl = ABPipeline(data_loader, config_w_cluster)
            pl.run()
            assert pl.preprocess_result.are_buckets_imbalanced is True

    def test_preprocess_logxform(self):
        data, config = get_test_input()
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = pathlib.Path(temp_dir)
            data.iloc[: data.shape[0] // 2, :].to_parquet(folder / "raw_data.parquet")
            data.iloc[data.shape[0] // 2 :, :].to_parquet(folder / "raw_data2.parquet")
            data_loader = DataLoader(data_folder=folder)
            pl = ABPipeline(data_loader, config)
            pl.run()
            pl2 = ABPipeline(data, config)
            pl2.run()
