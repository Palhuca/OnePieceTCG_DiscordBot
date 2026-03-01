import os
from dotenv import load_dotenv, find_dotenv
from langchain_chroma import Chroma
from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel, Field
from zipp.glob import separate


class GetFromChromaQAArgs(BaseModel):
    query: str = Field(description='Query that will be search in QA')

class GetFromChromaRuleArgs(BaseModel):
    query: str = Field(description='Query that will be search in Rule')

class GetFromChromaCardArgs(BaseModel):
    query: str = Field(description='Card effect that will be used to search a card')



CHROMA_PATH = "chroma"
_ = load_dotenv(find_dotenv())

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large")



@tool(args_schema= GetFromChromaQAArgs)
def get_from_chroma_qa(query:str) -> str:
    """Receive a question and return the most relevant Q&A and card interaction information based on the inputted query that should be used as context. The result contains the source information. The data is formatted as following
    Format: |{Card_Id}|{Q&A_Question}|{Answer}|"""

    print(f"Query received in get_from_chroma_qa: {query}")
    db_qa = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings,
                   collection_name="QeA")
    retsults_qa = db_qa.max_marginal_relevance_search(query, k=3, fetch_k=10)

    out_text_qa = "".join([doc.page_content for doc in retsults_qa])
    out_metadata_qa = [doc.metadata.get("source", None) for doc in retsults_qa]

    formated_sources = f"Sources: {out_metadata_qa}"
    return f"{out_text_qa}"

@tool(args_schema= GetFromChromaRuleArgs)
def get_from_chroma_rule(query:str) -> str:
    """Receive a question and return the most relevant Rules of the One Piece Card Game based on the inputted query that should be used as part of the context.
    The result also contains the source information.
    The data is formatted as following
    Format: {RULE_ID}. {RULE_TEXT}
    Rules are segmented in a section and subsection structure where the RULE_ID have the format 1-1-1-1-1, but must be understood as 1.1.1.1.1.
    Use the RULE_ID to search for the context of those rules using the rule_search tool, example, rule 1.2.3, search for rule 1.2 and 1 to get the context of rule 1.2.3. and give a better answer
"""

    db_qa = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings,
                   collection_name="Rules")
    retsults_qa = db_qa.max_marginal_relevance_search(query, k=5, fetch_k=20)

    out_text_qa = "\n".join([doc.page_content for doc in retsults_qa])
    out_metadata_qa = [doc.metadata.get("source", None) for doc in retsults_qa]

    formated_sources = f"Sources: {out_metadata_qa}"
    return f"{out_text_qa}"

@tool(args_schema= GetFromChromaCardArgs)
def get_from_chroma_card(query:str) -> str:
    """Search semantically for a card using the card text (mainly the effect) as the input parameter. Return the 10 most relevant cards. A more specific search will have better results
    In cases of card effects use this to search the card"""

    db_qa = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings,
                   collection_name="Cards")
    retsults_qa = db_qa.max_marginal_relevance_search(query, k=3, fetch_k=10)

    out_text_qa = "".join([doc.page_content for doc in retsults_qa])
    out_metadata_qa = [doc.metadata.get("source", None) for doc in retsults_qa]

    formated_sources = f"Sources: {out_metadata_qa}"
    return f"{out_text_qa}"
