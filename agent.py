# from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools.psql_search import card_search, rules_search
from tools.chroma_search import get_from_chroma_qa, get_from_chroma_rule, get_from_chroma_card
from prompt_template import get_prompt_template, get_new_prompt_template
from langchain_core.runnables import RunnablePassthrough

def run(llm, user_input, translate_chain):

    #prompt_template = hub.pull("hwchase17/react")

    print('is going to run')

    prompt_template = get_new_prompt_template()

    print(prompt_template)

    tools = [card_search, get_from_chroma_qa, get_from_chroma_rule, get_from_chroma_card, rules_search]
    agent = create_tool_calling_agent(llm, tools, prompt_template)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    seq_chain = translate_chain | {'input': RunnablePassthrough()} | agent_executor

    print('agent Execution')

    return seq_chain.invoke(user_input)

    #return agent_executor.invoke({"input": user_input})