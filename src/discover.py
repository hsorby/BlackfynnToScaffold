import requests
from awsClient import AWSClient

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