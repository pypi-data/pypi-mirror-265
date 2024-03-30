import unittest
from unittest.mock import patch, MagicMock, call
from neuronautics.ui.abstract_source import AbstractSource


class MockSource(AbstractSource):
    def _plot_single_view(self, path, channel_id):
        pass

    def _plot_grid_view(self, path):
        pass

    def _plot_list_view(self, channel_id):
        pass

    def load_files(self, folder_path):
        return [folder_path]


class TestAbstractSource(unittest.TestCase):
    def test_constructor(self):
        mock_ui = MagicMock()
        data_handler = MagicMock()

        ms = MockSource(mock_ui, data_handler)

        self.assertEqual(ms.ui, mock_ui)
        self.assertEqual(ms.data_handler, data_handler)

    def test_load_files(self):
        mock_ui = MagicMock()
        data_handler = MagicMock()

        ms = MockSource(mock_ui, data_handler)
        f = ms.load_files('random/folder')
        self.assertListEqual(f, ['random/folder'])

    def test_select_view(self):
        mock_ui = MagicMock()
        data_handler = MagicMock()

        ms = MockSource(mock_ui, data_handler)
        ms.filenames = ['file1', 'file2']
        ms.select_view()
        mock_ui.fileSelector.clear.assert_called_once()
        mock_ui.fileSelector.addItem.assert_has_calls([call('file1'), call('file2')])

    def test_select_file(self):
        mock_ui = MagicMock()
        data_handler = MagicMock()

        ms = MockSource(mock_ui, data_handler)
        with (patch.object(ms, 'load_analog_channels_ids') as spy_laci,
              patch.object(ms, 'plot_info_view') as spy_plot_info_view,
              patch.object(ms, 'plot_multiple_view') as spy_plot_multiple_view,
              patch.object(ms, 'plot_list_view') as spy_plot_list_view
              ):
            ms.select_file()

            spy_laci.assert_called_once()
            spy_plot_list_view.assert_called_once()
            spy_plot_info_view.assert_called_once()
            spy_plot_multiple_view.assert_called_once()

    def test_load_analog_channels_ids_no_files(self):
        mock_ui = MagicMock()
        data_handler = MagicMock()

        ms = MockSource(mock_ui, data_handler)
        mock_ui.fileSelector.currentText.return_value = None

        ms.load_analog_channels_ids()
        mock_ui.channelSelector.clear.assert_not_called()

    def test_load_analog_channels_ids(self):
        mock_ui = MagicMock()
        data_handler = MagicMock()

        ms = MockSource(mock_ui, data_handler)
        mock_ui.fileSelector.currentText.return_value = ['f1', 'f2']
        data_handler.return_value.get_analog_channels_ids.return_value = [1,2,3]

        ms.load_analog_channels_ids()
        mock_ui.channelSelector.clear.assert_called_once()
        mock_ui.channelSelector.addItem.assert_has_calls([call('1'), call('2'), call('3')])

    def test_plot_info_view(self):
        mock_ui = MagicMock()
        data_handler = MagicMock()

        ms = MockSource(mock_ui, data_handler)
        data_handler.return_value.get_info.return_value = {'a': 1, 'b': 2}

        with patch('neuronautics.ui.abstract_source.QtWidgets.QTableWidgetItem') as mck_wgt:
            mck_wgt.side_effect = lambda x: x
            ms.plot_info_view()

        mock_ui.infoTable.setItem.assert_has_calls([call(0, 0, 'a'),
                                                    call(0, 1, 1),
                                                    call(1, 0, 'b'),
                                                    call(1, 1, 2), ])

    def test_plot_single_view(self):
        mock_ui = MagicMock()
        data_handler = MagicMock()

        ms = MockSource(mock_ui, data_handler)
        with patch.object(ms, '_plot_single_view') as mck_single_view:
            ms.plot_single_view()

            mck_single_view.assert_called_once()

    def test_plot_grid_view(self):
        mock_ui = MagicMock()
        data_handler = MagicMock()

        ms = MockSource(mock_ui, data_handler)
        with patch.object(ms, '_plot_grid_view') as mck_view:
            ms.plot_multiple_view()

            mck_view.assert_called_once()

    def test_plot_list_view(self):
        mock_ui = MagicMock()
        data_handler = MagicMock()

        ms = MockSource(mock_ui, data_handler)
        with patch.object(ms, '_plot_list_view') as mck_view:
            ms.plot_list_view()

            mck_view.assert_called_once()


if __name__ == '__main__':
    unittest.main()
