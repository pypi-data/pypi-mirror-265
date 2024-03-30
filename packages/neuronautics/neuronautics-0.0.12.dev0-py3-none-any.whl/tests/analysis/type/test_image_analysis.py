import unittest
from unittest.mock import patch, MagicMock
from neuronautics.analysis.type.image_analysis import ImageAnalysis
from neuronautics.analysis.type.abstract_analysis import AnalysisType
from matplotlib.figure import Figure
import pandas as pd
import numpy as np


class OneImageAnalysis(ImageAnalysis):

    def run(self, *args, **kwargs):
        return np.array([[0, 1], [1, 0]])

    def get_input_params(self):
        pass


class TestImageAnalysis(unittest.TestCase):
    def test_type(self):
        analysis = OneImageAnalysis()
        self.assertEqual(analysis.type(), AnalysisType.IMAGE)

    @patch("matplotlib.pyplot.subplots")
    def test_plot(self, mock_subplots):
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        # Act
        analysis = OneImageAnalysis()
        result = analysis.plot(title='my plot')

        # Assert
        self.assertEqual(result, mock_fig)
        mock_ax.imshow.assert_called_once()

    @patch("matplotlib.pyplot.colorbar")
    @patch("matplotlib.pyplot.subplots")
    def test_plot_cmap(self, mock_subplots, mock_colorbar):
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        # Act
        analysis = OneImageAnalysis()
        result = analysis.plot(title='my plot', cmap='Reds')

        # Assert
        self.assertEqual(result, mock_fig)
        mock_ax.imshow.assert_called_once()
        mock_colorbar.assert_called_once()


if __name__ == '__main__':
    unittest.main()
