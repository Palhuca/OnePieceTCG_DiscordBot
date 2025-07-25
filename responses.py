import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import agent


llm = ChatOpenAI(model='gpt-4o-mini-2024-07-18')
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large")

def translate_message(user_input: str) -> str:
    prompt_template = PromptTemplate.from_template(
        """Traduza a pergunta abaixo referente ao card game do One Piece para o ingles. Mantenha os nomes dos personagens e código das cartas.
        Mensagem: {msg}
        Answer: 
        """)

    chain = {"context": lambda q: user_input, "msg": RunnablePassthrough()} | prompt_template | llm | StrOutputParser()

    return chain.invoke(user_input)

'''
def get_resposes(user_input: str) -> str:

    prompt_withTCGContext = PromptTemplate.from_template(
        """You are a One Piece card game player assistant that helps players with rules, cards interaction questions, card identification and general card questions using the following context as a guide for the answer. You must analise the cards effects, the rules and the Q&A to answer. The answer must be in portugues and in a detailed way. Pay attention to the card numbers.
        Context: {context}
        Mensage: {msg}
        Answer: 
        """)

    loader = db_loader.dbLoader()
    chain = {"context": lambda q: loader.get_from_chroma(user_input), "msg": RunnablePassthrough()} | prompt_withTCGContext | llm | StrOutputParser()

    return chain.invoke(user_input)
'''
def get_message_agent(user_input: str) -> str:
    message = agent.run(llm, user_input)
    print(message)
    return message.get("output")

def get_message_agent_with_translation(user_input: str) -> str:

    prompt_template = PromptTemplate.from_template(
        """Traduza a pergunta abaixo referente ao card game do One Piece para o ingles. Mantenha os nomes dos personagens e código das cartas. A resposta deve conter somente o texto traduzido
        Mensagem a ser traduzida: {msg}
        Resposta:
        """)

    chain_translate = prompt_template | llm | StrOutputParser()

    full_chain = chain_translate | llm

    message = agent.run(llm, user_input,chain_translate)
    print(message)
    return message.get("output")

def get_embeddings():
    return embeddings
