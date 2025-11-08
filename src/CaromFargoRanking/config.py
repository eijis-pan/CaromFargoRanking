import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RATING_LIST_FILE_PATH = os.path.join(DATA_DIR, "rating_list.json")
RATING_LIST_CSV_FILE_PATH = os.path.join(DATA_DIR, "rating_list.csv")
