import BBR_functions as bbr
import pandas as pd
import sqlite3

links = []

def create_df(links):
    df = pd.DataFrame(columns = ['Date','Team','Opponent','Player','Position', 'Points'])
    for idx, l in enumerate(links):
        print('Adding Games: ' + str(round(idx / len(links) * 100, 2)) + '% Complete ' + l)
        soup = bbr.to_soup(l)
        home_table = bbr.game_table(soup, True)
        away_table = bbr.game_table(soup, False)
    
        for t in home_table:
            row = {'Date':t[5], 'Team':t[0], 'Opponent':t[1], 'Player':t[2], 'Position':t[3][0], 'Points': t[4]}
            df = df.append(row, ignore_index=True)
        for t in away_table:
            row = {'Date':t[5], 'Team':t[0], 'Opponent':t[1], 'Player':t[2], 'Position':t[3][0], 'Points': t[4]}
            df = df.append(row, ignore_index=True)
    return df

def update_sql(df):
    conn = sqlite3.connect('Basketball_DB')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS bbr (Date, Team, Opponent, Player, Position, Points)')
    conn.commit()

    df.to_sql('bbr', conn, if_exists='append', index = False)

def run_query(query):
    conn = sqlite3.connect('Basketball_DB')
    c = conn.cursor()
    c.execute(query)
    print(pd.read_sql_query(query, conn))



#bbr.add_season_links(2022, links)
#update_sql(create_df(links))

run_query('SELECT Team, Opponent, Position, Avg(points)as ap from bbr where Team = "NYK" group by position, Opponent order by Opponent')