import time

import gspread
from gspread import Spreadsheet
import json
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter, BASIC_FORMAT


logger = getLogger(__name__)
logger.setLevel(INFO)
# logger.setLevel(DEBUG)

handler = StreamHandler()
handler.setFormatter(Formatter(BASIC_FORMAT))
handler.setLevel(INFO)
# handler.setLevel(DEBUG)
logger.addHandler(handler)

# 3C fargo ref
RatingSheetName = "集約：Ratings"
JoinedCell = "C1"
COL_PLAYER = 0
COL_RATING = 1
COL_R = 2
COL_LAST_SEEN = 3
COL_SKILL_LEVEL = 4
COL_START_TARGET = 5
COL_CURRENT_TARGET = 6
COL_THIS_WEEK_LEVEL = 7
COL_COMPARE_RESULT = 8


# タブと改行で連結されたリストを取得する
def get_rating_list(spread_sheet: Spreadsheet) -> list:
    work_sheet = spread_sheet.worksheet(RatingSheetName)

    start = time.time()
    rating_list = []

    rating_rows = None
    try:
        rating_rows = work_sheet.acell(JoinedCell).value
    except gspread.exceptions.APIError as e:
        logger.error(e.response.reason)

    logger.debug(rating_rows)
    if rating_rows is None:
        return rating_list

    for rating_row in rating_rows.split("\n"):
        rating_cols = rating_row.split("\t")

        player_name = rating_cols[COL_PLAYER]
        if not player_name:
            break

        player_info = {}
        player_info["player"] = player_name
        player_info["rating"] = rating_cols[COL_RATING]
        player_info["ranking"] = rating_cols[COL_R]
        player_info["lastSeen"] = rating_cols[COL_LAST_SEEN]
        player_info["skillLevel"] = rating_cols[COL_SKILL_LEVEL]
        player_info["startTarget"] = rating_cols[COL_START_TARGET]
        player_info["currentTarget"] = rating_cols[COL_CURRENT_TARGET]
        player_info["thisWeekLevel"] = rating_cols[COL_THIS_WEEK_LEVEL]
        player_info["compareResult"] = rating_cols[COL_COMPARE_RESULT]

        logger.debug(player_info)
        rating_list.append(player_info)

    end = time.time()
    logger.debug(end - start)
    return rating_list
