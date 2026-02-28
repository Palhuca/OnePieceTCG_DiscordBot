from docling.document_converter import DocumentConverter, PdfFormatOption
import pandas as pd
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableStructureOptions, TableFormerMode
from docling.datamodel.base_models import InputFormat

pipeline_options = PdfPipelineOptions(do_table_structure=True)
pipeline_options.table_structure_options.do_cell_matching = True
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
pipeline_options.do_ocr = False

source = "pdf/rule_comprehensive.pdf"
filename= source.split("/")[-1].replace(".pdf", "")

# converter = DocumentConverter(format_options={
#         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
#     })
converter = DocumentConverter()
result = converter.convert(source)

with open(f"md/{filename}.md", "w", encoding="utf-8") as f:
    f.write(result.document.export_to_markdown())