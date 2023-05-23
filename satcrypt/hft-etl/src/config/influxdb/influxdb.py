
from config.config import Config


class InfluxDbConfig(Config):
    config_name = 'influxdb'

    def __init__(self):
        config_file = "./src/config/influxdb/config.json"
        super().__init__("influxdb", config_file)

    @property
    def config(self):
        return self.get_config(self.config_name)
    
    @property
    def url(self):
        return self.get_property(self.config_name, 'url')
    
    @property
    def org(self):
        return self.get_property(self.config_name, 'org')

    @property
    def token(self):
        return self.get_property(self.config_name, 'token')

    @property
    def bucket(self):
        return self.get_property(self.config_name, 'bucket')
