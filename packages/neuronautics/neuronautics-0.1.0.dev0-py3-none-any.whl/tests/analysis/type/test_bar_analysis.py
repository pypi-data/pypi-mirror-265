import unittest
from unittest.mock import patch, MagicMock
from neuronautics.analysis.type.bar_analysis import BarAnalysis
from neuronautics.analysis.type.abstract_analysis import AnalysisType
from matplotlib.figure import Figure
import pandas as pd


class OneBarAnalysis(BarAnalysis):

    def run(self, *args, **kwargs):
        return pd.DataFrame({'A': [1,2], 'B': [3,4]})

    def get_input_params(self):
        pass


class TestBarAnalysis(unittest.TestCase):
    def test_type(self):
        analysis = OneBarAnalysis()
        self.assertEqual(analysis.type(), AnalysisType.BAR)

    @patch("matplotlib.pyplot.xticks")
    @patch("matplotlib.pyplot.legend")
    @patch("matplotlib.pyplot.title")
    @patch("matplotlib.pyplot.tight_layout")
    def test_plot_vertical(self, mock_xticks, mock_legend, mock_title, mock_tight_layout):
        # Act
        bar_analysis = OneBarAnalysis()
        result = bar_analysis.plot(value_units='', stacked=True, vertical=True, title='')

        # Assert
        self.assertIsInstance(result, Figure)
        mock_xticks.assert_called_once()
        mock_legend.assert_called_once()
        mock_title.assert_called_once()
        mock_tight_layout.assert_called_once()

    @patch("matplotlib.pyplot.yticks")
    @patch("matplotlib.pyplot.legend")
    @patch("matplotlib.pyplot.title")
    @patch("matplotlib.pyplot.tight_layout")
    def test_plot_horizontal(self, mock_yticks, mock_legend, mock_title, mock_tight_layout):
        # Act
        bar_analysis = OneBarAnalysis()
        result = bar_analysis.plot(value_units='', stacked=True, vertical=False, title='')

        # Assert
        self.assertIsInstance(result, Figure)
        mock_yticks.assert_called_once()
        mock_legend.assert_called_once()
        mock_title.assert_called_once()
        mock_tight_layout.assert_called_once()

    @patch("matplotlib.pyplot.yticks")
    @patch("matplotlib.pyplot.legend")
    @patch("matplotlib.pyplot.title")
    @patch("matplotlib.pyplot.tight_layout")
    def test_plot_no_stacked(self, mock_yticks, mock_legend, mock_title, mock_tight_layout):
        # Act
        bar_analysis = OneBarAnalysis()
        result = bar_analysis.plot(value_units='', stacked=False, vertical=False, title='')

        # Assert
        self.assertIsInstance(result, Figure)
        mock_yticks.assert_called_once()
        mock_legend.assert_called_once()
        mock_title.assert_called_once()
        mock_tight_layout.assert_called_once()


if __name__ == '__main__':
    unittest.main()
