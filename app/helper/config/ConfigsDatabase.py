from jproperties import Properties

class ConfigsDatabase:

    configs = Properties()

    def __init__(self):

        with open('config/database-config.properties', 'rb') as config_file:
            
            self.configs.load(config_file)