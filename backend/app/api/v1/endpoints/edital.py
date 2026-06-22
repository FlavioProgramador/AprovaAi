from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.pdf_service import pdf_service
from app.services.gemini_service import gemini_service
from app.schemas.edital import AnalysisResponse

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_edital(file: UploadFile = File(...)):
    """
    Recebe um edital em formato PDF, extrai seu texto e processa utilizando
    a inteligência artificial (Google Gemini) para gerar as estatísticas de estudo.
    """
    # Validação do tipo de arquivo
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo enviado precisa ser um PDF válido."
        )
    
    try:
        # Lendo os bytes do arquivo
        contents = await file.read()
        
        # Extraindo texto do PDF
        text = pdf_service.extract_text(contents)
        if not text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Não foi possível extrair nenhum texto legível do arquivo PDF."
            )
        
        # Analisando usando serviço da IA (Gemini)
        analysis_result = gemini_service.analyze_syllabus(text)
        return analysis_result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao processar o arquivo: {str(e)}"
        )

@router.get("/health")
def health_check():
    """
    Endpoint simples para monitorar a saúde da API.
    """
    return {
        "status": "online",
        "gemini_api_configured": gemini_service.is_configured
    }
