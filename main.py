FILENAME = "examples/me_at_the_zoo.in"

infile = open(FILENAME)

generalSpecLine = infile.readline()

infile.close()

print(generalSpecLine)