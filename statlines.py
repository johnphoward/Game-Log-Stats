# statlines.py

from copy import copy, deepcopy

##### Important globals #####

# An empty template for each statline
statlineTemplate = {
	'team': 'unassigned',
	'opponent': 'unassigned',
	'home': 'unassigned',
	'time': 0,
	'ptsfor': 0,
	'ptsagainst': 0,
	'fgmfor': 0,
	'fgmagainst': 0,
	'fgafor': 0,
	'fgaagainst': 0,
	'3pmfor': 0,
	'3pmagainst': 0,
	'3pafor': 0,
	'3paagainst': 0,
	'ftmfor': 0,
	'ftmagainst': 0,
	'ftafor': 0,
	'ftaagainst': 0,
	'orbfor': 0,
	'orbagainst': 0,
	'drbfor': 0,
	'drbagainst': 0,
	'trbfor': 0,
	'trbagainst': 0,
	'astfor': 0,
	'astagainst': 0,
	'pffor': 0,
	'pfagainst': 0,
	'stlfor': 0,
	'stlagainst': 0,
	'tofor': 0,
	'toagainst': 0,
	'blkfor': 0,
	'blkagainst': 0,
	'margins': []
}

# Dictionary of all indices in each NBA.com play tuple
playIndex = {
	'GAME_ID': 0,
	'EVENTNUM': 1,
	'EVENTMSGTYPE': 2,
	'EVENTMSGACTIONTYPE': 3,
	'PERIOD': 4,
	'WCTIMESTRING': 5,
	'PCTIMESTRING': 6,
	'HOMEDESCRIPTION': 7,
	'NEUTRALDESCRIPTION': 8,
	'VISITORDESCRIPTION': 9,
	'SCORE': 10,
	'SCOREMARGIN': 11,
	'PERSON1TYPE': 12,
	'PLAYER1_ID': 13,
	'PLAYER1_NAME': 14,
	'PLAYER1_TEAM_ID': 15,
	'PLAYER1_TEAM_CITY': 16,
	'PLAYER1_TEAM_NICKNAME': 17,
	'PLAYER1_TEAM_ABBREVIATION': 18,
	'PERSON2TYPE': 19,
	'PLAYER2_ID': 20,
	'PLAYER2_NAME': 21,
	'PLAYER2_TEAM_ID': 22,
	'PLAYER2_TEAM_CITY': 23,
	'PLAYER2_TEAM_NICKNAME': 24,
	'PLAYER2_TEAM_ABBREVIATION': 25,
	'PERSON3TYPE': 26,
	'PLAYER3_ID': 27,
	'PLAYER3_NAME': 28,
	'PLAYER3_TEAM_ID': 29,
	'PLAYER3_TEAM_CITY': 30,
	'PLAYER3_TEAM_NICKNAME': 31,
	'PLAYER3_TEAM_ABBREVIATION': 32,
}

##### Statline creation #####

def parsePlayListForStats(plays, thisTeam, thatTeam, homeTeam, period = 1, time = '12:00'):
	"""
	Given a list of plays and a team abbreviation to evaluate for, 
	returns a dictionary object containing all relevant stats
	"""

	statline = deepcopy(statlineTemplate)
	statline['team'] = thisTeam
	statline['home'] = homeTeam
	statline['opponent'] = thatTeam
	awayTeam = thatTeam if thisTeam == homeTeam else thisTeam

	lastPlayTeam = ''

	for play in plays:
		playType = play[playIndex['EVENTMSGTYPE']]

		teamFor = ''
		description = ''
		secondary = None
		if not play[playIndex['HOMEDESCRIPTION']] is None:
			teamFor = homeTeam
			description = play[playIndex['HOMEDESCRIPTION']]
			if 'BLOCK' in description:
				if not play[playIndex['VISITORDESCRIPTION']] is None:
					teamFor = awayTeam
					secondary = description
					description = play[playIndex['VISITORDESCRIPTION']]
			else:
				secondary = play[playIndex['VISITORDESCRIPTION']]
		elif not play[playIndex['VISITORDESCRIPTION']] is None:
			teamFor = awayTeam
			description = play[playIndex['VISITORDESCRIPTION']]
		else:
			teamFor = None
			description = play[playIndex['NEUTRALDESCRIPTION']]

		if playType == 1:
			""" Made Shot """
			if teamFor == thisTeam:
				statline['fgafor'] += 1
				statline['fgmfor'] += 1
				statline['ptsfor'] += 2
				if '3PT' in description:
					statline['3pafor'] += 1
					statline['3pmfor'] += 1
					statline['ptsfor'] += 1
				if 'AST' in description:
					statline['astfor'] += 1
			else:
				statline['fgaagainst'] += 1
				statline['fgmagainst'] += 1
				statline['ptsagainst'] += 2
				if '3PT' in description:
					statline['3paagainst'] += 1
					statline['3pmagainst'] += 1
					statline['ptsagainst'] += 1
				if 'AST' in description:
					statline['astagainst'] += 1
		elif playType == 2:
			""" Missed Shot """
			# print play
			if teamFor == thisTeam:
				statline['fgafor'] += 1
				if '3PT' in description:
					statline['3pafor'] += 1
			else:
				statline['fgaagainst'] += 1
				if '3PT' in description:
					statline['3paagainst'] += 1

			if secondary:
				""" Block on play """
				if teamFor == thisTeam:
					statline['blkagainst'] += 1
				else:
					statline['blkfor'] += 1

			lastPlayTeam = teamFor

		elif playType == 3:
			""" Free throw """
			if teamFor == thisTeam:
				statline['ftafor'] += 1
				if not 'MISS' in description and play[playIndex['SCORE']]:
					statline['ftmfor'] += 1
					statline['ptsfor'] += 1
			else:
				statline['ftaagainst'] += 1
				if not 'MISS' in description and play[playIndex['SCORE']]:
					statline['ftmagainst'] += 1
					statline['ptsagainst'] += 1
			lastPlayTeam = teamFor

		elif playType == 4:
			""" Rebound """
			if teamFor == thisTeam:
				statline['trbfor'] += 1
				if lastPlayTeam == thisTeam:
					statline['orbfor'] += 1
				else:
					statline['drbfor'] += 1
			else:
				statline['trbagainst'] += 1
				if lastPlayTeam == thisTeam:
					statline['drbagainst'] += 1
				else:
					statline['orbagainst'] += 1

		elif playType == 5:
			""" Turnover """
			if teamFor == thisTeam:
				if secondary:
					if 'STEAL' in description:
						statline['stlfor'] += 1
						statline['toagainst'] += 1
					else:
						statline['stlagainst'] += 1
						statline['tofor'] += 1
				else:
					statline['tofor'] +=1
			else:
				if secondary:
					if 'STEAL' in description:
						statline['stlagainst'] += 1
						statline['tofor'] += 1
					else:
						statline['stlfor'] += 1
						statline['toagainst'] += 1
				else:
					statline['toagainst'] +=1

		elif playType == 6:
			""" Foul """
			if teamFor == thisTeam:
				statline['pffor'] += 1
			else:
				statline['pfagainst'] += 1

		else:
			""" Other """
			pass

		if period == play[playIndex['PERIOD']]:
			if not time == play[playIndex['PCTIMESTRING']]:
				timeSplit = time.split(':')
				newTimeSplit = play[playIndex['PCTIMESTRING']].split(':')
				seconds = int(timeSplit[1]) - int(newTimeSplit[1])
				if seconds < 0:
					seconds += 60
				statline['time'] += seconds
		else:
			time = '12:00' if period in [1, 2, 3, 4] else '5:00'

		margin = play[playIndex['SCOREMARGIN']]
		if margin:
			margin = 0 if margin == 'TIE' else int(margin)
			if thisTeam != homeTeam:
				margin *= -1
			statline['margins'].append(margin)

		period = play[playIndex['PERIOD']]
		time = play[playIndex['PCTIMESTRING']]
	return statline


##### Statline management #####

def addStatlines(a, b):
	"""
	Add two statlines together and return a new one.
	"""
	c = {}
	allKeys = a.keys()

	for key in allKeys:
		if key in ['home', 'team', 'opponent']:
			c[key] = b[key] if a[key] == b[key] or a[key] == 'unassigned' else 'multiple'
		elif key == 'margins':
			c[key] = copy(a[key]) + copy(b[key])
		else:
			c[key] = a[key] + b[key]

	return c


##### Calculation methods #####

def calculatePossessions(TmFGA, TmFTA, TmORB, TmDRB, TmFG, TmTOV, OppFGA, OppFTA, OppORB, OppDRB, OppFG, OppTOV):
	""" 
	Calculate the number of possessions in a NBA game based on Dean Oliver's formula. 
	"""
	return 0.5 * ((TmFGA + 0.4 * TmFTA - 1.07 * (TmORB * 1.0 / (TmORB + OppDRB)) * (TmFGA - TmFG) + TmTOV) 
		+ (OppFGA + 0.4 * OppFTA - 1.07 * (OppORB * 1.0 / (OppORB + TmDRB)) * (OppFGA - OppFG) + OppTOV))


def calculateNetRating(statline): 
	"""
	Given a statline, return the float value of a team's net rating rounded to 3 digits of precision.
	The formula is defined as (Points scored - points allowed) / 100 possessions
	Therefore, the net rating is (Points scored - points allowed) * 100 / (calculated possessions)
	"""
	possessions = calculatePossessions( statline['fgafor'],
										statline['ftafor'], 
										statline['orbfor'],
										statline['drbfor'],
										statline['fgmfor'],
										statline['tofor'],
										statline['fgaagainst'],
										statline['ftaagainst'],
										statline['orbagainst'],
										statline['drbagainst'],
										statline['fgmagainst'],
										statline['toagainst'] )
	raw_point_difference = statline['ptsfor'] - statline['ptsagainst']
	net_rating = raw_point_difference * 100.0 / possessions
	return round(net_rating, 3)
	