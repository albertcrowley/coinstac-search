from math import isnan

def update_meta_data_structure (result, key, val):
    if key not in result:
        result[key] = {
            "numeric" : False,
            "has_nan" : "NA",
            "min" : "NaN",
            "max" : "NaN",
            "enumeration" : []
        }
    try:
        if val == "nan":
            result[key]["has_nan"] = "Yes"
        else:
            f = float(val)

            if result[key]["min"] == "NaN":
                result[key]["min"] = f
            if result[key]["max"] == "NaN":
                result[key]["max"] = f

            result[key]["min"] = min(result[key]["min"], f)
            result[key]["max"] = max(result[key]["max"], f)
            result[key]["numeric"] = True
    except:
        result[key]["enumeration"].append(val)



