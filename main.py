FILENAME = "examples/me_at_the_zoo.in"

class EndPoint:
    def __init__(self, endPointDataCenterLink, numCaches) :
        self._endPointDataCenterLink = endPointDataCenterLink
        self._numCaches = numCaches
        self._cacheLinks = {}
        self._requests = {}
        
    def __str__(self):
        s = "\tData center = " + str(self._endPointDataCenterLink) + ", numCaches = " + str(self._numCaches) + "\n"
        s = s + "\tCaches: " 
        for cache in self._cacheLinks.keys() :
            s = s + str(cache) + ":" +  str(self._cacheLinks.get(cache)) + ", "
        s = s + "\n"

        s = s + "\tRequests: " 
        for vidNum in self._requests.keys() :
            s = s + "Vid " + str(vidNum) + ":" +  str(self._requests.get(vidNum)) + ", "
        s = s + "\n"
        
        return s

    def addCacheLink(self, cacheNum, delay):
        self._cacheLinks[cacheNum] = delay

    def addRequest(self, videoNum, num):
        self._requests[videoNum] = num
        
infile = open(FILENAME)

# Parse basic data
generalSpecLine = infile.readline()
generalSpecLineParts = generalSpecLine.split()

numVideos = int(generalSpecLineParts[0])
numEndPoints = int(generalSpecLineParts[1])
numRequestDescriptions = int(generalSpecLineParts[2])
numCaches = int(generalSpecLineParts[3])
cacheSize = int(generalSpecLineParts[4])

# parse video sizes
videoSizesLine = infile.readline()
videoSizesLineParts = videoSizesLine.split(); 
videosSizes = []
for vs in videoSizesLineParts:
    videosSizes.append(int(vs))

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

# parse requests
for i in range(numRequestDescriptions):
    requestLine = infile.readline()
    requestLineParts = requestLine.split()
    vidNum = int(requestLineParts[0])
    epNum = int(requestLineParts[1])
    num = int(requestLineParts[2])
    
    endPoints[epNum].addRequest(vidNum, num)

infile.close()

print("Number of Videos:", numVideos)
print("Number of End Points:", numEndPoints)
print("Number of Request Descriptions:", numRequestDescriptions)
print("Number of caches:", numCaches)
print("Caches Size:", cacheSize)

print("Video Sizes:", videosSizes)

print("End Points:")
for i in range(len(endPoints)) :
    print("End Point " + str(i) + ":")
    print(str(endPoints[i]))
