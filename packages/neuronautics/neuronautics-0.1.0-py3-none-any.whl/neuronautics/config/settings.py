import yaml
from pathlib import Path
from enum import Enum

from ..utils.helpers import file_path
from ..utils.singleton import Singleton

# TODO: tiene que ser capaz de leer y modificar en tiempo real


class SubSettings:
    def __getattr__(self, item):
        pass


class Settings(metaclass=Singleton):
    FILE = file_path('settings.yml')

    def __init__(self):
        settings = self.load()
        self.ui_spike = UiSpikeSettings(**settings)
        self.ui_raw = UiRawSettings(**settings)

    def save(self):
        settings = {k: v.__dict__ for k,v in self.__dict__.items()}
        with open(Settings.FILE, 'w') as stream:
            yaml.dump(settings, stream)

    @classmethod
    def load(cls):
        if Path(Settings.FILE).exists():
            with open(Settings.FILE, 'r') as stream:
                data = yaml.full_load(stream)
                if not data:
                    return dict()
                return data
        else:
            return dict()


class UiSpikeSettings(SubSettings, metaclass=Singleton):

    def __init__(self, ui_spike=None, **kwargs):
        self.SINGLE_VIEW_LENGTH_S = 5
        self.GRID_VIEW_STACKED_S = 30
        self.GRID_VIEW_TIMESERIES_S = 3
        self.MICRO_VOLTS_RANGE = None  # None or tuple e.g (-200, 200)
        if ui_spike:
            for key in ui_spike:
                setattr(self, key, ui_spike[key])

    def set_single_view(self, val):
        self.SINGLE_VIEW_LENGTH_S = val

    def set_grid_stacked_view(self, val):
        self.GRID_VIEW_STACKED_S = val

    def set_grid_timeseries_view(self, val):
        self.GRID_VIEW_TIMESERIES_S = val

    def set_volts_range(self, min_val, max_val):
        if min_val == 0 and max_val == 0:
            self.MICRO_VOLTS_RANGE = None
        else:
            self.MICRO_VOLTS_RANGE = (min_val, max_val)

    def set_volts_min(self, min_val):
        if self.MICRO_VOLTS_RANGE is None:
            self.set_volts_range(min_val, 0)
        else:
            self.set_volts_range(min_val, self.MICRO_VOLTS_RANGE[1])

    def set_volts_max(self, max_val):
        if self.MICRO_VOLTS_RANGE is None:
            self.set_volts_range(0, max_val)
        else:
            self.set_volts_range(self.MICRO_VOLTS_RANGE[0], max_val)


class UiRawSettings(SubSettings, metaclass=Singleton):

    def __init__(self, ui_raw=None, **kwargs):
        self.SINGLE_VIEW_LENGTH_S = 5
        self.GRID_VIEW_LENGTH_S = .3
        self.MICRO_VOLTS_RANGE = None
        if ui_raw:
            for key in ui_raw:
                setattr(self, key, ui_raw[key])

    def set_single_view(self, val):
        self.SINGLE_VIEW_LENGTH_S = val

    def set_grid_view(self, val):
        self.GRID_VIEW_LENGTH_S = val

    def set_volts_range(self, min_val, max_val):
        if min_val == 0 and max_val == 0:
            self.MICRO_VOLTS_RANGE = None
        else:
            self.MICRO_VOLTS_RANGE = (min_val, max_val)

    def set_volts_min(self, min_val):
        if self.MICRO_VOLTS_RANGE is None:
            self.set_volts_range(min_val, 0)
        else:
            self.set_volts_range(min_val, self.MICRO_VOLTS_RANGE[1])

    def set_volts_max(self, max_val):
        if self.MICRO_VOLTS_RANGE is None:
            self.set_volts_range(0, max_val)
        else:
            self.set_volts_range(self.MICRO_VOLTS_RANGE[0], max_val)
