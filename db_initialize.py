import os.path
import shutil
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from responses import get_embeddings


def load_documents(path, extension):
    loader = DirectoryLoader(path, glob="*." + extension)
    documents = loader.load()
    return documents


def load_csv_documents(path):
    loader = CSVLoader(file_path="./data/CardList/OP_TCG_CARD_LIST.csv", encoding="UTF-8",
                       csv_args={
                           "delimiter": ",",
                           "quotechar": '"',
                           "fieldnames": ["URL", "Effect", "ID", "Title", "Price", "Cost", "Color", "Types",
                                          "Attributes", "Rarity", "Card Type", "Power", "Source", "SET"]
                       }, source_column="ID", metadata_columns=["Source", "SET", "Price"]
                       )
    data = loader.load()
    return data


class Db_Loader:
    QA_DATA_PATH = "data/QA"
    CHROMA_PATH = "chroma"
    RULES_DATA_PATH = "data/Rules"
    CARD_DATA_PATH = "data/CardList/OP_TCG_CARD_LIST.csv"


    def start_chroma_db(self):
        if os.path.exists(self.CHROMA_PATH):
            return
        else:
            self.process_qa()
            self.process_rules()
            self.process_cards()

    def clean_chroma_db(self):
        if os.path.exists(self.CHROMA_PATH):
            shutil.rmtree(self.CHROMA_PATH)

    def process_qa(self):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=[
                r"\|[^\|]*\|[^\|]*\|[^\|]*\|[^\|]*\|"
            ],
            is_separator_regex=True,
            chunk_size=50,
            chunk_overlap=0
        )

        documents = load_documents(self.QA_DATA_PATH, "md")
        chunks = text_splitter.split_documents(documents)
        print(f"QA - Split {len(documents)} documents into {len(chunks)} chuncks")

        self.save_to_chroma(chunks, "QA")

    def process_rules(self):

        text_splitter = RecursiveCharacterTextSplitter(
            separators=[
                "\n\n",
                "\n",
            ],
            is_separator_regex=False,
            chunk_size=20,
            chunk_overlap=0
        )

        documents = load_documents(self.RULES_DATA_PATH, "md")
        chunks = text_splitter.split_documents(documents)
        #chunks = text_splitter.split_documents(documents)
        print(f"Rules - Split {len(documents)} documents into {len(chunks)} chuncks")
        print(chunks[2])



        self.save_to_chroma(chunks, "RULES")

    def save_to_chroma(self, chunks, collection):


        if collection == "RULES":
            db = Chroma.from_documents(chunks, get_embeddings(), persist_directory=self.CHROMA_PATH,
                                       collection_name="Rules")
        elif collection == "QA":
            db = Chroma.from_documents(chunks, get_embeddings(), persist_directory=self.CHROMA_PATH,
                                       collection_name="QeA")
        else:
            db = Chroma.from_documents(chunks, get_embeddings(), persist_directory=self.CHROMA_PATH,
                                       collection_name="Cards")
        print(f"Saved {len(chunks)} chunks to {self.CHROMA_PATH}")

    def process_cards(self):
        documents = load_csv_documents(self.CARD_DATA_PATH)
        self.save_to_chroma(documents,"CARDS")