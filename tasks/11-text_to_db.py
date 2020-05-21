import os
import sqlite3

from helpers.context import find_most_recent_export

imports = {
    "game_ids": {"file_prefix": "[@season]_game-ids", "staging_table": "staging_game_ids"},
    "game_summaries": {"file_prefix": "[@season]_game-summaries", "staging_table": "staging_game_summaries"},
    "teams": {"file_prefix": "[@season]_teams", "staging_table": "staging_teams"},
}


def copy_to_db_from_txt(file_path, table, insert_columns=None):
    "Copies text file into a database"


def create_staging_table_ddl(file_path, table):
    "Create staging table dynamically from text file"
    with open(file_path, "r") as f:
        headers = f.readline().replace("\n", "").split("|")

    columns = ""
    for header in headers:
        columns += f"{header} varchar(MAX), "

    staging_ddl = f"DROP TABLE IF EXISTS {table};\n" \
        f"CREATE TABLE {table} " \
        f"({columns[:-2]});"

    print(staging_ddl)


if __name__ == "__main__":
    season = 2020

    import_file_dir = os.path.join(
        os.path.dirname(__file__), "../raw_data/")

    for f in imports:
        # Get file path
        file_prefix = imports[f]["file_prefix"].replace(
            "[@season]", str(season))
        file_path = find_most_recent_export(import_file_dir, file_prefix)
        create_staging_table_ddl(file_path, imports[f]["staging_table"])
