from arcgis import *

try:
    username = 'praveenmp'
    password = 'Kee0Phah'
    gis = GIS("https://www.arcgis.com", username, password)
    url = r'https://www.arcgis.com/sharing/generateToken?username=' + username + r'&password=' + password + r'&referer=https://www.arcgis.com&f=json&expiration=600'
    print("Successfully Connected")
except:
    print("Failed")