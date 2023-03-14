from exception.exception import InvalidConversionException
import os

def human_format_to_float(str):
    if "G" in str:
        if str.split("G")[1] != "":
            raise InvalidConversionException("Invalid format")
        return float(str.split("G")[0]) * 1000000000
    elif "M" in str:
        if str.split("M")[1] != "":
            raise InvalidConversionException("Invalid format")
        return float(str.split("M")[0]) * 1000000
    elif "K" in str:
        if str.split("K")[1] != "":
            raise InvalidConversionException("Invalid format")
        return float(str.split("K")[0]) * 1000
    elif "m" in str:
        if str.split("m")[1] != "":
            raise InvalidConversionException("Invalid format")
        return float(str.split("m")[0]) / 1000
    else:
        raise InvalidConversionException("Invalid format")
    
def generate_os_path(original):
    return os.path.join("..", original)
   
def check_correct_application_config(config):
    if "number_of_applications" not in config:
        return False
    if "application_urgency_ratio" not in config["app_spec"]:
        return False
    if "min_n_node" not in config["app_spec"]:
        return False
    if "max_n_node" not in config["app_spec"]:
        return False
    if "min_task_n_core_requirements" not in config["app_spec"]:
        return False
    if "max_task_n_core_requirements" not in config["app_spec"]:
        return False
    if "min_task_operation_requirements" not in config["app_spec"]:
        return False
    if "max_task_operation_requirements" not in config["app_spec"]:
        return False
    if "min_task_edge_requirements" not in config["app_spec"]:
        return False
    if "max_task_edge_requirements" not in config["app_spec"]:
        return False
    if "task_connectivity_ratio" not in config["app_spec"]:
        return False
    return True

def generate_app_name(id):
    return "app_" + str(id)

def generate_app_node_id(id):
    return "app_node_" + str(id)
    
def generate_app_edge_id(id):
    return "app_edge_" + str(id)
    