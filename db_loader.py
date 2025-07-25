import os.path
import shutil
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader

import responses
from responses import get_embeddings
import chromadb

class dbLoader:

    DATA_PATH = "data/QA"
    CHROMA_PATH = "chroma"
    CARD_DATA_PATH = "data/CardList/OP_TCG_CARD_LIST.csv"

    def load_documents(self, path, extension):
        loader = DirectoryLoader(path, glob="*." + extension)
        documents = loader.load()
        return documents

    def load_csv_documents(self, path):
        loader = CSVLoader(file_path="./data/CardList/OP_TCG_CARD_LIST.csv", encoding="UTF-8",
                           csv_args={
                               "delimiter": ",",
                               "quotechar": '"',
                               "fieldnames": ["URL","Effect","ID","Title","Price","Cost","Color","Types","Attributes","Rarity","Card Type","Power","Source","SET"]
                           }, source_column="ID", metadata_columns=["Source","SET","Price"]
                           )
        data = loader.load()
        return data

    def create_splitter(self):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=[
                r"\|[^\|]*\|[^\|]*\|[^\|]*\|[^\|]*\|"
            ],
            is_separator_regex=True,
            chunk_size=50,
            chunk_overlap=0
        )

        documents = self.load_documents(self.DATA_PATH, "md")
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chuncks")

        self.save_to_chroma(chunks,True)
        #self.read_car_list()

    def read_car_list(self):
        documents = self.load_csv_documents(self.CARD_DATA_PATH)
        self.save_to_chroma(documents,False, True)

    def save_to_chroma(self,chunks, clear, is_cards = False):
        if os.path.exists(self.CHROMA_PATH) & clear:
            shutil.rmtree(self.CHROMA_PATH)

        if is_cards:
            db = Chroma.from_documents(chunks, responses.get_embeddings(), persist_directory=self.CHROMA_PATH, collection_name="cardList")
        else:
            db = Chroma.from_documents(chunks, responses.get_embeddings(), persist_directory=self.CHROMA_PATH, collection_name="QeA")
        print(f"Saved {len(chunks)} chunks to {self.CHROMA_PATH}")

    def get_from_chroma(self, query):
        db_qa = Chroma(persist_directory=self.CHROMA_PATH, embedding_function=responses.get_embeddings(), collection_name="QeA")
        retsults_qa = db_qa.similarity_search_with_relevance_scores(query, k=5)

        out_text_qa = "\n\n---\n\n".join([doc.page_content for doc, _score in retsults_qa])
        out_metadata_qa = [doc.metadata.get("source", None) for doc, _score in retsults_qa]

        db_card = Chroma(persist_directory=self.CHROMA_PATH, embedding_function=responses.get_embeddings(),
                       collection_name="cardList")
        retsults_card = db_card.similarity_search_with_relevance_scores(query, k=10)

        out_text_card = "\n\n---\n\n".join([doc.page_content for doc, _score in retsults_card])
        out_metadata_card = [doc.metadata.get("source", None) for doc, _score in retsults_card]

        formated_sources = f"Sources: {out_metadata_qa} {out_metadata_card}"
        print(f"{out_text_qa}\n{out_text_card}\n{formated_sources}")
        return f"{out_text_qa}\n{out_text_card}\n{formated_sources}"

    '''
    #main entry point
    def main():
        create_splitter()
    
    if __name__ == '__main__':
        main()
    '''