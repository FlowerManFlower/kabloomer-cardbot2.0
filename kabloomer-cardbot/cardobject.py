import re as regex


class cardObject(object):
	record = []
	name = ""
	cardclass = []
	tribes = []
	cardType = ""
	cost = 0
	costType = ""
	strength = 0
	strengthModifier = "<:Strength:903874899007930380>"
	health = 0
	healthModifier = "<:Health:903874645663576134>"
	traits = []
	ability = "<:Icon_TriggeredEffectGlow:1069004406491730030>"
	flavor = ""
	cardSet = ""
	rarity = "<:badgenew:1008530927892312116>"
	abilitySwitcher = {
	'Strength' : "<:Strength:903874899007930380>",
	'Health' : "<:Health:903874645663576134>",
	'Sun' : "<:Sun:903881342276759593>",
	'Brain' : "<:Brain1:903885991931154472>"
	}

	traitSwitcher = {
	'Amphibious' : '<:Amphibious:1068990328129990817>・',
	'Anti-Hero 2': '<:AntiHero:903886114983661578>・',
	'Anti-Hero 3': '<:AntiHero:903886114983661578>・',
	'Anti-Hero 4': '<:AntiHero:903886114983661578>・',
	'Anti-Hero 5': '<:AntiHero:903886114983661578>・',
	'Armored 1': '<:Armored:903884767748046858>・',
	'Armored 2': '<:Armored:903884767748046858>・',
	'Bullseye': '<:Bullseye:903884708310581290>・',
	'Deadly': '<:Deadly:903885745259946055>・',
	'Double Strike': '<:DoubleStrike:903885923215884358>・',
	'Hunt': '<:Hunt:1068991767644475412>・',
	'Frenzy': '<:Frenzy:903886051267997737>・',
	'Gravestone': '<:Gravestone_Icon:971870289178816573>・',
	'Overshoot 2': '<:overshoot:903885866286579762>・',
	'Overshoot 3': '<:overshoot:903885866286579762>・',
	'Splash Damage 1': '<:SplashDamage:1068985896898142299>・',
	'Splash Damage 3': '<:SplashDamage:1068985896898142299>・',
	'Splash Damage 6': '<:SplashDamage:1068985896898142299>・',
	'Strikethrough': '<:Strikethrough:903885692067782666>・',
	'Team-Up': '<:TeamUp:1069000377246175282>・',
	'Untrickable': '<:Untrickable:903885798892503110>・'
	}


	def __init__(self, record):
		self.resetCard()
		self.record = record

		for row in record:
			self.createName(row[0])
			self.createClasses(row[1])
			self.createTribes(row[2])
			self.createType(row[3])
			self.createCost(row[4])
			self.createCostType(row[5])
			self.createStrength(row[6])
			self.createStrengthModifier(row[7])
			self.createHealth(row[8])
			self.createHealthModifier(row[9])
			self.createTraits(row[10])
			self.createAbility(row[11])
			self.createFlavor(row[12])
			self.createCardSet(row[13])
			self.createRarity(row[14])

	def resetCard(self):
		self.record = []
		self.name = ""
		self.cardclass = []
		self.tribes = []
		self.cardType = ""
		self.cost = 0
		self.costType = ""
		self.strength = 0
		self.strengthModifier = "<:Strength:903874899007930380>"
		self.health = 0
		self.healthModifier = "<:Health:903874645663576134>"
		self.traits = []
		self.ability = "<:Icon_TriggeredEffectGlow:1069004406491730030>"
		self.flavor = ""
		self.cardSet = ""
		self.rarity = "<:badgenew:1008530927892312116>"


	def createName(self, recordName):
		self.name = recordName
	
	def createClasses(self, recordClass):
		if(recordClass is None):
			pass
		if(recordClass in self.cardclass):
			return
		else:
			self.cardclass.append(recordClass)

	def createTribes(self, recordTribe):
		if(recordTribe is None):
			return
		if(recordTribe in self.tribes):
			return
		else:
			self.tribes.append(recordTribe)

	def createType(self, recordType):
		self.cardType = recordType

	def createCost(self, costRecord):
		self.cost = costRecord
	
	def createCostType(self, recordCostType):
		if(len(self.costType) < 1):
			self.costType = recordCostType
			return
		elif(self.costType == recordCostType):
			return
		else:
			self.costType = "Special"

	def createStrength(self, recordStrength):
		self.strength = recordStrength
	
	def createStrengthModifier(self, recordStrengthModifier):
		if(recordStrengthModifier is None):
			return
		if(self.strengthModifier == recordStrengthModifier):
			return
		self.strengthModifier = recordStrengthModifier if self.strengthModifier == "<:Strength:903874899007930380>" else "<:MultiAbility:999559472911487017>"

	
	def createHealth(self, recordHealth):
		self.health = recordHealth if self.health != recordHealth else self.health
	
	def createHealthModifier(self, recordHealthModifier):
		if(recordHealthModifier is None):
			return
		if(self.healthModifier == recordHealthModifier):
			return
		self.healthModifier = recordHealthModifier if self.healthModifier == "<:Health:903874645663576134>" else "<:MultiAbility:999559472911487017>"
		
	def createTraits(self, recordTrait):
		if(recordTrait is None):
			return
		if(recordTrait == 'HealthStrength'):
			return
		if(recordTrait in self.traits):
			return
		else:
			self.traits.append(recordTrait)
	
	def createAbility(self, recordAbility):
		self.ability = recordAbility

	def createFlavor(self, recordFlavor):
		self.flavor = recordFlavor
	
	def createCardSet(self, recordCardSet):
		if(recordCardSet is None):
			return
		self.cardSet = recordCardSet
	
	def createRarity(self, recordRarity):
		self.rarity = recordRarity
	
	def getName(self):
		return(self.name)

	def getClasses(self):
		returnString = ""
		for c in self.cardclass:
			returnString += c
		return(returnString)

	def getTribes(self):
		returnString = "- "
		for tribe in self.tribes:
			returnString += tribe + " "
		return(returnString)

	def getType(self):
		return(self.cardType + " -")

	def getCost(self):
		return(self.cost)

	def getCostType(self):
		return(self.CostType)

	def getStrength(self):
		return(self.strength)

	def getStrengthModifier(self):
		return(self.strengthModifier)

	def getHealth(self):
		return(self.health)

	def getHealthModifier(self):
		return(self.healthModifier)

	def getStats(self):
		if(self.health != 0):
			if(self.strength != 0):
				return("%s%s  %s%s %s%s" % (self.cost, self.costType, self.strength, self.strengthModifier, self.health, self.healthModifier))
			else:
				return("%s%s  %s%s" % (self.cost, self.costType, self.health, self.healthModifier))
		else:
			return("%s%s" % (self.cost, self.costType))

	def getTraits(self):
		returnString = ""
		for trait in self.traits:
			returnString += self.traitSwitcher.get(trait) + "__" + trait + "__, "
		else:
			returnString = returnString[0:-2]
		returnString += "\n" if len(returnString) > 0 else ""
		return(returnString)

	def getAbility(self):
		abilityText = self.ability + "\n" if len(self.ability) > 0 else ""
		holdText = regex.search('[\+0123456789 ]\:(.+?)\:', abilityText)
		returnString = ""
		while(holdText is not None):
			replacement = self.abilitySwitcher.get(holdText.group(1))
			abilityText = abilityText[0:holdText.start()+1] + replacement + abilityText[holdText.end():]
			holdText = regex.search('[0123456789 ]\:(.+?)\:', abilityText)

		holdText = abilityText.split(" ")
		for word in holdText:
			if word in self.traitSwitcher:
				returnString += "__" + word + "__ "
			else:
				returnString += word + " "
		return(returnString)

	def getFlavor(self):
		return(self.flavor)

	def getSet(self):
		return(self.cardSet + " - " if len(self.cardSet) > 0 else "")

	def getRarity(self):
		return(self.rarity)

	def information(self):
		return( self.getName() + " | " + self.getClasses() + "\n" +
				self.getTribes() + self.getType() + "\n" +
				self.getStats() + "\n" +
				self.getTraits() +
				self.getAbility() + 
				"*" + self.getFlavor() + "*\n" +
				"**\<\< " + (self.getSet() + self.getRarity()).upper() + " \>\>**")



	def __str__(self):
		return self.name


"""


<:Strength:903874899007930380> 
<:Health:903874645663576134> 
<:Sun:903881342276759593> 
<:Brain1:903885991931154472> 
<:ClassGuardian:903886862739968000> 
<:ClassKabloom:903886598242975774> 
<:ClassMegagrow:903887465079795722> 
<:ClassSmarty:903887385828392970> 
<:ClassSolar:903886649195376660> 
<:ClassBeastly:903886562914357258> 
<:ClassBrainy:903887622110343218> 
<:ClassCrazy:903887769749815326> 
<:ClassHearty:903887665399758889> 
<:ClassSneaky:903887707707670568> 
<:AntiHero:903886114983661578> 
<:Armored:903884767748046858> 
<:Bullseye:903884708310581290> 
<:Deadly:903885745259946055> 
<:DoubleStrike:903885923215884358> 
<:Frenzy:903886051267997737> 
<:Healthattack:991110916038996088> 
<:overshoot:903885866286579762> 
<:MultiAbility:999559472911487017> 
<:Strikethrough:903885692067782666> 
<:Untrickable:903885798892503110>

0name ・ 1cardclass.cardclass,
2tribe.tribe 3cardtype.cardtype,
4cost 5side.side, 6strength, 7trait.strengthmodifier, 8health, 9trait.healthmodifier,
10trait.trait,
11ability,
12flavor,
13cardset.cardset 14rarity.rarity
"""
