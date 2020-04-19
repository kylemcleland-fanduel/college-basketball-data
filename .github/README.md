# college-basketball-data

## Flowchart 
![alt text](readme_flowchart.png "Data Flowchart")

## Tasks

### `01-scrape_game_ids.py`
Parameters:
* season (int): The college basketball season (year). For a season e.g. 2019-2020, you would enter the year when the season ended (2020).

Takes a season (int) and scrapes a list of game_ids and creates a text file with a list of all game_ids at [`/raw_data/{season}_game-ids_{run_date}.txt`](/raw_data)


## Data Dictionary

### Raw Data

#### game-ids: 
List of game_ids for a season.

Fields:
* season (integer): The college basketball season (year). For a season e.g. 2019-2020, you would enter the year when the season ended (2020).
* game_id (integer): The unique game id used by the NCAA.