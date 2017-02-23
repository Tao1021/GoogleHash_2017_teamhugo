FILENAME = "examples/me_at_the_zoo.in"

infile = open(FILENAME)

# Parse basic data
generalSpecLine = infile.readline()
generalSpecLineParts = generalSpecLine.split()

numVideos = generalSpecLineParts[0]
numEndPoints = generalSpecLineParts[1]
numRequestDescriptions = generalSpecLineParts[2]
numCaches = generalSpecLineParts[3]

# parse video sizes
videoSizesLine = infile.readline()
videosSizes = map(int, videoSizesLine.split())



infile.close()

print("Number of Videos:", numVideos)
print("Number of End Points:", numEndPoints)
print("Number of Request Descriptions:", numRequestDescriptions)
print("Number of caches:", numCaches)

print("Video Sizes:", videosSizes)
