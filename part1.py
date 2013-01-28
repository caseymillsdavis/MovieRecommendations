"""CME 211 Final Project
   Part 1 Module
   Author: Casey Mills Davis
   Stanford University

   COMMAND LINE USAGE
   Usage:
   python    part1.py    u.data    similarities.txt      3
                       <data file>  <output file>   <sim number>
   Using <data file> computes similarity coefficients and writes the
   <sim number> most similar users IDs and Pearson Correlation Coeffs
   to <output file>.
"""

from User import *
import sys
import math
import operator
import time
import re

# Regular expression for quickly grabbing values from input file
dataPattern = re.compile('\d+')

# Constants - may be optimized later
MIN_ITEMS_IN_COMMON = 3
WEIGHTING_THRESHOLD = 20
MIN_SIM_THRESHOLD = 0.4


def findMaxIDs(ratings):
    """Returns maxUserID and maxMovieID

    Keyword arguments:
    ratings -- list of parsed lines from u.data-like file

    """
    maxUserID = 1
    maxMovieID = 1
    for rating in ratings:
        if int(rating[0]) > maxUserID: maxUserID = int(rating[0])
        if int(rating[1]) > maxMovieID: maxMovieID = int(rating[1])
    return maxUserID, maxMovieID


def getUserData(userdatafile):
    """Returns a list of User objects with user-numbers 1 to numUsers
    Also returns numUsers and numMovies

    Keyword arguments:
    userdatafile -- u.data-like file

    """
    ratings = map(dataPattern.findall, userdatafile.readlines())
    numUsers, numMovies = findMaxIDs(ratings)
    users = [User(x) for x in range(1, numUsers + 1)]
    def updateUserData(userID, itemID, rating, users): users[userID-1].addRating(itemID, rating)
    for rating in ratings: updateUserData(int(rating[0]), int(rating[1]), int(rating[2]), users)
    return users, numUsers, numMovies


def setPearsons(numUsers, users):
    """Update users list by calculating and adding similarity
    coefficients for each user.

    Keyword arguments:
    numUsers
    users -- list of User objects

    """
    for m in range(numUsers):
        for n in range(m+1, numUsers):
            movieIntersection = set(users[m].ratings.keys()) & set(users[n].ratings.keys())
            numCommon = len(movieIntersection)
            if numCommon >= MIN_ITEMS_IN_COMMON:
                weightScale = 1.0
                if numCommon < WEIGHTING_THRESHOLD: weightScale = numCommon/WEIGHTING_THRESHOLD
                aSquare = 0.0
                bSquare = 0.0
                abCross = 0.0
                for movie in movieIntersection:
                    rsuba = users[m].ratings[movie] - users[m].average
                    rsubb = users[n].ratings[movie] - users[n].average
                    abCross += rsuba * rsubb
                    aSquare += rsuba**2
                    bSquare += rsubb**2
                pearson =  float(abCross) / (float(math.sqrt(aSquare*bSquare)) + .000001)
                pearson = weightScale * pearson
                if pearson >= MIN_SIM_THRESHOLD:
                    users[m].addPearson(users[n].number, pearson)
                    users[n].addPearson(users[m].number, pearson)


def writePearsons(users, numToWrite, outfile):
    """Writes highest similarity coefficients to file

    Keyword arguments:
    users -- list of User objects
    numToWrite -- max number of similar users to list for each user
    outfile -- file for writing similarity coefficients

    """
    for user in users:
        outfile.write('%03d  ' % (int(user.number),))
        for match in user.getBestMatches()[:numToWrite]:
            outfile.write('(%3d, %.2f)  ' % (int(match[0]), match[1],) )
        outfile.write('\n')

def part1Wrapper(dataFileName, simFileName, numSims):
    """Writes similarity coefficents to file
    Combines raw functions from part1.py module

    Keyword arguments:
    dataFileName -- input file, like u.data
    simFileName -- similarities file for write
    numSims -- number of similar users to output

    """
    try:
        userData = open(dataFileName, 'r')
        simFile = open(simFileName, 'w')
    except IOError:
        print 'Cannot use given filenames: ' + dataFileName + ' ' + simFileName
        sys.exit()

    #1. Generate users
    users, numUsers, numMovies = getUserData(userData)
    #2. Calculate similarity coefficients
    setPearsons(numUsers, users)
    #3. Output similarity coefficients to file
    writePearsons(users, numSims, simFile)

    userData.close()
    simFile.close()


if __name__ == "__main__":
    startT = time.time()
    if (len(sys.argv) != 4):
        print "Usage:"
        print "   %s <data file> <output file> <num of sim users>" % sys.argv[0]
        sys.exit()

    # Collect input arguments
    try:
        datafilename    = sys.argv[1]
        outfilename = sys.argv[2]
        numsims  = int(sys.argv[3])
    except Exception, e:
        print e
        print "Problem with command line arguments."
        print "Usage:"
        print "   %s <data file> <output file> <num of sim users>" % sys.argv[0]
        sys.exit()

    part1Wrapper(datafilename, outfilename, numsims)

    #print running time
    print 'Time required: %3.2f seconds' % ( time.time() - startT,)
