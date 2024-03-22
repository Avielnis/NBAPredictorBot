import logging

logging.basicConfig(
    format="%(levelname)s %(asctime)s %(module)s:%(lineno)d: %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("GamblerLoger.log"),
        logging.StreamHandler()
    ]
)



TEAMS_FULL_NAME_TO_SHORT = {
    'Dallas Mavericks': 'DAL',
    'Boston Celtics': 'BOS',
    'Minnesota Timberwolves': 'MIN',
    'Orlando Magic': 'ORL',
    'Toronto Raptors': 'TOR',
    'Cleveland Cavaliers': 'CLE',
    'San Antonio Spurs': 'SA',
    'Brooklyn Nets': 'BKN',
    'Miami Heat': 'MIA',
    'Memphis Grizzlies': 'MEM',
    'Los Angeles Lakers': 'LAL',
    'Phoenix Suns': 'PHO',
    'Detroit Pistons': 'DET',
    'Philadelphia 76ers': 'PHI',
    'New Orleans Pelicans': 'NO',
    'Chicago Bulls': 'CHI',
    'Los Angeles Clippers': 'LAC',
    'Charlotte Hornets': 'CHA',
    'New York Knicks': 'NY',
    'Denver Nuggets': 'DEN',
    'Indiana Pacers': 'IND',
    'Washington Wizards': 'WAS',
    'Atlanta Hawks': 'ATL',
    'Milwaukee Bucks': 'MIL',
    'Oklahoma City Thunder': 'OKC',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'Houston Rockets': 'HOU',
    'Golden State Warriors': 'GS',
    'Utah Jazz': 'UTA',
}

TEAMS_SHORT_TO_FULL_NAME = {
    'DAL': 'Dallas Mavericks',
    'BOS': 'Boston Celtics',
    'MIN': 'Minnesota Timberwolves',
    'ORL': 'Orlando Magic',
    'TOR': 'Toronto Raptors',
    'CLE': 'Cleveland Cavaliers',
    'SA': 'San Antonio Spurs',
    'BKN': 'Brooklyn Nets',
    'MIA': 'Miami Heat',
    'MEM': 'Memphis Grizzlies',
    'LAL': 'Los Angeles Lakers',
    'PHO': 'Phoenix Suns',
    'DET': 'Detroit Pistons',
    'PHI': 'Philadelphia 76ers',
    'NO': 'New Orleans Pelicans',
    'CHI': 'Chicago Bulls',
    'LAC': 'Los Angeles Clippers',
    'CHA': 'Charlotte Hornets',
    'NY': 'New York Knicks',
    'DEN': 'Denver Nuggets',
    'IND': 'Indiana Pacers',
    'WAS': 'Washington Wizards',
    'ATL': 'Atlanta Hawks',
    'MIL': 'Milwaukee Bucks',
    'OKC': 'Oklahoma City Thunder',
    'POR': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'HOU': 'Houston Rockets',
    'GS': 'Golden State Warriors',
    'UTA': 'Utah Jazz',
}



