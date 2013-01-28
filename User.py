"""CME 211 Final Project
   User Module
   Author: Casey Mills Davis
   Stanford University

   Contains the definition of the User object.
"""

import operator

class User(object):
 
    def __init__(self, number):
        self.number = number
        self.average = 0
        self.numRatings = 0
        self.ratings = {}
        self.matches = {}
        self.bestMatch = []
        self.predictions = {}
        self.bestRecs = []
        
    def getNumber(self):
        return self.number
 
    def getAverage(self):
        return self.average

    def addRating(self, itemID, rating):
        self.numRatings += 1
        self.ratings[itemID] = rating
        self.average = float(sum(self.ratings.values()))/self.numRatings

    def getRating(self, itemID):
        try:
            return self.ratings[itemID]
        except:
            print "User " + str(self.number) + " has no rating for movie: " + str(itemID)

    def getRatings(self):
        return self.ratings

    def getBestMatches(self):
        self.bestMatch = sorted(self.matches.iteritems(), key=operator.itemgetter(1), reverse=True)
        return self.bestMatch

    def addPearson(self, userID, pearson):
        self.matches[userID] = pearson

    def addPrediction(self, itemID, predictedRating):
        self.predictions[itemID] = predictedRating

    def getPrediction(self, itemID):
        try:
            return self.predictions[itemID]
        except:
            print "User " + str(self.number) + "has no prediction for movie: " + str(itemID)

    def getPredictions(self):
        self.bestRecs = sorted(self.predictions.iteritems(), key=operator.itemgetter(1), reverse=True)
        return self.bestRecs
 
    def __str__(self):
        return "%d's average rating is %s" % (self.number, self.average)
