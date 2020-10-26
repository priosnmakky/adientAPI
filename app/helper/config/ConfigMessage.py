from jproperties import Properties

class ConfigMessage:

    configs = Properties()

    def __init__(self):

        with open('config/message-config.properties', 'rb') as config_file:
            self.configs.load(config_file)