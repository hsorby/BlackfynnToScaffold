import requests
from awsClient import AWSClient
import os

class Discover:
    def __init__(self):
        self.baseURL = 'https://api.blackfynn.io/discover/'
        self.awsClient = AWSClient()

    def get_file(self, datasetName, fileName):
        datasetID = self.get_discover_id_from_name(datasetName)
        resp = requests.get('https://api.blackfynn.io/discover/search/files',
                            {'query': fileName, 'datasetId': datasetID})
        s3_uri = resp.json()['files'][0]['uri']
        url = self.awsClient.get_signed_url(s3_uri)
        return url

    def get_discover_id_from_name_sd(self, datasetName):
        # This url requires authentication so is currently unusable :(
        resp = requests.get(self.baseURL + '/search/dataset', {'query': datasetName})

    def get_discover_id_from_name(self, datasetName):
        resp = requests.get(self.baseURL + '/datasets', {'limit': 1000})
        datasets = resp.json()['datasets']
        d_id = [d['id'] for d in datasets if datasetName in d['name']][0]
        return d_id

    def parseScaffoldMetaItem(self, item, uri):
      path, filename = os.path.split(uri)
      if "URL" in item:
        newpath = os.path.join(path, item["URL"])
        url = self.awsClient.get_signed_url(newpath)
        item["URL"] = url
      if "GlyphGeometriesURL" in item:
        newpath = os.path.join(path, item["GlyphGeometriesURL"])
        url = self.awsClient.get_signed_url(newpath)
        item["GlyphGeometriesURL"] = url

    def createPresignedScaffold(self, url, uri):
        resp = requests.get(url)
        data = resp.json()
        for item in data:
          self.parseScaffoldMetaItem(item, uri)
        return data

    def get_scaffold_from_package_id(self, id):
        resp = requests.get(self.baseURL + '/packages/' + id + '/files', {'limit': 100})
        fileinfo = resp.json()['files'][0]
        uri = fileinfo['uri']
        url = self.awsClient.get_signed_url(uri)
        return self.createPresignedScaffold(url, uri)

