# NOTE: needs to create an app for the testing, but then other tests start failing. I will keep it commented for the future
#
# import unittest
# from PyQt5 import QtWidgets
# from unittest.mock import patch
# from neuronautics.analysis.analysis_creator import AnalysisCreatorUi
#
#
# class TestAnalysisCreatorUi(unittest.TestCase):
#     def setUp(self):
#         self.app = QtWidgets.QApplication([])
#         self.dialog = AnalysisCreatorUi()
#
#     def tearDown(self):
#         self.app.quit()
#
#     @patch('neuronautics.analysis.analysis_creator.open_external_editor')
#     @patch('neuronautics.analysis.analysis_creator.AnalysisCreator.create')
#     @patch('neuronautics.utils.logger.Logger')
#     def test_create_analysis(self, mock_logger, mock_create, mock_open_editor):
#         mock_create.return_value = '/path/to/analysis'
#         self.dialog.analysisName.setText('Test Analysis')
#
#         self.dialog.create_analysis()
#
#         mock_create.assert_called_once_with('Test Analysis', 'line')
#         mock_open_editor.assert_called_once_with('/path/to/analysis')
#
# if __name__ == '__main__':
#     unittest.main()
