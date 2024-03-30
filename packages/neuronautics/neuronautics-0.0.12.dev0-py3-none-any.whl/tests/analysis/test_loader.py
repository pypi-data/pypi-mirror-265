import unittest
from unittest.mock import patch, MagicMock

from neuronautics.analysis.loader import Loader


class TestLoader(unittest.TestCase):
    def setUp(self):
        self.loader = Loader()

    @patch('neuronautics.analysis.loader.load_yaml')
    def test_load(self, mock_load_yaml):
        # Setup
        Loader._instance_analysis = MagicMock(return_value=('test', 'class'))
        mock_load_yaml.return_value = [{'name': 'test'}]
        # Call
        self.loader.load()
        # Assert
        self.assertEqual(self.loader.analysis_config, {'test': {'name': 'test'}})
    @patch('neuronautics.analysis.loader.load_yaml')
    def test_load_2(self, mock_load_yaml):
        # Setup
        Loader._instance_analysis = MagicMock(return_value=('test', 'class'))
        mock_load_yaml.side_effect = [[{'name': 'test'}], [{'name': 'othertest'}]]
        # Call
        self.loader.load()
        # Assert
        self.assertEqual(self.loader.analysis_config, {'othertest': {'name': 'othertest'},
                                                       'test': {'name': 'test'}})

    @patch('neuronautics.analysis.loader.file_path')
    def test_get_analysis_path(self, mock_file_path):
        # Setup
        mock_file_path.return_value = 'mymockedpath'
        self.loader.analysis_config = {'test': {'path': 'test_path'}}
        # Call
        result = self.loader.get_analysis_path('test')
        # Assert
        self.assertEqual(result, 'mymockedpath')

    @patch('neuronautics.analysis.loader.file_path')
    def test_get_analysis_path_none(self, mock_file_path):
        # Setup
        mock_file_path.return_value = 'mymockedpath'
        self.loader.analysis_config = {'test': {}}
        # Call
        result = self.loader.get_analysis_path('test')
        # Assert
        self.assertEqual(result, None)

    @patch('neuronautics.analysis.loader.Loader._get_module')
    def test__instance_analysis(self, mock_get_module):
        # Setup
        mock_module = MagicMock()
        mock_get_module.return_value = mock_module
        mock_module.TestClass = MagicMock()
        # Call
        result = self.loader._instance_analysis({'name': 'test', 'module': 'test_module', 'class': 'TestClass', 'path': 'test_path'})
        # Assert
        self.assertEqual(result, ('test', mock_module.TestClass()))

    def test__instance_analysis_exception(self):
        # Call
        with self.assertRaises(Exception):
            result = self.loader._instance_analysis({'name': 'test', 'module': 'test_module', 'class': 'TestClass', 'path': 'test_path'})

    @patch('neuronautics.analysis.loader.Loader._instance_analysis')
    def test_check_module(self, mock_instance_analysis):
        # Setup
        mock_instance = MagicMock()
        mock_instance.get_input_params.return_value = [{'name': 'param1', 'default': 'value1'}]
        mock_instance.run.return_value = None
        mock_instance_analysis.return_value = ('test', mock_instance)
        # Call
        result = self.loader.check_module({'name': 'test'})
        # Assert
        self.assertTrue(result)

    def test_check_module_fail(self):
        # Call
        result = self.loader.check_module({'name': 'test'})
        # Assert
        self.assertFalse(result)

    def test_get_types(self):
        # Setup
        mock_handle = MagicMock()
        mock_handle.type.return_value = 'test_type'
        self.loader.analysis_handle = {'test': mock_handle}
        # Call
        result = self.loader.get_types()
        # Assert
        self.assertEqual(result, {'test': 'test_type'})

    @patch('neuronautics.analysis.loader.Loader._get_module')
    def test_load_and_execute_class(self, mock_get_module):
        # Setup
        mock_module = MagicMock()
        mock_get_module.return_value = mock_module
        mock_module.TestClass = MagicMock()
        mock_instance = mock_module.TestClass()
        mock_instance.get_input_params.return_value = 'test_input_params'
        mock_instance.execute.return_value = 'test_execute'
        # Call
        result = self.loader.load_and_execute_class('test_module', 'TestClass')
        # Assert
        self.assertEqual(result, ('test_input_params', 'test_execute'))

    def test_load_and_execute_class_exception(self):
        result, execution = self.loader.load_and_execute_class('test_module', 'TestClass')
        # Assert
        self.assertEqual(execution, "")
        self.assertTrue(result.startswith("Error"))

    @patch('neuronautics.analysis.loader.importlib.import_module')
    def test__get_module_import_module(self, mock_import_module):
        # Setup
        mock_module = MagicMock()
        mock_import_module.return_value = mock_module
        # Call
        result = self.loader._get_module('test_module', 'test_path')
        # Assert
        self.assertEqual(result, mock_module)

    @patch('neuronautics.analysis.loader.importlib.import_module', side_effect=Exception())
    @patch('neuronautics.analysis.loader.importlib.util.spec_from_file_location')
    @patch('neuronautics.analysis.loader.importlib.util.module_from_spec')
    def test__get_module(self, mock_module_from_spec, mock_spec_from_file_location, mock_import_module):
        # Setup
        mock_module = MagicMock()
        mock_import_module.return_value = mock_module
        mock_spec = MagicMock()
        mock_spec_from_file_location.return_value = mock_spec
        mock_module_from_spec.return_value = mock_module
        # Call
        result = self.loader._get_module('test_module', 'test_path')
        # Assert
        self.assertEqual(result, mock_module_from_spec.return_value)

    @patch('neuronautics.analysis.loader.Loader.check_module')
    @patch('neuronautics.analysis.loader.load_yaml')
    def test_save(self, mock_load_yaml, mock_check_module):
        # Setup
        Loader._dump = MagicMock(return_value=None)
        mock_check_module.return_value = True
        # Call
        self.loader.save({'name': 'test'})
        # Assert
        Loader._dump.assert_called_with(mock_load_yaml.return_value)

    @patch('neuronautics.analysis.loader.load_yaml')
    @patch('neuronautics.analysis.loader.yaml.dump')
    def test_delete(self, mock_dump, mock_load_yaml):
        # Setup
        mock_load_yaml.return_value = [{'name': 'test'}]
        # Call
        self.loader.delete('test')
        # Assert
        mock_dump.assert_called_once()

if __name__ == '__main__':
    unittest.main()
