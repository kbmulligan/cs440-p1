# p1.py - find the maximum clique in a graph
# by K. Brett Mulligan
# 27 Aug 2014
# CSU CS440
# Dr. Asa Ben-Hur
##############################################



def initPoints (filename):

    pf = open(filename, 'r')
    if pf == None:
        print "Error: Could not open points file."
    else:
        for line in pf:
            if line != "":
                pData = line
                listOfValues = pData.split(" ")

                #######
    pf.close()