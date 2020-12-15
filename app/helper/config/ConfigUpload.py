from jproperties import Properties

class ConfigsUpload:

    configs = Properties()

    def __init__(self):

        with open('config/upload-config.properties', 'rb') as config_file:
            self.configs.load(config_file)
