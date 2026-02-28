from docling.document_converter import DocumentConverter

source = "md/rule_comprehensive.md"
filename= source.split("/")[-1].replace(".md", "")

converter = DocumentConverter()
result = converter.convert(source)

with open(f"md/{filename}.md", "w", encoding="utf-8") as f:
    f.write(result.document.export)