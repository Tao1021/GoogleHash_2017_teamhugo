FILENAME = "examples/me_at_the_zoo.in"

class EndPoint:
    def __init__(self, endPointDataCenterLink, numCaches) :
        self._endPointDataCenterLink = endPointDataCenterLink
        self._numCaches = numCaches
        self._cacheLinks = {}
        
    def __str__(self):
        s = "End Point [data center = " + str(self._endPointDataCenterLink) + ", numCaches = " + str(self._numCaches) + "]"
        for cache in self._cacheLinks.keys() :
            s = "\t\t" + str(cache) + " : " +  str(self._cacheLinks.get(cache))
        return s

    def addCacheLink(self, cacheNum, delay):
        self._cacheLinks[cacheNum] = delay

infile = open(FILENAME)

# Parse basic data
generalSpecLine = infile.readline()
generalSpecLineParts = generalSpecLine.split()

numVideos = int(generalSpecLineParts[0])
numEndPoints = int(generalSpecLineParts[1])
numRequestDescriptions = int(generalSpecLineParts[2])
numCaches = int(generalSpecLineParts[3])

# parse video sizes
videoSizesLine = infile.readline()
videosSizes = map(int, videoSizesLine.split())

# Read end point data

endPoints = []

for endPointIndex in range(numEndPoints):
    endPointSpecLine = infile.readline()
    endPointSpecLineParts =endPointSpecLine.split()
    endPointDataCenterLink = int(endPointSpecLineParts[0])
    endPointNumCache = int(endPointSpecLineParts[1])
    
    endPoint = EndPoint(endPointDataCenterLink, endPointNumCache)
    endPoints.append(endPoint)
    
    for epCacheNum in range(endPointNumCache) :
        epCacheSpec = infile.readline()
        epCacheSpecParts = epCacheSpec.split()
        x = int(epCacheSpecParts[0])
        delay = int(epCacheSpecParts[1])
        endPoint.addCacheLink(x, delay)

infile.close()

print("Number of Videos:", numVideos)
print("Number of End Points:", numEndPoints)
print("Number of Request Descriptions:", numRequestDescriptions)
print("Number of caches:", numCaches)

print("Video Sizes:", videosSizes)

print("End Points:")
for i in range(len(endPoints)) :
    print("End Point " + str(i) + ":")
    print("\t", str(endPoints[i]))
