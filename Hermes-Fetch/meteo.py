import requests
import pandas as pd

class MeteoData:

    def __init__(self, resp: requests.Response) -> None:

        self.resp = resp.json() if isinstance(resp, requests.Response) else resp
        self.lat = self.resp['latitude']
        self.lon = self.resp['longitude']
        self.timezone = self.resp['timezone']
        self.units = self.resp['current_units'] # assuming variables have the same unit as current

    def get_forecast(self, forecast_type: str, time='time') -> pd.DataFrame:
        """Returns a single dataframe of a specified type of forecast

        Args:
            forecast_type (str): String specifying the forecast type (minutely_15, hourly, NOT CURRENT...etc.)
            time (str, optional): String specifying the name of the time column. Defaults to 'time'

        Returns:
            pd.DataFrame: pd.DataFrame, includes the time column in datetime and all the variables of interest. 
        """
        if forecast_type not in self.resp:
            raise KeyError("Trying to access a forecast type that isn't present in your API call")

        if forecast_type != 'current':
            df = pd.DataFrame(self.resp[forecast_type])
        else:
            df = pd.DataFrame([self.resp[forecast_type]])

        df[time] = pd.to_datetime(df[time])
        return df
    
    def get_units(self) -> {str:str}:
        return self.units

class MeteoClient:

    def __init__(self, base = 'https://api.open-meteo.com/v1/', params = None):

        self.base = base
        self.params = params
        self.resps = None

    def fetch_forecast(self, params = None) -> None:
        """Fetches data from Open-Meteo API (gives a list of JSON)

        Args:
            params (_type_, optional): Dictionary of structure:

            params = {
            "latitude": [52.52, 51.5085, 52.52],
            "longitude": [13.41, -0.1257, 13.41],
            "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
            "minutely_15": ["temperature_2m", "relative_humidity_2m", "precipitation"],
            "hourly": "temperature_2m",
            "timezone": "America/Los_Angeles",
            "forecast_days": 1
            }

            Defaults to None.

        Raises:
            e: Failed request
        """
        parameters = params if params else self.params
        try:
            self.resps = requests.get(f'{self.base}/forecast',
                                    params=parameters)
        except Exception as e:
            print('Error while fetching forecast data')
            self.resp = None
            raise e

    def gen_meteo_data(self):
        """Generator of MeteoData Objects from self.resps
        """
        for resp in self.resps.json():
            yield MeteoData(resp)
        
    def gen_forecasts(self, forecast_type:[str]):
        """Generates (lon,lat), forecast_type, pd.DataFrame

        Args:
            forecast_type ([str]): List of forecasts to extract (current, hourly, minutely_15min)
        """
        for meteo in self.gen_meteo_data():
            for fore in forecast_type:
                yield (meteo.lon, meteo.lat), fore, meteo.get_forecast(fore)
