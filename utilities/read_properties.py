from .path_finder import get_path_to_file
from .project_logger import get_logger
import configparser

logger = get_logger(logger_name=__name__)

def interpret_config_file(path: str = get_path_to_file('configs', 'creds.ini')):
    """Read and return a config parser object"""

    config_object = configparser.ConfigParser()

    try:
        config_object.read(path)
    except Exception:
        logger.exception("Error reading the config file")
        return None

    return config_object


def extract_specific_data(results: dict = None, section: str = None, option: str = None):
    """Extract specific data when specified section and options available"""

    if section is not None and option is None:
        return results[section]
    if section is not None and option is not None:
        results[section][option]

    return results


def read_config_file(
        config_path: str =  get_path_to_file('configs', 'creds.ini'), 
        section: str = None, 
        option: str = None):
    """Read a config file"""

    config_object = interpret_config_file(path=config_path)

    results = {}

    for section_config in config_object.sections():
        section_dict = {}

        for option_config in config_object.options(section_config):
            try:
                section_dict[option_config] = config_object.get(section_config, option_config)
            except Exception:
                logger.exception(f"Error reading option {option} in section {section}")

        results[section_config] = section_dict

    return extract_specific_data(results=results, section=section, option=option)