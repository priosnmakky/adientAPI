from jproperties import Properties

class ConfigPart:

    configs = Properties()

    def __init__(self):

        with open('config/part-config.properties', 'rb') as config_file:
            self.configs.load(config_file)