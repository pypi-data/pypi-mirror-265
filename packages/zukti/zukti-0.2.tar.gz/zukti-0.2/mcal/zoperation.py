# -------------- For EyeTest ---------------------------->>>>>>>>

MAYOPIA_SNELLEN_FRACTION = {
    "6/6":0.7275,
    "6/7.5": 0.91,
    "6/9.6": 1.164,
    "6/12": 1.455,
    "6/13.5": 1.64,
    "6/15": 1.82,
    "6/16.5": 2.01,
    "6/17.7": 2.15,
    "6/19.5": 2.365,
    "6/21.45": 2.6,
    "6/24": 2.91,
    "6/25.56": 3.1,
    "6/27": 3.27,
    "6/30": 3.63,
    "6/37.5": 4.54,
    "6/48": 5.82,
    "6/60": 7.27,
    "6/90":10.9125,
    "6/120":  14.55,
}
    
HYPEROPIA_SNELLEN_FRACTION = {
    "6/6"   :0.86,
    "7.5"   :0.86,
    "9.6"   :1.05,
    "12"    :1.28,
    "13.5"  :1.40,
    "15.24" :1.58,
    "18.28" :1.63,
    "21.336":1.87,
    "24.384":1.98,
    "27.432":2.33,
    "30.48" :2.68,
    "33.5"  :3.50,
}

HYPEROPIA_SNELLEN_DATA = {
    "6/6"   :0.00,  
    "7.5"   :0.25,  
    "9.6"   :0.50,
    "12"    :1.00,   
    "13.5"  :1.25, 
    "15.24" :1.50, 
    "18.28" :2.10, 
    "21.336":2.50, 
    "24.384":3.00, 
    "27.432":3.50, 
    "30.48" :4.00, 
    "33.5"  :4.50, 
}


MYOPIA_SNELLEN_DATA = {
    "6/6": 0,
    "6/7.5": 0.25,
    "6/9.6": 0.6,
    "6/12": 1,
    "6/13.5": 1.25,
    "6/15": 1.5,
    "6/16.5": 1.75,
    "6/17.7": 2.0,
    "6/19.5": 2.25,
    "6/21.45": 2.57,
    "6/24": 3,
    "6/25.56": 3.26,
    "6/27": 3.5,
    "6/30": 4,
    "6/37.5": 5.24,
    "6/48": 7,
    "6/60": 9,
    "6/90": 14,
    "6/120": 19,
    }


AGE_POWER_MAPPING = {
    (39, 41): 1.00,
    (40, 46): 1.25,
    (45, 51): 1.50,
    (50, 56): 1.75,
    (55, 61): 2.00,
    (60, 66): 2.25,
    (65, 120): 2.50,
}

CYL_POWER_MAPPING = {
    (-1, 4): 0,
    (-1, 5): 0.25,
    (4, 8): 0.5,
    (7, 11): 0.75,
    (10, 14): 1,
    (13, 17): 1.25,
    (16, 19): 1.5,
    (18, 21): 1.75,
    (19, 22): 2.0,
    (20, 23): 2.25,
    (21, 24): 2.5,
    (22, 25): 2.75,
    (23, 26): 3.0,
    (24, 27): 3.5,
    (26, 28): 4.0,
    (27, 29): 4.5,
    (28, 30): 5.0,
}


# ----------------- For Lenso Meter---------------------

LENSO_CYL_POWER_MAPPING= {
    (0,0.2):     0,             
    (0.2,0.32):  0.25,               
    (0.33,0.4):  0.5,                
    (0.4,0.46):  0.75,               
    (0.46,0.49): 1.0,                
    (0.49,0.55): 1.25,               
    (0.55,0.57): 1.5,                
    (0.57,0.59): 1.75,               
    (0.59,0.61): 2.0,                
    (0.61,0.63): 2.25,               
    (0.63,0.66): 2.5,                
    (0.66,0.69): 2.75,               
    (0.69,0.72): 3.0,                
    (0.72,0.75): 3.5,                
    (0.75,0.78): 4.0,                
    (0.79,0.81): 4.5,                
    (0.81,0.83): 5.0,                
    (0.83,0.84): 5.5,                
    (0.84,0.86): 6.0,
}

SPH_POWER_MAPPING = {
    (1.1, 1): 0,
    (1, 0.92):  0.25,
    (0.92, 0.90): 0.5,
    (0.90, 0.88): 0.75,
    (0.88, 0.86): 1,
    (0.86, 0.84): 1.25,
    (0.84, 0.82): 1.5,
    (0.82, 0.80): 1.75,
    (0.80, 0.77): 2,
    (0.77, 0.75): 2.25,
    (0.75, 0.73): 2.5,
    (0.73, 0.71): 2.75,
    (0.71, 0.70): 3,
    (0.70, 0.68): 3.25,
    (0.68, 0.66): 3.5,
    (0.66, 0.65): 3.75,
    (0.65, 0.64): 4,
    (0.64, 0.60): 4.5,
    (0.60, 0.58): 5,
    (0.58, 0.56): 5.5,
    (0.56, 0.54): 6,
    (0.54, 0.50): 6.5,
    (0.50, 0.48): 7,
    (0.48, 0.46): 7.5,
    (0.46, 0.44): 8,
    (0.44, 0.42): 8.5,
    (0.42, 0.40): 9,
    (0.40, 0.38): 9.5,
    (0.38, 0.36): 10,
    (0.36, 0.34): 10.5,
    (0.34, 0.32): 11,
    (0.32, 0.26): 12
}

"""
Get cyl power, function
"""
def get_eye_cyl_power(cyl_param):
    eye_cyl_power = 0
    if cyl_param is not None:
        for eye_cyl_range, power in CYL_POWER_MAPPING.items():
            if eye_cyl_range[0] < float(cyl_param) < eye_cyl_range[1]:
                eye_cyl_power = power
                break
    return eye_cyl_power
 
"""
Get Age power, function
"""
def get_age_power(age_power_param):
    age_power = 0
    for age_range, power in AGE_POWER_MAPPING.items():
        if age_range[0] < int(age_power_param) < age_range[1]:
            age_power = power
            break
    return age_power    
 
"""
Get Report Data For Myopia and Hyperopia Test, function
"""
def get_report_data_for_myopia_and_hyperopia(test, snellen_fraction, age_power_param):
    if test == "myopia":
        target_value = snellen_fraction
        data = MYOPIA_SNELLEN_DATA
    elif test == "hyperopia":
        target_value = snellen_fraction
        data = HYPEROPIA_SNELLEN_DATA
    SPH_value = data.get(target_value, 0)
 
    eye_cyl_power = get_eye_cyl_power(age_power_param)
    return SPH_value, eye_cyl_power


def map_cyl_power_function(eccentricity):
    """Map cyl to corresponding power based on predefined ranges."""
    for cyl_range, power in LENSO_CYL_POWER_MAPPING.items():
        if cyl_range[0] < eccentricity < cyl_range[1]:
            return power
    return 0


def calculate_cyl(eccentricity):
    """Calculate sph power based on minor axis and major axis."""
    result = 0.0
    try:
        if eccentricity >= 0.235:
            result = map_cyl_power_function(eccentricity)
        else:
            result = map_cyl_power_function(eccentricity)
        return result
    except Exception as e:
        return result


def map_sph_power_function(sph):
    """Map sph to corresponding power based on predefined ranges."""
    for sph_range, power_value in SPH_POWER_MAPPING.items():
        if sph_range[0] >= sph > sph_range[1]:
            return power_value
    return 0


def calculate_sph(height_50,height_25):
    """Calculate sph power based on height_50 and height_25."""
    result = 0.0
    try:
        status, result = "+", 0
        ratio = round((height_25 / height_50), 2)
        if height_50 > height_25:
            result = map_sph_power_function(ratio)
            status = "-"
        elif height_50 < height_25:
            result = ((ratio - 1) * 4) / ratio
            status =  "+"
        return result, status

    except Exception as e:
        status = None
        return result, status
