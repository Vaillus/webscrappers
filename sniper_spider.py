import urllib.request
from bs4 import BeautifulSoup
import os
import json
import requests
from .utils import get_params

class SniperSpider:
    """Used to get a single inofrmation on a single web page.
    """
    def __init__(self, params={}):
        self.url = None
        self.request = None

        self.http_string = None
        self.expected_value = None

        self.set_params_from_dict(params=params)

    def set_params_from_dict(self, params):
        self.url = params.get("url", "")
        self.request = params.get("request", [])
        self.expected_value = params.get("expected_value", "")

    # ==================================================================

    def shoot(self):
        """Load the web page and get the desired information from it
        Returns:
            str: info from web page
        """
        target = ""
        # Get the web page
        self._get_http_string()
        # Try to access the data in the web page
        try:
            target = self._aim()
        except:
            target = "None"
            print(f"The spider of {self.url} couldn't aim at the target")
        # determining whether the page was parsed and the spider succeeded
        success, parsed = self._pull_triger(target)
        return target, success, parsed    
    
    def _get_http_string(self):
        """call the web page, format it to be readable by beatifulsoup
         and store the result in http_string
        """
        try: 
            rep = requests.get(self.url, timeout=0.5)
            self.http_string = rep.content.decode("utf8")
            self.http_string = BeautifulSoup(self.http_string, 'html.parser')
            print(len(self.http_string))
        except:
            self.http_string = "None"
            print(f"Couldn't get {self.url} http string") 

    
    def _aim(self):
        """Read the web page and get the information

        Args:
            request (dictionary): defines the cell information where the data is.

        Returns:
            str: info from web page
        """
        if self.http_string != "None":
            http_sel = self.http_string
            for step in self.request:
                # assign parameters of the parsing
                params = {"name": step["cell_type"]}
                if step.get("class", ""):
                    params["class_"]= step["class"]
                http_sel = http_sel.find(**params)
                # result is the class attribute of the cell if it has been found
                if step.get("test_presence", False) and http_sel:
                    result = step.get("class", "None")
                # result is the content of the cell
                elif step.get("string", False):
                    result = http_sel.string
                else:
                    result = "None"
        else:
            result = "None"
        return result

    def _pull_triger(self, parsing_result):
        """indicate wheter the page was parsed and the spider found the value expected
        Args: parsing_result (string): the value returned by the spider
        Returns: success, parsed (bool, bool)
        """
        if parsing_result == self.expected_value:
            success = True
            parsed = True
        elif parsing_result == "None":
            success = False
            parsed = False
        else:
            success = False
            parsed = True

        return success, parsed



if __name__ == "__main__":
    params = {
        "url": "",
        "request": {  
            "cell_type" : "div", 
            "class" : "product-page-description col-flex-lg-5 col-flex-sm-12",
            "string" : False
        }
    }
    params = get_params("spider_data")["processor_topachat"]
    #print(params)
    sniper = SniperSpider(params)
 
    result, success, parsed = sniper.shoot()
 
    print(result, success, parsed)