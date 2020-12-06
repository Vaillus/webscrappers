#import discord_notify as dn
from .sniper_spider import *
import json
import os
from .utils import get_params



class SpiderManager:
    def __init__(self, params={}):
        self.spider_data = None

        self.set_params_from_dict(params=params)
    
    def set_params_from_dict(self, params):
        if not params:
            params = get_params("spider_data.json")
        self.spider_data = params

    # ================================================================

    def execute_spiders(self, spider_names):
        """ get the results of the spiders whose names are specified
        Args: spider_names ([str])
        Returns: dictionary: containing the fields 'target', 'success' and 'parsed'
        """
        results = {}
        for spider_name in spider_names:
            results[spider_name] = self.execute_spider(spider_name)
        return results
    
    def execute_spider(self, spider_name):
        """ get the results of the spider whose name is specified
        Args: spider_name (str)
        Returns: dictionary: containing the fields 'target', 'success' and 'parsed'
        """
        spider_params = self.spider_data[spider_name]
        result = self._execute_spider_params(spider_params)
        return result

    def _execute_spider_params(self, params):
        """Initialize a spider with specified params, execute it and return dictionary of results
        Args: params (dict)
        Returns: dict: containing the fields 'target', 'success' and 'parsed'
        """
        sniper = SniperSpider(params)
        target_str, success, has_parsed = sniper.shoot()
        result = {
            "target": target_str, 
            "success": success, 
            "parsed": has_parsed
                }

        return result

    


if __name__ == "__main__":
    
    params = get_params("spider_data")
    sm = SpiderManager(params)
    results = sm.execute_spiders(["processor_ldlc", "processor_amd", "processor_topachat"])
    print(results)