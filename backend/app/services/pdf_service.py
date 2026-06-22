import io
import logging
import pdfplumber

logger = logging.getLogger(__name__)

class PDFService:
    @staticmethod
    def extract_text(file_bytes: bytes) -> str:
        """
        Extrai o conteúdo de texto de um arquivo PDF recebido em bytes usando pdfplumber.
        Caso ocorra algum erro na extração ou o PDF não tenha texto extraível,
        retorna uma string vazia.
        """
        try:
            pdf_file = io.BytesIO(file_bytes)
            text_content = []
            
            with pdfplumber.open(pdf_file) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                        
            full_text = "\n".join(text_content).strip()
            logger.info(f"PDF carregado com sucesso usando pdfplumber. Total de páginas: {len(pdf.pages)}. Caracteres extraídos: {len(full_text)}")
            return full_text
        except Exception as e:
            logger.error(f"Erro ao ler arquivo PDF com pdfplumber: {str(e)}")
            return ""

pdf_service = PDFService()
