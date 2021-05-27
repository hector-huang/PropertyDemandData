import json

def getLocationList(locDict, index):
    newList = [location["geometry"]["coordinates"][index] for location in locDict]
    return newList

def initCoordinatesDict(minLat, maxLat, minLon, maxLon):
    coordinatesDict = {}
    latInterval = (maxLat - minLat)/100
    lonInterval = (maxLon - minLon)/50
    for i in range(101):
        for j in range(51):
            coordinate = (minLat + latInterval*i, minLon + lonInterval*j)
            coordinatesDict[coordinate] = 0
    return coordinatesDict

def getStandardizeCoordinate(prop, minLat, maxLat, minLon, maxLon):
    latInterval = (maxLat - minLat)/100
    lonInterval = (maxLon - minLon)/50
    xindex = int((prop["geometry"]["coordinates"][0] - minLat)/latInterval)
    yindex = int((prop["geometry"]["coordinates"][1] - minLon)/lonInterval)
    total_views = int(prop["properties"]["total_views"])
    return {"coordinate": (minLat + xindex*latInterval, minLon + yindex*lonInterval), "total_views": total_views}

with open('listings.geojson') as json_file:
    geoDict = json.load(json_file)
    locationDict = geoDict["features"]
    latList = getLocationList(locationDict, 0)
    lonList = getLocationList(locationDict, 1)
    
    minLat = min(latList)
    maxLat = max(latList)
    minLon = min(lonList)
    maxLon = max(lonList)

    coordinatesDict = initCoordinatesDict(minLat, maxLat, minLon, maxLon)

    for location in locationDict:
        coordinate = getStandardizeCoordinate(location, minLat, maxLat, minLon, maxLon)
        coordinatesDict[coordinate["coordinate"]] += coordinate["total_views"]

    filteredDict = dict()
    for (key, value) in coordinatesDict.items():
        if value != 0:
            filteredDict[key] = value
    
    features = [ {"type":"Feature","properties":{"id":str(int(k[0]*1000+k[1]*100)), "total_views":v, "geometry":{"type":"Point","coordinates":[k[0],k[1],0]}}} for (k,v) in filteredDict.items() ]
    finalDict = {"type":"FeatureCollection","crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}},"features":features}
    jsonString = json.dumps(finalDict)
    print(jsonString)