from arcgis.gis import GIS

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

    def get_sublayers():
        pass