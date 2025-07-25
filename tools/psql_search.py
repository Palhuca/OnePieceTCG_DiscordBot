from langchain.agents import tool
import psycopg2
import sqlparse
from pydantic import BaseModel, Field

class CardSearchArgs(BaseModel):
    query: str = Field(description='Select SQL command that will be executed to search a card')

@tool(args_schema= CardSearchArgs)
def card_search(query:str = "SELECT * FROM op_tcg_card_list WHERE ID = 'ST14-003'"):
    """Search for a card using a SQL as input and executing on a database that has the table named op_tcg_card_list.
    SQL command must be valid
    When using color search concat both colors with the first latter of each color in caps (Pascal Case) (exemple: BlackPurple, BlueBlack)
    When using color search always try to switch color orders exemple: BlueRed, RedBlue
    All columns except url, id, set and Card Type use Pascal Case patten
    url, id, set and Card Type columns use all letters in caps
    Exemples:
        SELECT * FROM op_tcg_card_list WHERE ID = 'ST14-003'
        SELECT * FROM op_tcg_card_list WHERE Title LIKE '%Luffy%' AND Set = 'OP09'"
        SELECT * from op_tcg_card_list WHERE color LIKE '%Yellow%' AND Cost = 3 AND Title = 'Nami'
        SELECT * from op_tcg_card_list WHERE color LIKE '%BlackYellow%' AND card_type = 'LEADER' AND Title = 'Monkey.D.Luffy'
    Cards with the same id are just alternative arts of that card and can be ignored
    The op_tcg_card_list columns are: URL,Effect,ID,Title,Price,Cost,Color,Types,Attributes,Rarity,Card Type,Power,Source,Set. Don't use ' or \" on column names. ID must be all in caps"""

    conn = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='123qwe',
        host='localhost',
        port='5432'
    )

    cursor = conn.cursor()
    query = query.replace("\"", "\'")
    statements = sqlparse.parse(query)
    for statement in statements:
        print(statement)
        if statement.get_type() == "SELECT":
            cursor.execute(query)
            response = cursor.fetchall()
            return response
        else:
            return "query must be a well formed SELECT"