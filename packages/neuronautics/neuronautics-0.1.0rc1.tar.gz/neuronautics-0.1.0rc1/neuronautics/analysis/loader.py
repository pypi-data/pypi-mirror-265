import importlib
import importlib.util
import yaml
from pathlib import Path
from ..utils.helpers import file_path, load_yaml, app_path
from ..utils.singleton import Singleton

from ..recordings.config import YML_ANALYSIS_BASE


BASE_ANALYTICS = YML_ANALYSIS_BASE
EXTRA_ANALYTICS = file_path('analysis/extra.yml')
# TODO: raised exceptions can be customised


class Loader(metaclass=Singleton):
    """
    A Singleton class that loads and manages analysis configurations.

    Attributes:
        analysis_handle (dict): A dictionary to hold the analysis handles.
        analysis_config (dict): A dictionary to hold the analysis configurations.
    """
    def __init__(self):
        """
        Initializes the Loader instance.
        """
        self.analysis_handle = None
        self.analysis_config = None

    def load(self):
        """
        Loads the analysis configuration from the base and extra analytics files.
        """
        base = load_yaml(BASE_ANALYTICS, list())
        analysis = load_yaml(EXTRA_ANALYTICS, list())
        for b in base:
            if not any([b.get('name') == an.get('name') for an in analysis]):
                analysis.append(b)
        analysis = sorted(analysis, key=lambda an: an.get('name'))

        self.analysis_handle = {name: handle for name, handle in [Loader._instance_analysis(an) for an in analysis]}
        self.analysis_config = {config.get('name'): config for config in analysis}

    def get_analysis_path(self, name: str) -> str:
        """
        Gets the path of the analysis.

        Args:
            name (str): The name of the analysis.

        Returns:
            str: The path of the analysis.
        """
        path = self.analysis_config[name].get('path')
        if path:
            return file_path(path)
        return None

    @classmethod
    def _instance_analysis(cls, analysis: dict) -> tuple:
        """
        Instantiates the analysis.

        Args:
            analysis (dict): The analysis configuration.

        Returns:
            tuple: A tuple containing the name of the analysis and the dynamic class instance.
        """

        try:
            module = cls._get_module(analysis.get('module'), analysis.get('path'))
            dynamic_class = getattr(module, analysis.get('class'))()
            return analysis.get('name'), dynamic_class
        except Exception as e:
            raise e

    @classmethod
    def check_module(cls, analysis: dict) -> bool:
        """
        Checks the module.

        Args:
            analysis (dict): The analysis configuration.

        Returns:
            bool: True if the module is valid, False otherwise.
        """
        try:
            name, instance = cls._instance_analysis(analysis)
            params_def = instance.get_input_params()
            params = {param['name']: param['default'] for param in params_def}
            instance.run(None, **params)
        except:
            return False
        return True

    def get_types(self) -> dict:
        """
        Gets the types of the analysis.

        Returns:
            dict: A dictionary mapping the name of the analysis to its type.
        """
        return {name: handle.type() for name, handle in self.analysis_handle.items()}

    @staticmethod
    def load_and_execute_class(module_name: str, class_name: str) -> tuple:
        """
        Loads and executes a class.

        Args:
            module_name (str): The name of the module.
            class_name (str): The name of the class.

        Returns:
            tuple: A tuple containing the result of the input parameters and the execution.
        """
        try:
            module = Loader._get_module(module_name)
            dynamic_class = getattr(module, class_name)
            instance = dynamic_class()

            input_params_result = instance.get_input_params()
            execute_result = instance.execute()

            return input_params_result, execute_result
        except Exception as e:
            return f"Error: {e}", ""

    @staticmethod
    def _get_module(module_name: str, path: str = None):
        """
        Gets the module.

        Args:
            module_name (str): The name of the module.
            path (str, optional): The path of the module. Defaults to None.

        Returns:
            module: The module.
        """
        try:
            module = importlib.import_module(module_name)
        except:
            spec = importlib.util.spec_from_file_location(module_name, file_path(path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        return module

    @classmethod
    def save(cls, config: dict):
        """
        Saves the configuration.

        Args:
            config (dict): The configuration to save.
        """
        cls.delete(config['name'])
        analysis = load_yaml(EXTRA_ANALYTICS, list())
        if Loader.check_module(config):
            analysis.append(config)
            cls._dump(analysis)

    @classmethod
    def delete(cls, name: str):
        """
        Deletes the analysis.

        Args:
            name (str): The name of the analysis to delete.
        """
        analysis = load_yaml(EXTRA_ANALYTICS, list())
        analysis = [an for an in analysis if an.get('name').upper() != name.upper()]
        cls._dump(analysis)

    @classmethod
    def _dump(cls, analysis: list):
        """
        Dumps the analysis.

        Args:
            analysis (list): The analysis to dump.
        """
        with open(EXTRA_ANALYTICS, 'w') as stream:
            yaml.dump(analysis, stream)

