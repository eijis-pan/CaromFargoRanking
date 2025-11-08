import json
import tempfile
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter, BASIC_FORMAT
import gspread
from google.auth import exceptions
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import storage
import os

import config
from scripts.google_auth import get_google_auth_settngs
from scripts.sheet_api_player_ranking import get_rating_list

logger = getLogger(__name__)
# logger.setLevel(INFO)
logger.setLevel(DEBUG)

handler = StreamHandler()
handler.setFormatter(Formatter(BASIC_FORMAT))
# handler.setLevel(INFO)
handler.setLevel(DEBUG)
logger.addHandler(handler)

if __name__ == "__main__":

    auth_settings = get_google_auth_settngs()
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as file:
        json.dump(auth_settings, file)
        authJsonPath = file.name
        file.close()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = authJsonPath

    try:
        # credentials = ServiceAccountCredentials.from_json_keyfile_dict(auth_settings, scope)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(authJsonPath, scope)
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets())
        client = gspread.authorize(credentials)
    except exceptions.DefaultCredentialsError as e:
        logger.error(f"Google認証に失敗")
        exit(1)
    finally:
        os.remove(authJsonPath)

    try:
        spread_sheet = client.open_by_key(os.environ['CAROM_FARGO_SPREADSHEET_ID'])
    except Exception as e:
        logger.error("Google SpreadSheet が見つからないかアクセス権限がありません")
        exit(2)

    logger.debug(f"レーティングデータ取得")
    try:
        ratings = get_rating_list(spread_sheet)
    except Exception as e:
        logger.error(f"レーティングデータ取得に失敗")
        exit(3)

    logger.debug(ratings)
    if 0 < len(ratings):
        try:
            with open(config.RATING_LIST_FILE_PATH, mode="w", encoding="utf-8") as file:
                json.dump(ratings, file, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))
        except Exception as e:
            logger.error(f"レーティングファイル作成に失敗")
            exit(4)
