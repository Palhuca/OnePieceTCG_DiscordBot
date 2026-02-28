import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('OPTCG_CardList.db')
cursor = conn.cursor()

# Create a table for products
# creating card table with columns for card details (id,name,card_type,color,cost,life,effect,type,counter,
# power,attribute,block,collection_name,collection_id,trigger,trigger_effect)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS card (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        card_type TEXT,
        color TEXT,
        cost INTEGER,
        life INTEGER,
        effect TEXT,
        type TEXT,
        counter INTEGER,
        power INTEGER,
        attribute TEXT,
        block TEXT,
        collection_name TEXT,
        collection_id TEXT,
        trigger BOOLEAN,
        trigger_effect TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS rules (
        id TEXT PRIMARY KEY,
        rule TEXT NOT NULL)
''')

# Read the CSV file and insert data into the card table
import pandas as pd
with open('DataScraping/tempScrapCards.csv', 'r', encoding='utf-8') as csvfile:
    df = pd.read_csv(csvfile)
    df.to_sql('card', conn, if_exists='replace', index=False)

# Commit the changes to the database
conn.commit()

# Close the connection
# conn.close()

print("Database 'my_application.db' initialized successfully with 'products' and 'orders' tables.")

# Read the CSV file and insert data into the rule table
with open('data/Rules/normalized_rule_comprehensive.csv', 'r', encoding='utf-8') as csvrulefile:
    df_rule = pd.read_csv(csvrulefile, quotechar='"', sep=',')
    df_rule.to_sql('rules', conn, if_exists='replace', index=False)

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()

print("Database 'my_application.db' initialized successfully with 'products' and 'orders' tables.")