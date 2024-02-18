import yaml

class Config:
    cfg: dict = {}
    
    @staticmethod
    def get():
        if Config.cfg == {}:
            with open("config.yaml", "r") as f:
                Config.cfg = yaml.safe_load(f)
                
        return Config.cfg