import os


def createAssetFoldersIfNotExisted(asset, base_path):
    '''This function first creates a folder in the name of asset. Then it
    creates two csv_data and txt_data subfolders inside it.'''
    pair_path = base_path + asset
    list_of_pairs = os.listdir(base_path)
    if asset not in list_of_pairs:
        os.mkdir(os.path.join(base_path, pair_path))
        os.mkdir(os.path.join(base_path, pair_path + "\\csv_data\\"))
        os.mkdir(os.path.join(base_path, pair_path + "\\txt_data\\"))
