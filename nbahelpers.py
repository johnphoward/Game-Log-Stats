# nbahelpers.py

import datetime

# borrowed and adapted from another project

##### useful dictionaries #####

nbaTeams = ['ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC',
 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI',
  'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

teamNameLookup = {
	'ATL':'Atlanta Hawks',
	'BOS':'Boston Celtics',
	'BRK':'Brooklyn Nets', 
	'CHO':'Charlotte Hornets', 
	'CHI':'Chicago Bulls', 
	'CLE':'Cleveland Cavaliers', 
	'DAL':'Dallas Mavericks', 
	'DEN':'Denver Nuggets', 
	'DET':'Detroit Pistons', 
	'GSW':'Golden State Warriors', 
	'HOU':'Houston Rockets', 
	'IND':'Indiana Pacers', 
	'LAC':'Los Angeles Clippers',
	'LAL':'Los Angeles Lakers', 
	'MEM':'Memphis Grizzlies', 
	'MIA':'Miami Heat', 
	'MIL':'Milwaukee Bucks', 
	'MIN':'Minnesota Timberwolves', 
	'NOP':'New Orleans Pelicans',
	'NYK':'New York Knicks', 
	'OKC':'Oklahoma City Thunder', 
	'ORL':'Orlando Magic', 
	'PHI':'Philadelphia 76ers',
	'PHO':'Phoenix Suns', 
	'POR':'Portland Trailblazers', 
	'SAC':'Sacramento Kings', 
	'SAS':'San Antonio Spurs', 
	'TOR':'Toronto Raptors', 
	'UTA':'Utah Jazz', 
	'WAS':'Washington Wizards'
}

knownAbbreviations = {
	'ATL': ['ATL'],
	'BOS': ['BOS'],
	'BRK': ['BRK', 'BKN'], 
	'CHO': ['CHO', 'CHA'], 
	'CHI': ['CHI'], 
	'CLE': ['CLE'], 
	'DAL': ['DAL'], 
	'DEN': ['DEN'], 
	'DET': ['DET'], 
	'GSW': ['GSW', 'GS'], 
	'HOU': ['HOU'], 
	'IND': ['IND'], 
	'LAC': ['LAC'],
	'LAL': ['LAL'], 
	'MEM': ['MEM'], 
	'MIA': ['MIA'], 
	'MIL': ['MIL'], 
	'MIN': ['MIN'], 
	'NOP': ['NO', 'NOR', 'NOP'],
	'NYK': ['NY', 'NYK'], 
	'OKC': ['OKC'], 
	'ORL': ['ORL'], 
	'PHI': ['PHI'],
	'PHO': ['PHO', 'PHX'], 
	'POR': ['POR'], 
	'SAC': ['SAC'], 
	'SAS': ['SAS', 'SA'], 
	'TOR': ['TOR'], 
	'UTA': ['UTA', 'UTAH'], 
	'WAS': ['WAS', 'WASH']
}

reverseTeamNameLookup = {
	'Atlanta Hawks':'ATL',
	'Boston Celtics':'BOS',
	'Brooklyn Nets':'BRK', 
	'Charlotte Hornets':'CHO',
	'Charlotte Bobcats':'CHA',
	'Chicago Bulls':'CHI', 
	'Cleveland Cavaliers':'CLE', 
	'Dallas Mavericks':'DAL', 
	'Denver Nuggets':'DEN', 
	'Detroit Pistons':'DET', 
	'Golden State Warriors':'GSW', 
	'Houston Rockets':'HOU', 
	'Indiana Pacers':'IND', 
	'Los Angeles Clippers':'LAC',
	'Los Angeles Lakers':'LAL', 
	'Memphis Grizzlies':'MEM', 
	'Miami Heat':'MIA', 
	'Milwaukee Bucks':'MIL', 
	'Minnesota Timberwolves':'MIN', 
	'New Orleans Pelicans':'NOP',
	'New Orleans Hornets':'NOH',
	'New York Knicks':'NYK', 
	'Oklahoma City Thunder':'OKC', 
	'Orlando Magic':'ORL', 
	'Philadelphia 76ers':'PHI',
	'Phoenix Suns':'PHO', 
	'Portland Trailblazers':'POR',
	'Portland Trail Blazers':'POR', 
	'Sacramento Kings':'SAC', 
	'San Antonio Spurs':'SAS', 
	'Toronto Raptors':'TOR', 
	'Utah Jazz':'UTA', 
	'Washington Wizards':'WAS'
}

monthLookup = {
	'Jan':'01',
	'Feb':'02',
	'Mar':'03',
	'Apr':'04',
	'May':'05',
	'Jun':'06',
	'Jul':'07',
	'Aug':'08',
	'Sep':'09',
	'Oct':'10',
	'Nov':'11',
	'Dec':'12'
}

formalMonthLookup = {
	'01':'January',
	'02':'February',
	'03':'March',
	'04':'April',
	'05':'May',
	'06':'June',
	'07':'July',
	'08':'August',
	'09':'September',
	'10':'October',
	'11':'November',
	'12':'December'
}

##### Methods #####

def convertToSeconds(line):
	if type(line) == int:
		return line
	if line == '0':
		return 0
	line = str(line)
	x = int(line[0:line.find(':')]) * 60
	if '.' in line:
		y = int(line[line.find(':') + 1: line.find('.')])
	else:
		y = int(line[line.find(':') + 1:])
	return str(x + y)

def getTodaysDate():
	thisYear = datetime.date.today().year
	month = datetime.date.today().month
	day = datetime.date.today().day

	if len(str(month)) < 2:
		month = '0' + str(month)
	if len(str(day)) < 2:
		day = '0' + str(day)

	date = str(thisYear) + str(month) + str(day)
	return date

def getCurrentSeason():
	thisYear = datetime.date.today().year
	month = datetime.date.today().month
	day = datetime.date.today().day
	if month > 10:
		return thisYear + 1
	elif month == 10 and day > 25:
		return thisYear + 1
	else:
		return thisYear

def getAbbreviationFromTeamName(name):
	for key in reverseTeamNameLookup.keys():
		if name in key:
			return reverseTeamNameLookup[key]
	print 'Failure!!!!!!!!!'
	print name
	return 'FAILED'

def checkKnownAbbreviations(abbr):
	if abbr in knownAbbreviations.keys():
		return abbr
	for key in knownAbbreviations.keys():
		if abbr in knownAbbreviations[key]:
			return key
