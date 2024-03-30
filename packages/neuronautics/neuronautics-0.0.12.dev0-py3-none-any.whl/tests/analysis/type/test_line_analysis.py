import unittest
from unittest.mock import patch, MagicMock
from neuronautics.analysis.type.line_analysis import LineAnalysis
from neuronautics.analysis.type.abstract_analysis import AnalysisType
from matplotlib.figure import Figure
import pandas as pd
import numpy as np


class OneLineAnalysis(LineAnalysis):

    def run(self, *args, **kwargs):
        return pd.DataFrame({'A': [1,2], 'B': [3,4]})

    def get_input_params(self):
        pass


class TestBarAnalysis(unittest.TestCase):
    def test_type(self):
        analysis = OneLineAnalysis()
        self.assertEqual(analysis.type(), AnalysisType.LINE)

    @patch("matplotlib.pyplot.subplots")
    def test_plot(self, mock_subplots):
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        # Act
        analysis = OneLineAnalysis()
        result = analysis.plot(title='my plot')

        # Assert
        self.assertEqual(result, mock_fig)
        mock_ax.plot.assert_called_once()


if __name__ == '__main__':
    unittest.main()
