from arcgis.gis import GIS
from pathlib import Path
import arcgis
import os
import shutil
import time
import geopandas as gpd




class arcgis_listings:

    username = 'praveenmp'
    password = 'Kee0Phah'
    gis = GIS("https://www.arcgis.com", username, password)
    user = gis.users.get(username=username)

    def get_folders(self):
        folder_list = []
        folders = self.gis.users.me.folders
        for i in folders:
            folder_list.append(i)
        return folder_list

    def get_layers(self, folder_name):
        folder = self.user.items(folder = folder_name)
        result = []
        for item in folder:
            result.append(item.title)
        return result

    def get_sublayers_names(self, feature_id):
        item = self.gis.content.get(feature_id)
        sublayer_list = []
        if item.type in ['Feature Service', 'Map Service', 'CSV Collection', 'Shapefile', 'Microsoft Excel']:
            for layer in item.layers:
                sublayer_list.append(layer.properties.name)
            return(sublayer_list)
        elif item.type in ['Web Map']:
            web_map = arcgis.mapping.WebMap(item)
            layers = web_map.layers
            for sublayers in layers:
                sublayer_list.append(sublayers.title)
            return(sublayer_list)
        else:
            print("______________________________")
            print("ERROR")
            print("Item type is: ",item.type)
            print("______________________________")

    def get_feature_id(self, feature_title):
        search_result = self.gis.content.search(query=f'title: "{feature_title}"')
        return search_result[0].id
    
    def get_feature_type(self, layer_name):
        layer = self.get_feature_id(layer_name)
        layer_obj = self.gis.content.get(layer)
        return layer_obj.type


class arcgis_downloads:
    username = 'praveenmp'
    password = 'Kee0Phah'
    gis = GIS("https://www.arcgis.com", username, password)
    user = gis.users.get(username=username)

    def download_file(self, feature_title, sublayer, filetype):
        arc = arcgis_listings()
        feature_id = arc.get_feature_id(feature_title)
        root_dir = os.getcwd()
        downloads_path = os.path.join(root_dir, "main/static/downloads")
        items = self.gis.content.get(feature_id)


        if items.type in ['Feature Service', 'Map Service', 'CSV Collection', 'Shapefile', 'GeoPackage']:
            o_items = self.gis.content.search(query=f'id: "{feature_id}"')
            for item in o_items:
                stitle = item.title
                result = item.export(f'{item.title}', filetype)
                result.download(save_path=downloads_path)
                if result.type in ['CSV Collection', 'Shapefile', 'GeoPackage']:
                    result.delete()
                    time.sleep(5)
            return stitle
        
        elif items.type in ['Web Map']:
            web_map = arcgis.mapping.WebMap(items)
            layers = web_map.layers
            for sublayers in layers:
                try:
                    map_layer = self.gis.content.get(sublayers.itemId)
                    result = map_layer.export(f'{map_layer.title}', filetype)
                    result.download(save_path=downloads_path)
                    if result.type in ['CSV Collection', 'Shapefile', 'GeoPackage']:
                        result.delete()
                        time.sleep(5)
                except Exception as e:
                    print(f"Error: {e}")
                    continue

    def clear_files(self):
        root_dir = os.getcwd()
        path = os.path.join(root_dir, "main/static/downloads")
        try:
            shutil.rmtree(path)
        except OSError as e:
            print("Error: %s : %s" % (path, e.strerror))

