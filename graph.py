from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel

from langgraph.graph import START, END, StateGraph
from langgraph.types import Send

from schemas import *
from prompt_template import *

from dotenv import load_dotenv

from tools.chroma_search import get_from_chroma_card
from tools.psql_search import card_search, generic_sql_tool

load_dotenv()

# llm_model = 'gpt-5-nano-2025-08-07'
llm_model = 'gpt-4o-mini-2024-07-18'
llm = ChatOpenAI(model=llm_model)

#Nós
def build_first_query(state: ReportState):

    users_input = state.user_input
    prompt = build_queries.format(user_input=users_input)
    query_llm = llm.with_structured_output(QueryStructure)
    response = query_llm.invoke(prompt)
    return {"queries": response.inputs}

def translate_input(state: ReportState):

    users_input = state.user_input
    prompt = translate_template.format(input_msg=users_input)
    chain_translate = llm | StrOutputParser()
    result = chain_translate.invoke(prompt)
    print(result)
    return result

def card_finder(query: str):
    # tools = [card_search, get_from_chroma_card]
    tools = generic_sql_tool(llm).get_tools()
    system_prompt = card_finder_system_template
    user_prompt = {"messages": [{"role": "user", "content": query}]}

    result = send_to_llm_with_tools(user_prompt, tools, system_prompt)
    query_results = QueryResult(type="card_info", content=result["messages"][-1].content)
    return {"query_results": [query_results]}

def rule_finder(query: str):
    tools = generic_sql_tool(llm).get_tools()
    system_prompt = card_finder_system_template
    user_prompt = {"messages": [{"role": "user", "content": query}]}

    result = send_to_llm_with_tools(user_prompt, tools, system_prompt)
    query_results = QueryResult(type="rule_info", content=result["messages"][-1].content)
    return {"query_results": [query_results]}

def spawn_researchers(state:ReportState):
    query_list = state.queries
    send_list=[]
    for query in query_list:
        if(query.type == "CARD SEARCH"):
            send_list.append(Send("card_finder", prompt) for prompt in query.queries)
        elif (query.type == "RULE SEARCH"):
            send_list.append(Send("rule_finder", prompt) for prompt in query.queries)
        # elif (query.type == "Q&A SEARCH"):
        #     send_list.append(Send("qea_finder", prompt) for prompt in query.queries)
    return send_list

def send_to_llm_with_tools(query, tools, system_prompt):
    agent = create_agent(
        model=llm_model,
        tools=tools,
        system_prompt=system_prompt
    )
    result = agent.invoke(query)
    return result

def qea_finder(query: str):
    pass

def final_response_builder(state: ReportState):
    pass

#Edges

builder = StateGraph(ReportState)

builder.add_node("build_first_query", build_first_query)
# builder.add_node("translate_input", translate_input)
builder.add_node("card_finder", card_finder)
builder.add_node("rule_finder", rule_finder)
builder.add_node("qea_finder", qea_finder)
builder.add_node("final_response_builder", final_response_builder)

builder.add_edge(START, "build_first_query")
builder.add_conditional_edges("build_first_query", spawn_researchers, ["card_finder", "rule_finder", "qea_finder"])
builder.add_edge("card_finder", "final_response_builder")
builder.add_edge("rule_finder", "final_response_builder")
builder.add_edge("qea_finder", "final_response_builder")
builder.add_edge("final_response_builder", END)

graph = builder.compile()


if __name__ == "__main__":
    # from IPython.display import Image, display
    # image = Image(graph.get_graph().draw_mermaid_png())
    # display(image)
    user_input = """
    Witch card has the effect "when attacking, draw 2 cards and trash 1", costs 4 and has the name cavendish?
    """
    # graph.invoke({"user_input": user_input})
    # data = {"user_input": user_input, "queries_results": []}
    # rs = ReportState(**data)
    # print(build_first_query(rs))
    print(card_finder(user_input))