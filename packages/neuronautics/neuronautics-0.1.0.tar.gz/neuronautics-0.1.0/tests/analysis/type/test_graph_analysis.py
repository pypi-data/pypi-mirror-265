import unittest
from unittest.mock import patch, MagicMock
from neuronautics.analysis.type.graph_analysis import GraphAnalysis
from neuronautics.analysis.type.abstract_analysis import AnalysisType
from matplotlib.figure import Figure
import pandas as pd
import numpy as np


class OneGraphAnalysis(GraphAnalysis):

    def run(self, *args, **kwargs):
        return np.array([[0, 1], [1, 0]])

    def get_input_params(self):
        pass


class TestGraphAnalysis(unittest.TestCase):
    def test_type(self):
        analysis = OneGraphAnalysis()
        self.assertEqual(analysis.type(), AnalysisType.GRAPH)

    @patch("networkx.draw")
    def test_plot(self, mock_draw):
        # Act
        analysis = OneGraphAnalysis()
        result = analysis.plot(title='my plot')

        # Assert
        self.assertIsInstance(result, Figure)
        mock_draw.assert_called_once()


if __name__ == '__main__':
    unittest.main()
