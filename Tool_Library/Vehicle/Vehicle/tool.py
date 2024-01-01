import requests


def get_response(url: str, **kargs):
    try:
        response = requests.get(url=url, params=kargs)
    except:
        return {"error": "connection error."}

    try:
        observation = response.json()
    except:
        observation = response.text

    return observation


def decode_vin(vin: str, modelyear: int = 2023):
    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}'
    return get_response(url, modelyear=modelyear, format='json')


def decode_WMI(wmi: str):
    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeWMI/{wmi}'
    return get_response(url, format='json')


def get_WMI(manufacturer: str | int, vehicle_type: str | int = None):
    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetWMIsForManufacturer/{manufacturer}'
    if vehicle_type == None:
        return get_response(url, format='json')
    else:
        return get_response(url, format='json', vehicleType=vehicle_type)


def get_manufacturer_details(manufacturer: str | int):
    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetManufacturerDetails/{manufacturer}'
    return get_response(url, format='json')


def get_makes(manufacturer: str | int = None, vehicle_type: str | int = None, year: int = None):
    if manufacturer is not None:
        if year is not None:
            url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForManufacturerAndYear/{manufacturer}'
            return get_response(url, year=year, format='json')
        else:
            url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForManufacturer/{manufacturer}'
            return get_response(url, format='json')
    elif vehicle_type is not None:
        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/{vehicle_type}'
        return get_response(url, format='json')
    else:
        return {"error": "name and vehicle_type can not both be None."}


def get_vehicle_types(name: str = None, id: int = None):
    if name is not None:
        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleTypesForMake/{name}'
        return get_response(url, format='json')
    elif id is not None:
        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleTypesForMakeId/{id}'
        return get_response(url, format='json')


def get_models(id: int = None, name: str = None, year: int = None, vehicle_type: str | int = None):
    if id is not None:
        if (year is None) and (vehicle_type is None):
            url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/{id}'
        else:
            url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/{id}'
            if year is not None:
                url = url + f'/modelyear/{year}'
            if vehicle_type is not None:
                url = url + f'/vehicletype/{vehicle_type}'
        return get_response(url, format='json')
    elif name is not None:
        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeYear/make/{name}'
        if (year is None) and (vehicle_type is None):
            return {"error": "when name is not None, year and vehicle can not both be None."}
        if year is not None:
            url = url + f'/modelyear/{year}'
        if vehicle_type is not None:
            url = url + f'/vehicletype/{vehicle_type}'
        return get_response(url, format='json')


def get_vehicle_variables():
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleVariableList'
    return get_response(url, format='json')


def get_vehicle_variable_values(variable: str | int):
    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleVariableValuesList/{variable}'
    return get_response(url, format='json')


if __name__ == '__main__':
    # print(decode_vin('5UXWX7C5*BA'))
    # print(decode_WMI('1FD'))
    # print(get_WMI('hon'))
    # print(get_manufacturer_details('honda'))
    # print(get_makes(name='mer', year=2013))
    # print(get_makes(vehicle_type='car'))
    # print(get_makes())
    # print(get_vehicle_types(name='mercedes'))
    # print(get_vehicle_types(id=450))
    # print(get_models(name='honda', year=2015, vehicle_type='car'))
    # print(get_models(id=474, year=2015, vehicle_type='truck'))
    # print(get_vehicle_variables())
    # print(get_vehicle_variable_values('battery type'))
    pass
