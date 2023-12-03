import pandas as pd
import gridstatus

def create_iso_object(iso_name):
    # Check if the attribute exists in the gridstatus module
    if hasattr(gridstatus, iso_name):
        # Get the class based on the iso_name string
        iso_class = getattr(gridstatus, iso_name)
        # Create an instance of the class
        return iso_class()
    else:
        raise ValueError(f"No such ISO class: {iso_name}")
    
def get_current_load(iso_obj) -> pd.DataFrame:
    """Get load data from a given ISO object"""
    return iso_obj.get_load('today')

def get_current_load_forcast(iso_obj) -> pd.DataFrame:
    """Get forecast load data from a given ISO object"""
    return iso_obj.get_load_forecast('today')

# TODO: Fuel Mix, Gas price...etc.