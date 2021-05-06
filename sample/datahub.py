# Standard library imports
import csv
import pathlib
import zipfile
import pickle
import datetime
import urllib


# Third party imports
import pandas

# Local application/library specific imports


class Database:
    """A database class for downloading and inventorying Stats Canada tables.

    Attributes:
        meta_data (dict): a dual leveled dict where meta_data is stored in
            the second level.
        alerts (bool): if True enables audible updates for downloads
            and updates.
    """

    def __init__(self, alerts=False):
        """Loads the meta_data dictionary from a pickle, else it creates it.
        Also sets audible update behavior for the object.

        Args:
            alerts (bool): Sets object behavior for audible updates
        """
        self.alerts = alerts
        try:
            self.meta_data = pickle.load(open("RawData/meta_data.p", "rb"))
        except FileNotFoundError:
            self.meta_data = dict()
            self.save()

    def _download_data(self, data_name):
        """Downloads the specified data table from Stats Canada.
        Used in both the .add_data and .update_data methods.

        Args:
            data_name: The data table meta-data identifier key.
        """
        dl_url = self.meta_data[data_name]['dl_url']
        dl_type = dl_url[dl_url.rfind('.'):]

        download = r'RawData/temp' + dl_type
        urllib.request.urlretrieve(dl_url, download)

        if dl_type == '.zip':
            with zipfile.ZipFile(download, 'r') as zip_ref:
                self.meta_data[data_name]['data_file'] = 'RawData/' + \
                                                         zip_ref.namelist()[0]
                self.meta_data[data_name]['meta_data'] = 'RawData/' + \
                                                         zip_ref.namelist()[1]
                zip_ref.extractall(r'RawData')

        else:
            raise TypeError('Download is not a .zip file.')

        with open('RawData/11100134_MetaData.csv', mode='r') as metafile:
            csv_file = csv.reader(metafile)
            result = []
            for row in list(csv_file)[0:2]:
                result.append(row)

        # Clean the headers of unusual characters.
        result[0] = [''.join(c for c in d if c not in 'ï»¿"') for d in
                     result[0]]

        # Update data dictionary to include meta data.
        self.meta_data[data_name].update(dict(zip(result[0], result[1])))

        file_path = pathlib.Path(download)
        self.meta_data[data_name]['updated'] = datetime.datetime.now()

        try:
            file_path.unlink()
        except OSError as e:
            print("Error: %s : %s" % (file_path, e.strerror))

    def load_data(self, data_name):

        """Loads the downloaded data table into a Pandas DataFrame.

        Args:
            data_name: the identifier of the data table in self.meta_data

        Returns:
            A pandas DataFrame of the data table.
        """
        return pandas.read_csv(self.meta_data[data_name]['data_file'])

    def save(self):
        """Saves self.meta_data to a pickle at RawData/meta_data.p """
        pickle.dump(self.meta_data, open("RawData/meta_data.p", "wb"))

    def add_data(self, data_name, dl_url):
        """Downloads, unzips, and adds a new data table to the self.meta_data

        :param data_name: The key for the data table in self.meta_data
        :param dl_url:
        :return:
        """
        # Adds the download url to the metadata,
        #   also deletes previous metadata if it exists
        self.meta_data[data_name] = {'dl_url': dl_url}

        self._download_data(data_name)

        self.save()

    def update_data(self, data_name):
        """Downloads, unzips, and updates self.meta_data for the specified data

        Args:
            data_name (str): The key for the data table in self.meta_data.
        """
        self._download_data(data_name)
        self.save()

    def filter_meta(self, attributes):
        """Filters self.meta_data and returns only the specified attributes.

        Args:
            attributes (list): The meta-data attributes to be displayed.

        Returns:
            A dual level dict of self.meta_data with only the specified
                meta-data attributes.
        """
        meta = {}
        for k in self.meta_data.keys():
            meta[k] = {}
            for sk, v in self.meta_data[k].items():
                if sk in attributes:
                    meta[k][sk] = v
        return meta
