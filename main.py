from dotenv import load_dotenv, find_dotenv

import db_initialize
from DiscordBot import initializeDiscord
import os

#load token from env file
_ = load_dotenv(find_dotenv())
restChroma = False
updateCardList = False
updateQA = False

def initialize_db():
    db = db_initialize.Db_Loader()
    if restChroma:
        db.clean_chroma_db()
    db.start_chroma_db()
    print(f'Bot finished loading data to Database!')


if __name__ == '__main__':
    initialize_db()
    initializeDiscord()