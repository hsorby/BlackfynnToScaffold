import logging
from json import loads, dumps
from os.path import splitext
from sanic import Sanic
from sanic.response import json, html, text, redirect
from packageIdToScaffold import BFWorker
from discover import Discover
import requests

app = Sanic()

logger = logging.getLogger(__name__)
bfWorker = BFWorker(None)
discover = Discover()
        
@app.route('/getInfo')
async def getInfo(request):
    id = 0
    for k, values in request.args.items():
      v = values[0]
      if k == 'id':
          id = v
      data = bfWorker.getCollectionAndMetaFromPackageId(id)
      if data != None:
        myResponse = {'collectionId': data[0], 'fileName':data[1]}
        return json(myResponse)
    return json({'error': 'error with the provided ID '}, status=400)

@app.route('/scaffold/<colId:string>/<fileName:string>')
async def scaffold(request, colId, fileName):
    awsURL = bfWorker.getURLFromCollectionIdAndFileName(colId, splitext(fileName)[0])
    try:
      resp = requests.get(awsURL)
      return json({'awsURL':resp.url})
    except Exception as e:
      return json({'error': e}, status=400)

@app.route('/blackfynn/<datasetName:string>/<fileName:string>')
async def bf_get_file(request, datasetName, fileName):
    try:
        ds = bfWorker.bf.get_dataset(datasetName)
        file_url = ds.get_items_by_name('Derivatives')[0].get_items_by_name(fileName)[0].files[0].url
        return json({'awsURL': file_url}, status=200)
    except IndexError as e:
        return json({'error': f'No files found in dataset: {datasetName} of name: {fileName}'}, status=400)

@app.route('/discover/<datasetName:string>/<fileName:string>')
async def get_discover_file(request, datasetName, fileName):
    try:
        url = discover.get_file(datasetName, fileName)
        return json({'awsURL': url}, status=200)
    except IndexError as e:
        return json({'error': f'No files found in dataset: {datasetName} of name: {fileName}'}, status=400)

def main():
    app.run(host='0.0.0.0', port=6765)





if __name__ == '__main__':
    main()
