from arcgis.gis import GIS
from pathlib import Path
import arcgis
import os

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
        if item.type in ['Feature Service', 'Map Service', 'CSV Collection']:
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

class arcgis_downloads:
    username = 'praveenmp'
    password = 'Kee0Phah'
    gis = GIS("https://www.arcgis.com", username, password)
    user = gis.users.get(username=username)

    def download_file(self, feature_title, sublayer, filetype):
        arc = arcgis_listings()
        feature_id = arc.get_feature_id(feature_title)
        root_dir = os.getcwd()
        downloads_path = os.path.join(root_dir, "downloads")
        o_items = self.gis.content.search(query=f'id: "{feature_id}"')
        for item in o_items:
            stitle = item.title
            result = item.export(f'{item.title}', filetype)
            result.download(save_path=downloads_path)
        return stitle
