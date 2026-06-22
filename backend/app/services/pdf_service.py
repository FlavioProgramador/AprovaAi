import io
import logging
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

class PDFService:
    @staticmethod
    def extract_text(file_bytes: bytes) -> str:
        """
        Extrai o conteúdo de texto de um arquivo PDF recebido em bytes.
        Caso ocorra algum erro na extração ou o PDF não tenha texto extraível,
        retorna uma string vazia.
        """
        try:
            pdf_file = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_file)
            text_content = []
            
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
                    
            full_text = "\n".join(text_content).strip()
            logger.info(f"PDF carregado com sucesso. Total de páginas: {len(reader.pages)}. Caracteres extraídos: {len(full_text)}")
            return full_text
        except Exception as e:
            logger.error(f"Erro ao ler arquivo PDF: {str(e)}")
            return ""

pdf_service = PDFService()
