from pickle import *

PATH_BASE = r"C:\Users\Andrew\Documents\My Dropbox\src\MTGO shuffler\\"
FILENAME = r"results.pickle"
PATH = PATH_BASE + FILENAME

def unpickle():
	with open(PATH, "rb") as file:
		results = load(file)

	return results

def pickle(results):
	totalHands = sum(results.itervalues())
	with open(PATH, "wb") as file:
		dump((results, totalHands), file)
