
import blackfynn

#pkg = bf.get('N:package:99d63b9e-c902-4e0a-9694-3ea31caa6708')
#print(pkg.sources)
#pkg = bf.get('N:package:c31f905d-34b8-40b0-9e6d-244f039bede6')
#print(pkg.sources)
#collection=pkg.parent

class BFWorker(object):
  def __init__(self, id):
    self.bf = Blackfynn(id)


  def getCollectionAndMetaFromPackageId(self, packageId):
    pkg = self.bf.get(packageId)
    if type(pkg) is blackfynn.DataPackage:
      colId = pkg.parent
      col = self.bf.get(colId)
      items = col.items
      for item in items:
        if packageId == item.id:
          return [colId, item.name]
    return None

  def getURLFromCollectionIdAndFileName(self, collectionId, fileName):
    col = self.bf.get(collectionId)
    if type(col) is blackfynn.Collection:
      items = col.items
      print(items)
      for item in items:
        if fileName == item.name:
          pkg = item
          try:
            bfFile = pkg.files[0]
            url = bfFile.url
            return url
          except:
            return None
    return None
