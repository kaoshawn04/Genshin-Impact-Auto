import configparser


def get_config(section: str, args: list):
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    
    return {
        arg: config[section][arg]
        for arg in args
    }