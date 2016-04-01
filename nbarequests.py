# nbarequests.py

import requests
import json
import os

##### Globals #####

season = '2014-15'
season_type = 'Regular Season'
league_id = '00'
request_headers = {'User-Agent': 'Chrome/48.0.2564.103', 'Connection': 'keep-alive'}

data_dir = 'data'
play_log_dir = 'play_logs'
extension = '.json'

##### Universal methods #####

def makeRequestURL(api_type, parameters = {}):
	""" 
	Given a base and a dictionary of parameters,
	return a valid url for a NBA API request
	"""
	base_url = 'http://stats.nba.com/stats/'
	paramString = ''
	for param, value in parameters.iteritems():
		param = param.replace(' ', '+')
		value = value.replace(' ', '+')
		paramString += param + '=' + value + '&'

	return base_url + api_type + '?' + paramString[:-1]

##### Specific request methods #####

def getTeamIDsForSeason():
	"""
	Return a dictionary of all NBA.com team IDs where each entry
	has the form TeamAbbreviation: TeamID
	"""
	request_type = 'leaguedashptteamdefend'
	parameters = {
		'Season': season,
		'SeasonType': season_type,
		'LeagueID': league_id,
		'Conference': '',
		'DateFrom': '',
		'DateTo': '',
		'DefenseCategory': 'Overall',
		'PerMode': 'PerGame'
	}
	request_url = makeRequestURL(request_type, parameters)
	response = requests.get(request_url, headers=request_headers)
	json_list = response.json()
	teams = json_list['resultSets'][0]['rowSet']
	teamIDs = {str(team[2]): str(team[0]) for team in teams}
	return teamIDs

def getGameIDsForSeason():
	"""
	Return a dictionary of all games from the season,
	according to the NBA.com game ID. Entries take the form
	Game Name : ID, where Game Name = yyyymmdd + away team + home team
	'20160305GSWBOS' would be the March 5, 2016 GSW @ BOS game
	"""
	request_type = 'leaguegamelog'
	parameters = {
		'Season': season,
		'SeasonType': season_type,
		'LeagueID': league_id,
		'Direction': 'DESC',
		'PlayerOrTeam': 'T',
		'Sorter': 'PTS'
	}
	request_url = makeRequestURL(request_type, parameters)
	response = requests.get(request_url, headers=request_headers)
	json_list = response.json()
	games = json_list['resultSets'][0]['rowSet']
	gameDict = {}
	for game in games:
		if '@' in game[6]:
			gameName = str(game[5]).replace('-', '') + str(game[6]).replace(' @ ', '')
			gameDict[gameName] = str(game[4])
	return gameDict

def getPlaysForGameID(game_id, save_local=True):
	"""
	Given a NBA.com game ID, return the list
	of all plays from that game. Each play is
	a tuple passed directly as received from NBA.com
	"""
	path = os.path.join(data_dir, play_log_dir, str(game_id) + extension)

	if os.path.isfile(path) and save_local:
		with open(path) as data_file:
			data = json.load(data_file)
		return data

	request_type = 'playbyplayv2'
	params = {
		'EndPeriod': '10',
		'EndRange': '55800',
		'RangeType': '2',
		'Season': season,
		'SeasonType': season_type,
		'StartPeriod': '1',
		'StartRange': '0',
		'GameID': game_id
	}
	
	request_url = makeRequestURL(request_type, params)
	response = requests.get(request_url, headers=request_headers)
	json_plays = response.json()
	plays = json_plays['resultSets'][0]['rowSet']
	
	if len(plays) == 0:
		return []

	last_time = plays[-1][6]
	last_period = plays[-1][4]

	if save_local and (last_time == '0:00' and last_period not in [1, 2, 3]):
		with open(path, 'w') as save_file:
			json.dump(plays, save_file)
    
	return plays
