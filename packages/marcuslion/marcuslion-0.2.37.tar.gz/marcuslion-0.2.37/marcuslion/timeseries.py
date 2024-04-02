import io
import urllib
import urllib3

import pandas as pd

from marcuslion.config import api_version
from marcuslion.restcontroller import RestController


class TimeSeries(RestController):
    """
    https://qa1.marcuslion.com/swagger-ui/index.html#/time-series-api-controller
    """

    def __init__(self):
        super().__init__(api_version + "/timeseries/history")

    def list(self) -> pd.DataFrame:
        """
        Indicators.list()
        """
        return super().verify_get()

    def list(self, symbol, interval, page_size) -> pd.DataFrame:
        """
        Indicators.list()
        """
        return super().verify_get(symbol + "/" + interval + "/" + str(page_size), {})

    def query(self, ref):
        return super().verify_get_data("query", {"ref", ref})

    def search(self, search) -> pd.DataFrame:
        return super().verify_get_data("search", {"search", search})

    def download(self, params) -> pd.DataFrame:
        """
        Indicators.download(ref, params)
        """
        res = super().verify_get("", params)
        if res is None or 'data' not in res:
            return pd.DataFrame()
        return pd.DataFrame(res['data'], columns=res['schema'])

    def subscribe(self, ref, params):
        """
        Indicators.subscribe(ref, params)
        """
        pass
