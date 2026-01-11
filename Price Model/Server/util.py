import json
import pickle
import numpy as np
import pandas as pd
__city = None
__location = None
__type = None
__data_columns = None
__model = None
json_data = None
locations_data = None  
def get_city_names():
    return __city

def get_location_city_names():
    return __location

def get_types():
    return __type

def get_estimated_price(area, bedroom, bath, property_type, city, location):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
        
    x = np.zeros(len(__data_columns))
    x[0] = area
    x[1] = bedroom
    x[2] = bath
    try:
        type_index = __data_columns.index(property_type.lower())
    except:
        type_index = -1
    try:
        city_index = __data_columns.index(city.lower())
    except:
        city_index = -1
        
    if loc_index >= 0:
        x[loc_index] = 1
    if type_index >= 0:
        x[type_index] = 1
    if city_index >= 0:
        x[city_index] = 1
    return round(__model.predict([x])[0], 0)

def load_saved_artifacts():
    global __data_columns, __city, __model, __type, __location, locations_data, __property_data
    print("Loading saved artifacts...")
    
   
    with open(r"C:\Users\DELL\OneDrive\Desktop\PakEstate-ML-main\Home Price Model\Server\Artifacts\data_columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __type = __data_columns[3:8]
        __city = __data_columns[56:65]
       
        __location = __data_columns[8:56] 

   
    path = r'C:\Users\DELL\OneDrive\Desktop\PakEstate-ML-main\Home Price Model\Model\locations.json'
    with open(path, 'r') as f:
        data = json.load(f)
        locations_data = data["locations_data"]
       
        if isinstance(locations_data, str):
            locations_data = json.loads(locations_data)

 
    with open(r"C:\Users\DELL\OneDrive\Desktop\PakEstate-ML-main\Home Price Model\Server\Artifacts\Pakistan_Home_Prices_Model.pickle", "rb") as f:
        __model = pickle.load(f)
    
    print(f"Successfully loaded {len(locations_data)} records into locations_data.")
    print("Loading saved artifacts...done")


def get_location_names(property_type, city):
    
    if locations_data is None:
        return []
    matching_locations = []
   
    target_type = str(property_type).strip().lower()
    target_city = str(city).strip().lower()

    for record in locations_data:
       
        if record["type"].strip().lower() == target_type and \
           record["location_city"].strip().lower() == target_city:
            matching_locations.extend(record["location"])
            
    return sorted(list(set(matching_locations)))

def validate_property_csp(area, bedroom, bath, property_type):
    """
    CSP Filtering Layer: Checks if the input values satisfy 
    physical and logical real estate constraints.
    """
    # Unary Constraints
    if area < 100 or area > 50000:
        return False, f"Area ({area}) is outside realistic bounds (100-50,000 sqft)."
    
    if bedroom < 0 or bedroom > 15:
        return False, "Bedroom count must be between 0 and 15."

    # Binary Constraints: Validating relationships
   
    if bedroom > 0 and (area / bedroom) < 200:
        return False, "Area is too small for the number of bedrooms (Min 200 sqft/room)."

    # Constraint: Bathrooms shouldn't exceed bedrooms by more than 3
    if bath > (bedroom + 3):
        return False, "Unrealistic bathroom-to-bedroom ratio."

    # 3. Higher-Order Constraints
    if property_type.lower() == "flat" and area > 10000:
        return False, "A flat exceeding 10,000 sqft is statistically invalid for this region."

    return True, "Success"

if __name__ == "__main__":
    load_saved_artifacts()
    # get_location_names("house", "hyderabad")
    # print("location:", get_location_names("house", "hyderabad"))
    print(get_estimated_price(2178.000,4,6,"house","b-17","islamabad"))
    print(get_estimated_price(2178,6,4,"house","islamabad","b-17"))


