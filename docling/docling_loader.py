from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType

from docling.chunking import HybridChunker

source = "pdf/rule_comprehensive.pdf"
filename= source.split("/")[-1].replace(".pdf", "")

loader = DoclingLoader(
    file_path=source,
    export_type=ExportType.DOC_CHUNKS,
    chunker=HybridChunker(tokenizer="sentence-transformers/all-MiniLM-L6-v2"),
)

docs = loader.load()
print (f"Loaded {len(docs)} document chunks from {source}")
print(docs[0].page_content[0])