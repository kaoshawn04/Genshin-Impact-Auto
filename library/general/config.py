import configparser


def get_config(section: str):
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    
    return {
        key: config[section][key]
        for key in config[section]
    }