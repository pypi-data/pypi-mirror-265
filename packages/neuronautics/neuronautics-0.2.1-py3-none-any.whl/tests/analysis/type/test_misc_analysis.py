import unittest
from neuronautics.analysis.type.misc_analysis import MiscAnalysis
from neuronautics.analysis.type.abstract_analysis import AnalysisType


class OneMiscAnalysis(MiscAnalysis):

    def run(self, *args, **kwargs):
        pass

    def get_input_params(self):
        pass

    def plot(self, *args, **kwargs):
        pass


class TestBarAnalysis(unittest.TestCase):
    def test_type(self):
        analysis = OneMiscAnalysis()
        self.assertEqual(analysis.type(), AnalysisType.OTHER)



if __name__ == '__main__':
    unittest.main()
