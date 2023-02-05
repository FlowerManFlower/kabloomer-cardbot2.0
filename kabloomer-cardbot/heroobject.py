import re as regex




class heroObject(object):
	record = []
	name = ""
	abbreviation = ""
	heroclasses = []
	herosupers = {}
	flavor = ""
	classSelector = [
	'<:ClassGuardian:903886862739968000>',
	'<:ClassKabloom:903886598242975774>',
	'<:ClassMegagrow:903887465079795722>',
	'<:ClassSmarty:903887385828392970>',
	'<:ClassSolar:903886649195376660>',
	'<:ClassBeastly:903886562914357258>',
	'<:ClassBrainy:903887622110343218>',
	'<:ClassCrazy:903887769749815326>',
	'<:ClassHearty:903887665399758889>',
	'<:ClassSneaky:903887707707670568>']
	abilitySwitcher = {
	'Strength' : "<:Strength:903874899007930380>",
	'Health' : "<:Health:903874645663576134>",
	'Sun' : "<:Sun:903881342276759593>",
	'Brain' : "<:Brain1:903885991931154472>"
	}

	def __init__(self, record):
		self.resetCard()
		self.record = record

		for row in record:
			self.createName(row[0])
			self.createAbbreviation(row[1])
			self.createClasses(row[2])
			self.createherosupers(row[3:6])
			self.createFlavor(row[6])

	def resetCard(self):
		self.record = []
		self.name = ""
		self.abbreviation = ""
		self.heroclasses = []
		self.herosupers = {}
		self.flavor = ""

	def createName(self, recordName):
		self.name = recordName

	def createAbbreviation(self, recordAbbreviation):
		self.abbreviation = recordAbbreviation
	
	def createClasses(self, recordClass):
		if(recordClass in self.heroclasses):
			return
		else:
			self.heroclasses.append(recordClass)

	def createherosupers(self, recordSuper):
		print(recordSuper)
		try:
			if(recordSuper[1] in self.herosupers[recordSuper[0]]):
				pass
			else:
				self.herosupers[recordSuper[0]].append(recordSuper[1])
			if(recordSuper[2] in self.herosupers[recordSuper[0]]):
				pass
			else:
				self.herosupers[recordSuper[0]].append(recordSuper[2])
		except:
			self.herosupers[recordSuper[0]] = [recordSuper[1]]


	def createFlavor(self, recordFlavor):
		self.flavor = recordFlavor
		
	def getName(self):
		return(self.name)

	def getAbbreviation(self):
		return(self.abbreviation)

	def getClasses(self):
		returnString = ""
		for c in self.heroclasses:
			returnString += c
		return(returnString)

	def getherosupers(self):
		returnString = ""
		for herosuper in self.herosupers:
			tempsuper = []
			tempsuperString = ""
			abilityText = ""
			tempsuper.append("**" + herosuper + "** ")
			for superclass in self.herosupers[herosuper]:
				print(superclass)
				if(superclass in self.classSelector):
					tempsuper.append(superclass)
				else:
					abilityText = superclass
					holdText = regex.search('[0123456789 ]\:(.+?)\:', abilityText)
					while(holdText is not None):
						replacement = self.abilitySwitcher.get(holdText.group(1))
						abilityText = abilityText[0:holdText.start()+1] + replacement + abilityText[holdText.end():]
						holdText = regex.search('[0123456789 ]\:(.+?)\:', abilityText)

			tempsuper.append("\n" + abilityText + "\n")
			for entry in tempsuper:
				tempsuperString += entry
			if(tempsuper[2] in self.classSelector):
				returnString = tempsuperString + returnString
			else:
				returnString += tempsuperString

		return(returnString)

	def getFlavor(self):
		return(self.flavor)

	def information(self):
		return( self.getName() + " (" + self.getAbbreviation() + ") | " + self.getClasses() + "\n\n" +
				"Supers:\n" + self.getherosupers() +
				"*" + self.getFlavor() + "*")


	def __str__(self):
		return self.name


"""
hero_name0, abbreviation1,
cardclass.cardclass2,
card.name3,
hero_flavor4
"""
