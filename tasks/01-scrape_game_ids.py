import os
import re
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup


def get_season_context(year):
    '''
    Return season_id, start_date, and end_date for a given year.
    List of seasons is manually hard-coded due to small scope. 
    To add a season, simply add it to the dictionary.
    '''
    seasons = {
        2019: {
            "season_id": 14300,
            "start_date": date(2018, 11, 6),
            "end_date": date(2019, 4, 8),
        },
        2020: {
            "season_id": 17060,
            "start_date": date(2019, 11, 5),
            "end_date": date(2020, 3, 11),
        },
    }

    if year in seasons:
        return seasons[year]
    else:
        print(f"I didn't understand that input for season: {year} \n"
              f"Please choose from the following inputs: \n"
              f"{list(seasons)}"
              )
        quit()


def game_id_scraper(season):
    print(f"Scraping game IDs for {season}.")
    season_context = get_season_context(season)

    loop_date = season_context["start_date"]
    loop_end_date = season_context["end_date"]
    game_ids = []

    while loop_date <= loop_end_date:
        scoreboard_url = f"http://stats.ncaa.org/season_divisions/{season_context['season_id']}/scoreboards?game_date={loop_date.strftime('%m/%d/%y')}"
        response = requests.get(scoreboard_url)

        soup = BeautifulSoup(response.text, features="html.parser")
        _game_ids = re.findall("contests/([0-9]*)/box_score", str(soup))

        game_ids.extend(_game_ids)
        loop_date = loop_date + timedelta(days=1)

    return game_ids


if __name__ == "__main__":

    # Scrape game_ids from a season and write to .csv
    season = 2020
    game_ids = game_id_scraper(season=season)

    date_stamp = date.today().strftime('%Y-%m-%d')
    file_name = f"{season}_game-ids_{date_stamp}.txt"
    file_path = os.path.join(os.path.dirname(
        __file__), "../raw_data/", file_name)

    with open(file_path, "w") as f:
        # header row
        f.write("season|game_id\n")

        # body
        for game_id in game_ids:
            f.write(f"{season}|{game_id}\n")
