from math import isnan

def update_meta_data_structure (result, key, val):
    if key not in result:
        result[key] = {
            "numeric" : False,
            "has_nan" : False,
            "min" : float('nan'),
            "max" : float('nan'),
            "enumeration" : []
        }
    try:
        if val == "nan":
            result[key]["has_nan"] = True
        else:
            f = float(val)

            if isnan(result[key]["min"]):
                result[key]["min"] = f
            if isnan(result[key]["max"]):
                result[key]["max"] = f

            result[key]["min"] = min(result[key]["min"], f)
            result[key]["max"] = max(result[key]["max"], f)
            result[key]["numeric"] = True
    except:
        result[key]["enumeration"].append(val)


