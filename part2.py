"""CME 211 Final Project
   Part 2 Module
   Author: Casey Mills Davis
   Stanford University

   COMMAND LINE USAGE
   Usage:
   python    part2.py    u.data     similarities.txt      53       1294
                       <data file> <similarities file> <user ID> <movie ID>
   Returns the predicted rating of movie <movie ID> by user <user ID>.
   Prediction is based on data from two input files.
"""

from User import *
import part1
import sys
import time
import re

# Regular expression for quickly grabbing values from input file
idPat = re.compile(r'(\d+),')
pearsonPat = re.compile(r'(\d\.\d\d)')

def setPearsonsMan(numUsers, users, IDs, PCCs):
    """Adds similarity coefficients to users list

    Keyword arguments:
    numUsers
    users -- list of User objects
    IDs -- list of similar ID lists, must have length numUsers
    PCCs -- list of similarity coefficent lists, has 1-to-1 correspondence with IDs

    """
    for n in range(numUsers):
        for m in range(len(IDs[n])):
            users[n].addPearson(int(IDs[n][m]),float(PCCs[n][m]))
            

def setRatings(numUsers, users, ratings):
    """Updates ratings data stored in users list

    Keyword arguments:
    numUsers
    users -- list of User objects
    ratings -- list of line tokens form a u.data-like file

    """
    def updateUserData(userID, itemID, rating, users): users[userID-1].addRating(itemID, rating)
    for rating in ratings: updateUserData(int(rating[0]), int(rating[1]), int(rating[2]), users)

def part2Wrapper(dataFileName, simFileName):
    """Reads a u.data like file and a similarities file in the format
    used by module part1. Returns a list of User objects which reflect
    the two input files.

    Keyword arguments:
    dataFileName -- input file, like u.data
    simFileName -- similarities file, part1 module format

    """
    try:
        simFile = open(simFileName, 'r')
    except IOError:
        print 'Cannot open similarities file: ' + simFileName + '\n'
        sys.exit()

    try:
        uData = open(dataFileName, 'r')
    except IOError:
        print 'Cannot open user file: ' + dataFileName + '\n'
        sys.exit()

    simLines = simFile.readlines()
    IDs = map(idPat.findall, simLines)
    PCCs = map(pearsonPat.findall, simLines)
    users, numUsers, numMovies = part1.getUserData(uData)
    setPearsonsMan(numUsers, users, IDs, PCCs)
    simFile.close()
    uData.close()
    return users

def getPrediction(users, userID, movieID):
    """Returns predicted movie rating

    Keyword arguments:
    users -- list of User objects
    userID -- ID of user 
    movieID -- ID of movie 

    """
    try:
        simUsers = users[userID-1].getBestMatches()
    except Exception, e:
        print e
        print "Bad users list in getPrediction(~)."
        sys.exit()
    prediction = 0.0
    numSum = 0.0
    denSum = 0.000001
    prediction += users[userID-1].getAverage()
    simUsersThatRated = []
    for match in simUsers:
        simUser = users[match[0]-1]
        if movieID in simUser.getRatings():
            simUsersThatRated.append(match)
    for match in simUsersThatRated:
        simUser = users[match[0]-1]
        pearson = match[1]
        numSum += (simUser.getRating(movieID) - simUser.getAverage()) * pearson
        denSum += pearson
    prediction += numSum/denSum
    return prediction
            

# For testing
if __name__ == "__main__":
    startT = time.time()
    if (len(sys.argv) != 5):
        print "Usage:"
        print "   %s <data file> <similarities file> <user ID> <movie ID>" % sys.argv[0]
        sys.exit()

    # Collect input arguments
    try:
        datafilename = sys.argv[1]
        simfilename = sys.argv[2]
        userid = int(sys.argv[3])
        movieid = int(sys.argv[4])
    except Exception, e:
        print e
        print "Problem with command line arguments."
        print "Usage:"
        print "   %s <data file> <similarities file> <user ID> <movie ID>" % sys.argv[0]
        sys.exit()

    users = part2Wrapper(datafilename, simfilename)
    pred = getPrediction(users, userid, movieid)
    print "Predicted rating of movie " + str(movieid) + " by user " + str(userid) + ": " + '%1.2f' % (pred,)
    
    #print running time
    print 'Time required: %3.2f seconds' % ( time.time() - startT,)
