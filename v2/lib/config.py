import yaml

class Config:
    '''
    This class is purely for loading in static configuration, like read-only
    SNMP data. The below function reads in 'config.yaml', and parses the YAML
    structure into a dictionary. Once the file has already been read in once, 
    it is cached into the class variable for a quick and easy passing of the
    data.
    '''

    cfg: dict = {}
    
    @staticmethod
    def get():
        if Config.cfg == {}:
            '''
            I choose to do this in a blocking (non-async) manner, due to 
            this snippet being more than likely executed at beginning of
            a script, where no real async tasks are taking place at the
            moment.
            '''
            with open("config.yaml", "r") as f:
                Config.cfg = yaml.safe_load(f)
                
        return Config.cfg