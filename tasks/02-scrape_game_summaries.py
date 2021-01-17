import os
import re
import csv
from datetime import date

import requests
from bs4 import BeautifulSoup

from helpers.context import find_most_recent_export


def game_summary_scraper(game_id):
    """
    Scrapes the box score information give a game_id.
    Returns a list of summary information.
    """

    box_score_url = f"http://stats.ncaa.org/contests/{game_id}/box_score"
    headers = {'user-agent': 'my-app/0.0.1'}
    response = requests.get(box_score_url, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    game_details = soup.find_all("table")
    """
    table [0] = score
    table [1] = game info (date, attendance)
    table [2] = officials
    table [3] = away box score
    table [4] = home box score
    """

    visit_id, home_id = re.findall(
        r"teams/([0-9]*)", str(game_details[0].find_all("a"))
    )

    visit_scores = re.findall(
        r">([0-9]*)</td>", str(game_details[0].find_all("tr")[1])
    )

    home_scores = re.findall(
        r">([0-9]*)</td>", str(game_details[0].find_all("tr")[2])
    )
    try:
        game_date = re.findall(
            r'(\d\d/\d\d/\d\d\d\d\s\d\d:\d\d\s\w\w)', str(game_details[2]))[0]
    except:
        game_date = ""

    try:
        attendance = re.findall(r"<td>([0-9][^<]*)", str(game_details[2]))[0]
        attendance = int(attendance.replace(",", ""))
    except:
        attendance = -1

    try:
        officials = re.findall(
            r"\n\s\s*([^<^\n^]*)[^<]", str(game_details[3]))  # find this later
    except:
        officials = []

    return (
        game_id,
        game_date,
        int(visit_id),
        int(home_id),
        visit_scores,
        home_scores,
        attendance,
        officials,
    )


if __name__ == "__main__":
    season = 2021

    # Load most recent export of {season}_game-ids for parsing
    file_folder = os.path.join(os.path.dirname(
        __file__), "../raw_data")
    file_prefix = f"{season}_game-ids"
    game_ids_file = find_most_recent_export(
        file_folder=file_folder, file_prefix=file_prefix)

    print(f"Loading list of game_ids from: {game_ids_file}")
    game_ids = []
    with open(game_ids_file, "r") as f:
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            game_ids.append(row["game_id"])

    # Create list of game details
    print("Parsing game box scores")
    game_details = []
    for game_id in game_ids[1:]:
        game_info = game_summary_scraper(game_id)
        print(f"     {game_info}")
        game_details.append(game_info)

    # Write game details to txt file
    date_stamp = date.today().strftime('%Y-%m-%d')
    file_name = f"{season}_game-summaries_{date_stamp}.txt"
    file_path = os.path.join(os.path.dirname(
        __file__), "../raw_data/", file_name)

    with open(file_path, "w") as f:
        # header row
        f.write(
            "game_id|game_date|visit_id|home_id|visit_scores|home_scores|attendance|officials\n")

        # body
        writer = csv.writer(f, delimiter="|", quoting=csv.QUOTE_MINIMAL)
        writer.writerows(game_details)
