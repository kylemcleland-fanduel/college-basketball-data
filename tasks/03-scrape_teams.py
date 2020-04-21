import os
import re
import csv
from datetime import date

import requests
from bs4 import BeautifulSoup

from helpers.context import find_most_recent_export


def team_scraper(team_id):
    """
    Scrapes the team summary page given a team_id.
    Returns team_name.
    """
    team_url = f"https://stats.ncaa.org/teams/{team_id}"
    response = requests.get(team_url)
    soup = BeautifulSoup(response.text, features="html.parser")

    team_details = soup.find_all("legend")

    team_short_name = re.findall(
        r"alt=\"([^\"]*)", str(team_details[0].find_all("img")))

    team_long_name = re.findall(
        r"ATHLETICS_URL\">([^<]*)", str(team_details[0].find_all("a")))

    return team_id, team_short_name, team_long_name


if __name__ == "__main__":
    season = 2020

    # Load most recent export of {season}_game-summaries for parsing team_ids
    file_folder = os.path.join(os.path.dirname(
        __file__), "../raw_data")
    file_prefix = f"{season}_game-summaries"
    game_summaries_file = find_most_recent_export(
        file_folder=file_folder, file_prefix=file_prefix)

    # Grab list of all visit_ids and home_ids, then de-dupe for list of unique teams
    print(f"Loading list of game_ids from: {game_summaries_file}")
    all_team_ids = []
    with open(game_summaries_file, "r") as f:
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            all_team_ids.append(row["visit_id"])
            all_team_ids.append(row["home_id"])

    team_ids = list(dict.fromkeys(all_team_ids))
    print(f"Found {len(team_ids)} unique team_ids")

    # Create list of team details
    print("Parsing team_ids")
    team_details = []
    for team_id in team_ids:
        team_info = team_scraper(team_id)
        print(f"     {team_info}")
        team_details.append(team_info)

        # Write team details to txt file
    date_stamp = date.today().strftime('%Y-%m-%d')
    file_name = f"{season}_teams_{date_stamp}.txt"
    file_path = os.path.join(os.path.dirname(
        __file__), "../raw_data/", file_name)

    with open(file_path, "w") as f:
        # header row
        f.write(
            "team_id|team_short_name|team_long_name\n")

        # body
        writer = csv.writer(f, delimiter="|", quoting=csv.QUOTE_MINIMAL)
        writer.writerows(team_details)
