import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import datetime


def add_season_links(year, list):
    year = str(year)
    content = requests.get('https://www.basketball-reference.com/leagues/NBA_' + year + '_games.html')
    soup = BeautifulSoup(content.text, 'html.parser')
    month_data = soup.find('div', class_='filter').find_all('a')

    for data in month_data:
        month_link = 'https://www.basketball-reference.com' + data['href'] 
        month_content = requests.get(month_link)
        month_soup = BeautifulSoup(month_content.text, 'html.parser')
        
        links = month_soup.find('table', id='schedule').find('tbody').find_all('td', class_='center')

        for l in links:
           link = l.find('a')
           if link:
               list.append('https://www.basketball-reference.com' + link['href'])

#TODO
#def update_links(game_link, list):
    # append game links following the provided game link  

def to_soup(link):
    content = requests.get(link)
    return BeautifulSoup(content.text, 'html.parser')

# Arg away: 0 for Home team, 1 for Away team
def get_team(game_soup, team):
     home_team = ""
     away_team = ""

     header = game_soup.find("div", {"class": "scorebox"})
     game_teams = header.find_all("a")

     for l in game_teams:
        m = re.search('/teams/([A-Z]{3})/\d{4}.html', str(l))
        if m: 
            if away_team == "":
                away_team = m.group(1)
            else:
                home_team = m.group(1)
    
     if team:
        return home_team
     else:
        return away_team

def get_date_link(game_link):
    m = re.search('(\d{4})(\d{2})(\d{2})', game_link)
    if m:
         return m.group(2) + '/' + m.group(3) + '/' + m.group(1)
    else:
         return ""

def get_date(game_soup):
    date = game_soup.find("div", class_="box").find("h1").text
    date = re.search(', (\S* \d+, \d{4})', date).group(1)
    date_time = datetime.datetime.strptime(date, '%B %d, %Y')
    return date_time

def get_position(player_soup):
    try:
        player = player_soup.find_all('p')    
        for position in player:
            matches = re.findall('(Shooting Guard|Power Forward|Point Guard|Small Forward|Center)', position.text)
            if matches:
                return matches

        return matches
    except:
        return ['']

def get_player_name(player_soup):
    try:
        return player_soup.find("h1", itemprop="name").find("span").text
    except:
        return ''

# Given a game link and team (Home: true, Away: false) game_table will return a list of tuples with player name, position and points
def game_table(game_soup, team):
    playing = get_team(game_soup, team)
    against = get_team(game_soup, (not team))
    date = get_date(game_soup)
    table = []
    team_table = game_soup.find('table', id="box-" + playing + "-game-basic").tbody.findAll('tr')

    for x in range(0,5):
        pl = team_table[x].find_all('th')[0].contents[0]
        pl = re.search('/players/\w/\w+.html', str(pl))
        player_soup = to_soup('https://www.basketball-reference.com' + pl.group(0))

        position = get_position(player_soup)
        name = get_player_name(player_soup)
        pnts = team_table[x].find_all('td', {'class': 'right'})[18].contents[0]
        table.append((playing, against, name, position, pnts, date))
    return table





#home = game_table(to_soup('https://www.basketball-reference.com/boxscores/202101010DEN.html'), True)
#away = game_table(to_soup('https://www.basketball-reference.com/boxscores/202110190MIL.html'), False)
#print(home)
#print(away)
#print(get_date(to_soup('https://www.basketball-reference.com/boxscores/202110190MIL.html')))

#home = game_table(to_soup('https://www.basketball-reference.com/boxscores/202101010DEN.html'), True)
#print(home)