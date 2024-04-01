from dataclasses import dataclass
from functools import cached_property
import netCDF4
import numpy as np
from datetime import datetime, timedelta


@dataclass
class WaveDataFile:
    """WaveDataFile class"""
    dataset: netCDF4.Dataset

    @classmethod
    def from_file(cls, filename: str):
        dataset = netCDF4.Dataset(filename)
        return cls(dataset)

    @cached_property
    def variables(self) -> list[str]:
        variables = list(self.dataset.variables.keys())
        drop_variables = ['time', 'latitude', 'longitude']
        variables = [item for item in variables if item not in drop_variables]
        return variables

    @cached_property
    def time(self) -> np.ma.masked_array:
        return self.dataset.variables['time'][:]

    @cached_property
    def datetime(self) -> list[datetime]:
        date_cftimes = netCDF4.num2date(self.time,
                                        self.dataset.variables['time'].units,
                                        self.dataset.variables['time'].calendar)
        date_times = np.ma.masked_array(
            data=[datetime(*d.timetuple()[:6]) for d in date_cftimes],
            mask=date_cftimes.mask
        )
        return date_times

    @cached_property
    def time_min(self) -> str:
        # Να το αλλάξω σε np min. Δουλεύει πολύ αργά έτσι
        return min(self.dataset.variables['time'])

    @cached_property
    def datetime_min(self) -> datetime:
        return self.datetime[0]

    @cached_property
    def datetime_max(self) -> datetime:
        return self.datetime[-1]

    @cached_property
    def time_max(self) -> str:
        return max(self.dataset.variables['time'])

    @cached_property
    def lon(self) -> np.ma.masked_array:
        return self.dataset.variables['longitude'][:]

    @cached_property
    def lat(self) -> np.ma.masked_array:
        return self.dataset.variables['latitude'][:]


@dataclass
class WaveVariable:
    """WaveVariable class"""
    wdf: WaveDataFile
    name: str

    @property
    def long_name(self) -> str:
        return self.wdf.dataset.variables[self.name].long_name

    @cached_property
    def values(self) -> np.ma.masked_array:
        return self.wdf.dataset.variables[self.name][:]

    @cached_property
    def min_value(self) -> float:
        return self.values.min()

    @cached_property
    def max_value(self) -> float:
        return self.values.max()

    def get_time_history_at_indices(
            self, lat_index: int, lon_index: int,
            start_date_index: int = 0,
            end_date_index: int = -1) -> np.ma.masked_array:
        """
        Get values from a masked array at specified indices across all arrays.

        Parameters:
            lat_index (int): Index along the lat dimension.
            lon_index (int): Index along the lon dimension.

        Returns:
            np.ma.masked_array: Array of values at the specified coord indices
                                for each time step.
        """
        values = self.values[start_date_index:end_date_index, lat_index, lon_index]
        return values

    def get_time_history_at_coords(
            self, lat: float, lon: float) -> np.ma.masked_array:
        """
        Get values from a masked array at specified coordinates across all arrays.

        Parameters:
            lat (float): Latitude.
            lon (float): Longitude.

        Returns:
            np.ma.masked_array: Array of values at the specified coords
                                for each time step.
        """
        lat_index = np.where(self.wdf.lat == lat)[0][0]
        lon_index = np.where(self.wdf.lon == lon)[0][0]
        return self.get_time_history_at_indices(lat_index, lon_index)
