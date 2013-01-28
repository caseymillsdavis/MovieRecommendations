"""CME 211 Final Project
   Part 3 Module
   Author: Casey Mills Davis
   Stanford University

   COMMAND LINE USAGE
   Usage:
   python    part3.py    u1.base       u1.test
                        <base file>  <test file>
   Prints the RMS error of predictions made from the training file
   compared to the test file.
"""

import part1
import part2
import sys
import time
import math

def RMSerror(trainingFileName, testFileName):
    """Returns the RMS error of predictions made from the training file
    compared to the test file.

    Keyword arguments:
    trainingFileName -- partial set of user data
    testFileName -- remainder of user data

    """
    try:
        trainingFile = open(trainingFileName, 'r')
        testFile = open(testFileName, 'r')
    except IOError:
        print 'Cannot open training/test files.'
        sys.exit()

    users, numUsers, numMovies = part1.getUserData(trainingFile)
    part1.setPearsons(numUsers, users)
    rmse = 0.0
    testRatings = map(part1.dataPattern.findall, testFile.readlines())
    n = len(testRatings)
    for rating in testRatings:
        userID = int(rating[0])
        movieID = int(rating[1])
        rating = float(rating[2])
        rmse += pow(rating - part2.getPrediction(users, userID, movieID), 2)
    return math.sqrt(rmse/n)
            

# For testing
if __name__ == "__main__":
    startT = time.time()
    if (len(sys.argv) != 3):
        print "Usage:"
        print "   %s <base file> <test file>" % sys.argv[0]
        sys.exit()

    # Collect input arguments
    try:
        basefilename    = sys.argv[1]
        testfilename = sys.argv[2]
    except Exception, e:
        print e
        print "Problem with command line arguments."
        print "Usage:"
        print "   %s <base file> <test file>" % sys.argv[0]
        sys.exit()

    err = RMSerror(basefilename, testfilename)
    print "RMS error: %2.4f" % (err,)

    #print running time
    print 'Time required: %3.2f' % ( time.time() - startT,)
