import logging
from json import loads, dumps
from os.path import splitext
from sanic import Sanic
from sanic.response import json, html, text, redirect
from packageIdToScaffold import BFWorker
import requests

app = Sanic()

logger = logging.getLogger(__name__)
bfWorker = BFWorker(None)
        
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
      return json(resp.content)
    except:
      return json({'error': 'error with the url '}, status=400)

def main():
    app.run(host='0.0.0.0', port=6765)


if __name__ == '__main__':
    main()
