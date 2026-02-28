#testpsql_search.py

import psql_search
import responses

def test_card_search():

    # result = psql_search.list_tables()
    # print("Existing tables:", result)
    # presult = psql_search.search_column("id", "OP12-001")
    # print("Search column result:", presult)
    query = '{"id" : "OP12-001"}'
    print("query is:", type(query), query)
    result = psql_search.card_search.run(query)
    print(result)

if __name__ == "__main__":
    test_card_search()