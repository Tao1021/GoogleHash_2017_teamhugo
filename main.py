# FILENAME = "examples/me_at_the_zoo.in"
FILENAME = "examples/kittens.in"
#FILENAME = "examples/simple.in"
# FILENAME = "examples/trending_today.in"
# FILENAME = "examples/videos_worth_spreading.in"

def cacheUsed(cacheSet):
    total = 0
    for vidNum in cacheSet:
        total =  videosSizes[vidNum] + total

    return total

class EndPoint:
    def __init__(self, endPointDataCenterLink, numCaches) :
        self._endPointDataCenterLink = endPointDataCenterLink
        self._numCaches = numCaches
        self._cacheLinks = []
        self._requests = []
        
    def __str__(self):
        s = "\tData center = " + str(self._endPointDataCenterLink) + ", numCaches = " + str(self._numCaches) + "\n"
        s = s + "\tCaches: " 
        for (cacheNum, delay) in self._cacheLinks:
            s = s + str(cacheNum) + ":" +  str(delay) + ", "
        s = s + "\n"

        s = s + "\tRequests: " 
        for (vidNum, numReq) in self._requests :
            s = s + "Vid " + str(vidNum) + ":" +  str(numReq) + ", "
        s = s + "\n"
        s = s + "\tTotal Traffic to DC: " + str(self.totalTrafficFromDC()) + "\n"
        
        return s

    def addCacheLink(self, cacheNum, delay):
        self._cacheLinks.append((cacheNum, delay))

    def addRequest(self, videoNum, num):
        self._requests.append((videoNum, num))
        
    def pruneBigVideos(self):
        vidsToDel = []
        for (vidNum, numReqs) in self._requests :
            if (videosSizes[vidNum] > cacheSize):
                vidsToDel.append((vidNum, numReqs))
            # now delete vidsToDelete
        
        self._requests  = [x for x in self._requests  if x not in vidsToDel]

    def totalTrafficFromDC(self):
        total = 0
        for (vidNum, numReq) in self._requests :
            total = total + (numReq * self._endPointDataCenterLink)
        return total
    
    def sortCachesBySpeed(self):
        self._cacheLinks.sort(key=lambda cacheNumDelay: cacheNumDelay[1], reverse=False)

    def sortRequestsByFreq(self):
        self._requests.sort(key=lambda videoNumFreq: videoNumFreq[1], reverse=True)

    def placeVidsInCaches(self):
        for (vidNum, numReq) in self._requests :
            # a cachelink is (cacheNum, delay)
            for cacheLink  in self._cacheLinks:
                cacheNum = cacheLink[0]
                cacheSet = cacheVideoDetails[cacheNum]
                freeSpace = cacheSize - cacheUsed(cacheSet)
                
                if (vidNum in cacheSet):
                    break;
                else :
                    if (freeSpace >= videosSizes[vidNum]):
                        cacheSet.add(vidNum)
                        break
                    
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

# Cache Structure
cacheVideoDetails = [set() for _ in range(numCaches)]

# Step 1
for ep in endPoints:
    ep.pruneBigVideos()


# Step 2

endPoints.sort(key=lambda ep: ep.totalTrafficFromDC(), reverse=True)

# Step 3
for ep in endPoints:
    ep.sortCachesBySpeed()
    
# Step 4
for ep in endPoints:
    ep.sortRequestsByFreq()
    
# step 5
for ep in endPoints:
    ep.placeVidsInCaches()

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



print("Caches")
for cache in cacheVideoDetails:
    print(cache)
    
# print to file!
file = open(FILENAME + ".out", "w") 


n = 0
for cacheIndex in range(len(cacheVideoDetails)):
    if (len(cacheVideoDetails[cacheIndex]) > 0):
        n = n + 1

file.write(str(n) + "\n")

for cacheIndex in range(len(cacheVideoDetails)):    
    
    cache = cacheVideoDetails[cacheIndex]
    
    if (len(cache) > 0) :
        file.write(str(cacheIndex) + " ")
        for vidNum in cache:        
            file.write(str(vidNum) + " ")

        file.write("\n")
file.close() 
