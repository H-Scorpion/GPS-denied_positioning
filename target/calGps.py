import pymap3d as pm

def calGps(obj):
    """ It take a ubx object. After doing some computation, 
    it'll return a new gps object with calculated location

    Args:
        obj (ubx object): ubx object with uncorrected gps data

    Returns:
        ubx object: uncorrected gps data after calculation
    """    
    if obj._id == 7:
        pass
        # dict_keys(['__module__', 'iTOW', 'year', 'month', 'day',
        #  'hour', 'min', 'sec', 'valid', 'tAcc', 'nano', 'fixType',
        #  'flags', 'flags2', 'numSV', 'lon', 'lat', 'height', 'hMSL',
        #  'hAcc', 'vAcc', 'velN', 'velE', 'velD', 'gSpeed', 'headMot',
        #  'sAcc', 'headAcc', 'pDOP', 'flags3', 'reserved1', 'reserved1x',
        #  'headVeh', 'magDec', 'magAcc', '__dict__', '__weakref__', '__doc__'])

        # obj.lon=obj.lon+5000000  # adding 1 for 10**-7degree
        # obj.lat=obj.lat-5*10**7
        # print(obj)
        
    return obj

def absGps(enu,refloc):
    """Calculate absolute GPS location in lon/lat
    
    Args:
        enu (tuple): (e, n, u)
        refloc (tuple): (lon, lat, height)

    Returns:
        tuple: (lon, lat, height)
    """    

    absLoc = pm.geodetic2enu(10**6,10**6, 4, 23, 121, 5)

    # absLoc = (0, 0, 0)  
    return absLoc

if __name__ == '__main__':
    enu = (3,4,5)
    refloc = (121, 25, 3)
    # absLoc = absGps(enu, refloc)
    absLoc = pm.enu2geodetic(10**6,10**6, 4, 1, 1, 5, deg= True)
    print(absLoc)

    