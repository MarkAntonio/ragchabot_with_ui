from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    AcceleratorOptions,
    PdfPipelineOptions,
)
from pathlib import Path


pipeline_options = PdfPipelineOptions()
# pipeline_options.accelerator_options = accelerator_options
pipeline_options.do_ocr = False
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True

FILE_PATH = "C:/Users/marco/OneDrive/Uast/2024.2/TAIA - Tópicos Avançados em IA [Optativa]/ProjetoRAG/rag_chatbot_ui/base_docs/1.MANUAL DO ESTUDANTE_OCR_Converted.pdf"
EXPORT_TYPE = ExportType.MARKDOWN

loader = DoclingLoader(
    file_path=FILE_PATH,
    export_type=EXPORT_TYPE,
    converter = DocumentConverter(
      format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
        )
      }
    )
)

docs_manual = loader.load()


# salvar o arquivo
caminho_arquivo = Path('manual_do_estudante.md')

# Criando e abrindo o arquivo para escrita
with open(caminho_arquivo, 'w') as arquivo:
    arquivo.write(docs_manual[0].page_content)
