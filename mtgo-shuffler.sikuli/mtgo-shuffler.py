import pickle
import time
import guide
import java.awt.Toolkit

REGION_CARDS = Region(219,681,649,51)
REGION_RIGHT_CLICK = Region(284,28,305,246)
REGION_CONCEDE_GAME2 = Region(529,448,109,37)
REGION_OK = Region(583,449,113,35)
REGION_SUBMIT = Region(357,29,73,32)
REGION_YES_NO = Region(8,375,105,38)
REGION_CONCEDE_MATCH2 = Region(534,449,101,30)
REGION_NEW_GAME = Region(684,0,117,30)
REGION_SELECT_DECK = Region(583,369,114,14)
REGION_NEW_GAME_OPTIONS = Region(360,183,563,394)
REGION_NEW_GAME_OPTIONS_OK = Region(591,526,98,16)

PATTERN_FOREST = Pattern("1309403746146.png").similar(0.90)
PATTERN_MOUNTAIN = Pattern("1309403798497.png").similar(0.90)
PATTERN_CONCEDE_GAME1 = Pattern("1309404343655.png").similar(0.95)
PATTERN_CONCEDE_GAME2 = Pattern("CDNCEDEGAME.png").similar(0.95)
PATTERN_OK = Pattern("113.png").similar(0.95)
PATTERN_SUBMIT = Pattern("Lil1III.png").similar(0.95)
PATTERN_YES_NO = Pattern("NDflif.png").similar(0.95)
PATTERN_CONCEDE_MATCH1 = "1309443165553.png"
PATTERN_CONCEDE_MATCH2 = "1309443262881.png"
PATTERN_NEW_GAME = "1309443466101.png"
PATTERN_NEW_GAME_OPTIONS = "1309443556970.png"
PATTERN_CORRECT_DECK = Pattern("1309443688027.png").similar(0.90)

PATH_BASE = r"C:\Users\Andrew\Documents\My Dropbox\src\MTGO shuffler\\"
WAIT_TIME = 30	# seconds

def beep(times=1):	
	for x in range(times):
		java.awt.Toolkit.getDefaultToolkit().beep()
		time.sleep(0.3)

def log(message, log="log.txt"):
	with open(PATH_BASE + log, "a+") as logFile:
		for file in [sys.stdout, logFile]:
			file.write(message)

def findAllLands(totalHands):
	forests = []
	mountains = []
	
	if REGION_CARDS.exists(PATTERN_FOREST):
		forests = list(REGION_CARDS.findAll(PATTERN_FOREST))

	if REGION_CARDS.exists(PATTERN_MOUNTAIN):
		mountains = list(REGION_CARDS.findAll(PATTERN_MOUNTAIN))

	lands = forests + mountains


	"""
	for land in lands:
		guide.rectangle(land)

	guide.text(Region(500,551,72,23), str(totalHands))

	guide.show(1)
	"""


	
	return len(lands)

def startMTGO():	
	PATTERN_MTGO2 = "1309445185772.png"
	PATTERN_MAXIMIZE = Pattern("1309445217736.png").similar(0.95)
	PATTERN_FREE_TRIAL = "1309445250255.png"
	REGION_PLAY = Region(66,160,120,64)
	PATTERN_PLAY = "1309445874954.png"
	REGION_PLAY_STRUCTURE = Region(605,294,64,23)
	PATTERN_SOLITAIRE = Pattern("1309445377671.png").similar(0.90)
	REGION_MATCH_STRUCTURE = Region(592,323,87,12)
	PATTERN_BEST_OF = Pattern("1309445743921.png").similar(0.90)
	REGION_DECK = Region(585,371,101,12)
	PATTERN_ALLOW_WATCHERS = "1309447788927.png"
	REGION_CASUAL_GAMES = Region(6,21,138,31)
	PATTERN_CASUAL_GAMES_ZERO = Pattern("1309555276543.png").similar(0.98)
	
	click(Pattern("1309481763452.png").similar(0.91))

	wait(PATTERN_MTGO2, WAIT_TIME * 2)
	click(PATTERN_MAXIMIZE)
	time.sleep(1)
	click(PATTERN_FREE_TRIAL)

	REGION_PLAY.wait(PATTERN_PLAY, WAIT_TIME)
	click(REGION_PLAY)

	wait(PATTERN_NEW_GAME_OPTIONS, WAIT_TIME)

	click(REGION_PLAY_STRUCTURE)
	time.sleep(0.5)
	wait(PATTERN_SOLITAIRE)
	click(PATTERN_SOLITAIRE)
	
	time.sleep(0.5)
	click(REGION_MATCH_STRUCTURE)
	time.sleep(0.5)
	wait(PATTERN_BEST_OF)
	click(PATTERN_BEST_OF)

	# Wait for the list of games to load so the deck is responsive.
	REGION_CASUAL_GAMES.waitVanish(PATTERN_CASUAL_GAMES_ZERO, 60)
	beep(1)
	time.sleep(3)
	click(REGION_DECK)
	time.sleep(1)
	if not exists(PATTERN_CORRECT_DECK):
		click(REGION_DECK)

	time.sleep(1)
	wait(PATTERN_CORRECT_DECK)
	click(PATTERN_CORRECT_DECK)
	
	time.sleep(1)
	if exists(PATTERN_ALLOW_WATCHERS):
		click(PATTERN_ALLOW_WATCHERS)

	time.sleep(0.5)
	click(REGION_NEW_GAME_OPTIONS_OK)

	REGION_YES_NO.wait(PATTERN_YES_NO, WAIT_TIME * 4)

def quitMTGO():
	beep(3)
	
	time.sleep(3)
	closeApp("Magic Online")
	time.sleep(5)

def nextGame():
	beep()
	
	time.sleep(0.5)
	rightClick(REGION_RIGHT_CLICK)
	
	REGION_RIGHT_CLICK.wait(PATTERN_CONCEDE_GAME1, WAIT_TIME)
	REGION_RIGHT_CLICK.click(PATTERN_CONCEDE_GAME1)

	REGION_CONCEDE_GAME2.wait(PATTERN_CONCEDE_GAME2, WAIT_TIME)
	click(REGION_CONCEDE_GAME2)

	REGION_OK.wait(PATTERN_OK, WAIT_TIME)
	time.sleep(0.5)
	click(REGION_OK)

	REGION_SUBMIT.wait(PATTERN_SUBMIT, WAIT_TIME)
	time.sleep(0.5)
	click(REGION_SUBMIT)

	REGION_YES_NO.wait(PATTERN_YES_NO, WAIT_TIME)

def captureHand(results, totalHands):
	numLands = findAllLands(totalHands)
	results[numLands] = results.setdefault(numLands, 0) + 1

def logResults(results):
	totalHands = sum(results.itervalues())
	percentageResults = results.copy()
	resultsStr = ""
	for numLands in sorted(results.keys()):
		percentageResults[numLands] = "%.2f%%" % ((100.0 * results[numLands]) / totalHands,)
		resultsStr += "%d lands: %s (%d)\n" % (numLands, percentageResults[numLands], results[numLands])

	message = str(results)
	message += "\nTotal hands: %d\n%s" % (totalHands, resultsStr)
	message += "-\n"

	log(message, log="results.txt")

def pickleResults(results, filename):
	with open(PATH_BASE + filename, "wb") as file:
		pickle.dump((results, sum(results.itervalues())), file)

def unpickleResults(filename):
	try:
		file = open(PATH_BASE + filename, "rb")
		results, totalHands = pickle.load(file)
		file.close()

		assert sum(results.itervalues()) == totalHands
		
		return results, totalHands
	except IOError:
		file = open(PATH_BASE + filename, "wb")
		file.write("")
		file.close()

		return {}, 0

def main():
	Settings.MoveMouseDelay = 0.4
	Settings.WaitScanRate = 10

	pickleFilename = "results.pickle"
	
	results, totalHands = unpickleResults(pickleFilename)

	log("Unpickled (%s, %d)\n" % (str(results), totalHands))

	while True:
		try:
			if not REGION_YES_NO.exists(PATTERN_YES_NO):
				startMTGO()
					
			totalHands = sum(results.itervalues())
			
			captureHand(results, totalHands)
			nextGame()
	
			if totalHands % 5 == 4:
				logResults(results)

			if totalHands % 50 == 0:
				quitMTGO()
				startMTGO()
				
		except FindFailed:
			beep(6)
			quitMTGO()

		except KeyboardInterrupt, ThreadDeath:
			raise

		except:
			beep(15)
			raise

		finally:
			pickleResults(results, pickleFilename)

if __name__ == '__main__':
	main()