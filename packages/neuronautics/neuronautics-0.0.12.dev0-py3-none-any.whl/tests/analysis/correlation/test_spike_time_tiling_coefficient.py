import unittest
from unittest.mock import patch
from neuronautics.analysis.correlation.spike_time_tiling_coefficient import SpikeTimeTilingCoefficient
import pandas as pd
import numpy as np


class TestSpikeTimeTilingCoefficient(unittest.TestCase):
    def test_get_input_params(self):
        ac = SpikeTimeTilingCoefficient()
        params = ac.get_input_params()

        for param in params:
            self.assertTrue(param['default'] <= param['max'])
            self.assertTrue(param['min'] <= param['default'])
            self.assertTrue('name' in param)
            self.assertTrue('type' in param)

    def test_run(self):
        spikes = pd.DataFrame({'class': [0, 0, 0, 0, 0, 0, 0, 0],
                               'channel_id': [0, 0, 0, 0, 1, 1, 1, 1],
                               'ts_ms': [1, 2, 3, 4, 1, 2, 3, 4]})
        expected_correlation = np.array([[False, True], [True, False]])

        with patch('neuronautics.analysis.correlation.spike_time_tiling_coefficient.Layout') as mck_layout:
            mck_layout.return_value.current.return_value = [[1, 2]]
            ac = SpikeTimeTilingCoefficient()
            output = ac.run(spikes, 0.5)

            np.testing.assert_array_equal(expected_correlation, output)

    def test_plot(self):
        """parent plot is called with the plot title set"""
        with patch('neuronautics.analysis.correlation.spike_time_tiling_coefficient.super') as spy_super:
            ac = SpikeTimeTilingCoefficient()
            ac.plot()
            spy_super().plot.assert_called_once_with('Spike Time Tiling Coefficient')



if __name__ == '__main__':
    unittest.main()
