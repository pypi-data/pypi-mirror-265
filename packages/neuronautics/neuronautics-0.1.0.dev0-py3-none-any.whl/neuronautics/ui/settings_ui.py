from ..utils.singleton import Singleton
from ..config.settings import Settings

settings = Settings()


class SettingsUi(metaclass=Singleton):
    def __init__(self, ui):
        self.ui = ui
        self._mapping_tab = {
            'Raw': self.ui.rawSettings,
            'Spike': self.ui.spikeSettings
        }
        self._config_raw_settings()
        self._config_spike_settings()

    def _config_spike_settings(self):
        self.ui.spikeSingleViewLen.setValue(settings.ui_spike.SINGLE_VIEW_LENGTH_S)
        self.ui.spikeGridStackedViewLen.setValue(settings.ui_spike.GRID_VIEW_STACKED_S)
        self.ui.spikeGridTSViewLen.setValue(settings.ui_spike.GRID_VIEW_TIMESERIES_S)
        if settings.ui_spike.MICRO_VOLTS_RANGE is None:
            self.ui.spikeMinRange.setValue(.0)
            self.ui.spikeMaxRange.setValue(.0)
        else:
            self.ui.spikeMinRange.setValue(settings.ui_spike.MICRO_VOLTS_RANGE[0])
            self.ui.spikeMaxRange.setValue(settings.ui_spike.MICRO_VOLTS_RANGE[1])
        self.ui.spikeSingleViewLen.valueChanged.connect(settings.ui_spike.set_single_view)
        self.ui.spikeGridStackedViewLen.valueChanged.connect(settings.ui_spike.set_grid_stacked_view)
        self.ui.spikeGridTSViewLen.valueChanged.connect(settings.ui_spike.set_grid_timeseries_view)
        self.ui.spikeMinRange.valueChanged.connect(settings.ui_spike.set_volts_min)
        self.ui.spikeMaxRange.valueChanged.connect(settings.ui_spike.set_volts_max)

    def _config_raw_settings(self):
        self.ui.rawSingleViewLen.setValue(settings.ui_raw.SINGLE_VIEW_LENGTH_S)
        self.ui.rawGridViewLen.setValue(settings.ui_raw.GRID_VIEW_LENGTH_S)
        if settings.ui_raw.MICRO_VOLTS_RANGE is None:
            self.ui.rawMinRange.setValue(.0)
            self.ui.rawMaxRange.setValue(.0)
        else:
            self.ui.rawMinRange.setValue(settings.ui_raw.MICRO_VOLTS_RANGE[0])
            self.ui.rawMaxRange.setValue(settings.ui_raw.MICRO_VOLTS_RANGE[1])
        self.ui.rawSingleViewLen.valueChanged.connect(settings.ui_raw.set_single_view)
        self.ui.rawGridViewLen.valueChanged.connect(settings.ui_raw.set_grid_view)
        self.ui.rawMinRange.valueChanged.connect(settings.ui_raw.set_volts_min)
        self.ui.rawMaxRange.valueChanged.connect(settings.ui_raw.set_volts_max)

    def settings_selected(self, item, index):
        selected_item = item.text(0)
        wgt = self.ui.stackedSettings
        wgt.setCurrentWidget(self._mapping_tab.get(selected_item, self.ui.emptySettings))

    def save(self):
        settings.save()