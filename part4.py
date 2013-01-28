"""CME 211 Final Project
   Part 4 Module
   Author: Casey Mills Davis
   Stanford University

   COMMAND LINE USAGE
   Usage:
   python    part4.py    u.data     recommendations.txt
                       <data file> <recommendations file>
   Outputs the top three movie recommendations for all users to
   <recommendations file>.
"""

import part1
import part2
import sys
import math
import operator
import time
import re


def getTopRecommendations(users, numMovies):
    """Updates users by finding all their recommendations for movies
    they have not rated and also returns a list of the top 3 recommendations
    for each User. Users must already have their similarity coefficients
    calculated!

    Keyword arguments:
    users -- list of User objects
    numMovies

    """
    topRecs = []
    for user in users:
        rated = user.getRatings()
        for movie in range(1, numMovies + 1):
            if movie not in rated:
                p = part2.getPrediction(users, user.getNumber(), movie)
                user.addPrediction(movie, p)
        topRecs.append(user.getPredictions()[:3])
    return topRecs

def writeRecommendations(users, outfile):
    """Writes the top 3 recommendations of each User to outfile.

    Keyword arguments:
    users -- list of User objects
    outfile

    """
    for user in users:
        outfile.write('%03d  ' % (user.number,))
        for match in user.getPredictions()[:3]:
            pRating = float(match[1])
            if pRating < 1.0: pRating = 1.0
            if pRating > 5.0: pRating = 5.0
            outfile.write('(%3d, %1.2f)  ' % (int(match[0]), pRating,) )
        outfile.write('\n')

def part4Wrapper(dataFileName, recFileName):
    """Combines functionality from part4 module. Takes a data file
    such as u.data and outputs the top three recommendations to
    recFileName.

    Keyword arguments:
    dataFileName -- file name, format is u.data
    recFileName -- writes here

    """
    try:
        userData = open(dataFileName, 'r')
        recFile = open(recFileName, 'w')
    except IOError:
        print 'Cannot use given filenames: ' + str(dataFileName) + ' ' + str(recFileName)
        sys.exit()
    users, numUsers, numMovies = part1.getUserData(userData)
    part1.setPearsons(numUsers, users)
    topRecs = getTopRecommendations(users, numMovies)
    writeRecommendations(users, recFile)
    userData.close()
    recFile.close()

# For testing
if __name__ == "__main__":
    startT = time.time()
    if (len(sys.argv) != 3):
        print "Usage:"
        print "   %s <data file> <recommendations file>" % sys.argv[0]
        sys.exit()

     # Collect input arguments
    try:
        datafilename = sys.argv[1]
        recfilename = sys.argv[2]
    except Exception, e:
        print e
        print "Problem with command line arguments."
        print "Usage:"
        print "   %s <data file> <recommendations file>" % sys.argv[0]
        sys.exit()

    part4Wrapper(datafilename, recfilename)

    #print running time
    print 'Time required: %3.2f' % ( time.time() - startT,)
