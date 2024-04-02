import pygrib
import xarray as xr

def load_data(file_path):
    """
    Load data from a GRIB or NetCDF4 file.
    
    Args:
        file_path (str): Path to the data file.
    
    Returns:
        numpy.ndarray: Loaded data as a numpy array.
    """
    if file_path.endswith(".grib"):
        with pygrib.open(file_path) as grbs:
            data = grbs.read_values()
    elif file_path.endswith(".nc"):
        ds = xr.open_dataset(file_path)
        data = ds.to_array().values
        ds.close()
    else:
        raise ValueError("Unsupported file format. Only GRIB and NetCDF4 are supported.")
    
    return data