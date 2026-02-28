import os.path
import time
import warnings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import pandas as pd
from selenium.webdriver.common.options import PageLoadStrategy

from sqlalchemy.dialects.oracle.dictionary import all_tables

import model.card_model

file_path = 'tempScrapCards.csv'
options = Options()
# options.headless = True
# options.add_argument("--window-size=1280,720")
options.add_argument("--headless")
# options.add_argument("--no-sandbox")

path_to_extension = "/home/palhuca/.config/google-chrome/Default/Extensions/cfhdojbkjhnklbpkdaibdccddilifddb/4.32.6_0"
options.add_argument('--load-extension=' + path_to_extension)
options.page_load_strategy='eager'
driver = webdriver.Chrome(options=options)
collection_list = ["OP01", "OP02", "OP03", "OP04", "OP05", "OP06", "OP07", "OP08", "OP09", "OP10",
                   "OP11", "OP12", "OP13", "OP14" "P", "EB01", "EB02", "EB03", "EB04"]


def execute(url, search_id):


    if os.path.exists('tempScrapCards.csv'):
        csvdf = pd.read_csv('tempScrapCards.csv')
        if search_id in csvdf.values:
            print(f"Card with ID {search_id} already exists in the CSV file.")
            return True, False

    driver.get(url)

    time.sleep(2)
    driver.execute_script("window.stop();")

    if "Page not found" in driver.title:
        print("Card not found or URL is incorrect.")
        return False, False

    #initializing variables with default values
    card_name = "NULL"
    card_id = "NULL"
    card_card_type = "NULL"
    card_color = "NULL"
    card_cost = "NULL"
    card_life = "NULL"
    card_effect = "NULL"
    card_type = "NULL"
    card_counter = "NULL"
    card_power = "NULL"
    card_attribute = "NULL"
    card_block = "NULL"
    card_collection_name = "NULL"
    card_collection_id = "NULL"
    card_trigger = "False"

    card_elements = driver.find_element(By.CLASS_NAME,"card-text")
    #List of all information sections in the card
    card_section_list = card_elements.find_elements(By.CLASS_NAME, "card-text-section")
    card_name = card_section_list[0].find_element(By.CLASS_NAME, "card-text-name").text
    card_id = card_section_list[0].find_element(By.CLASS_NAME, "card-text-id").text
    card_category = card_section_list[0].find_elements(By.CLASS_NAME, "card-text-type")
    span_info = card_category[0].find_elements(By.TAG_NAME, "span")
    card_card_type = span_info[0].text
    card_color = span_info[1].text
    full_category = card_category[0].text
    if card_card_type in ["Leader", "Character"]:
        card_effect = card_section_list[2].text
        if "\n" in card_effect:
            card_effect = card_effect.replace("\n", " || ")
        card_type = card_section_list[3].text
    else:
        card_effect = card_section_list[1].text
        card_type = card_section_list[2].text

    x = re.search(r"^\[Trigger\] (.*)", card_effect, flags=re.MULTILINE)
    if x:
        card_trigger = "True"
        card_trigger_effect = x.group(1)
        card_effect = card_effect.replace("[Trigger] " + card_trigger_effect, "").strip()
    else:
        card_trigger = "False"
        card_trigger_effect = "NULL"

    x = re.search(r".*(\d) Life", full_category)
    if x:
        card_life = x.group(1)
        card_cost = "NULL"
    else:
        card_life = "NULL"
        x = re.search(r".*(\d) Cost", full_category)
        if x:
            card_cost = x.group(1)
        else:
            card_cost = "NULL"

    if card_card_type not in ["Event", "Stage"]:
        attributes_section = card_section_list[1]
        if attributes_section:
            all_attributes = attributes_section.text
            x = re.search(r"(\d+) Power.*", all_attributes)
            if x:
                card_power = x.group(1)
            else:
                card_power = "NULL"

            card_att_span = attributes_section.find_element(By.TAG_NAME, "span")
            if card_att_span:
                card_attribute = card_att_span.text

            x = re.search(r"/+(\d+) Counter", full_category)
            if x:
                card_counter = x.group(1)
            else:
                card_counter = "NULL"
        else:
            card_power = "NULL"
            card_attribute = "NULL"
            card_counter = "NULL"

    card_block = driver.find_element(By.CLASS_NAME, "regulation-mark").text
    x = re.search(r"(OP\d{2})-.*", card_id)
    if x:
        card_collection_id = x.group(1)

    card_print_version_section = driver.find_element(By.CLASS_NAME, "card-prints-versions")
    card_collection_name = card_print_version_section.find_element(By.TAG_NAME, "a").text

    card = model.card_model.card(
        name=card_name,
        id=card_id,
        card_type=card_card_type,
        color=card_color,
        cost=card_cost,
        life=card_life,
        effect=card_effect,
        type=card_type,
        counter=card_counter,
        power=card_power,
        attribute=card_attribute,
        block=card_block,
        collection_name=card_collection_name,
        collection_id=card_collection_id,
        trigger=card_trigger
        ,trigger_effect=card_trigger_effect
    )

    # Save card data to database or CSV
    save_card_data(card)

    return True, True

# Method to save card data to csv and database
def save_card_data(card_model):
    # print(card_model)
    df = pd.DataFrame(card_model.__dict__)
    df.to_csv(file_path,index=False, header=not(os.path.exists(file_path)), mode="a")
    return True

if __name__ == '__main__':
    col_not_ended = True
    # add st 01 to 29 to collection list
    for i in range(1, 30):
        collection_list.append(f"ST{i:02d}")
    collection_list = ["PRB01", "PRB02", "EB04"]
    for collection in collection_list:
        card_id_to_search = 1
        col_not_ended = True
        while col_not_ended:
            print(f"Card {collection}-{card_id_to_search} will be scraped from limitlesstcg.com")
            col_not_ended, saved_to_csv = execute(f"https://onepiece.limitlesstcg.com/cards/{collection}-{card_id_to_search:03d}", f"{collection}-{card_id_to_search:03d}")
            card_id_to_search += 1
            if saved_to_csv:
                print("Sleeping for 5 seconds to avoid rate limiting...")
                time.sleep(1)
    driver.quit()