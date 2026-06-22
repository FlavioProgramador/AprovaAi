import csv
import io
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.edital import Edital
from app.models.topic import Topic

router = APIRouter()

@router.get("/csv/{edital_id}")
def export_edital_csv(
    edital_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Exporta o plano de estudos de um edital em formato CSV estruturado.
    Utiliza utf-8-sig (BOM) para compatibilidade perfeita com o Microsoft Excel.
    """
    # Verifica se o edital pertence ao usuário
    edital = db.query(Edital).filter(
        Edital.id == edital_id,
        Edital.user_id == current_user.id
    ).first()
    
    if not edital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Edital não encontrado ou você não tem permissão para acessá-lo."
        )
        
    topics = db.query(Topic).filter(Topic.edital_id == edital.id).all()
    
    # Gerando o arquivo CSV em memória
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    
    # Cabeçalho do CSV
    writer.writerow([
        "ID do Tópico", 
        "Nome do Assunto", 
        "Peso/Prioridade", 
        "Relevância (%)", 
        "Recomendação de Estudo", 
        "Status de Progresso", 
        "Questões Resolvidas", 
        "Questões Corretas",
        "Aproveitamento (%)"
    ])
    
    status_mapping = {
        "to_study": "Não Iniciado",
        "studying": "Em Progresso",
        "completed": "Concluído"
    }
    
    for t in topics:
        aproveitamento = 0.0
        if t.questions_solved > 0:
            aproveitamento = round((t.questions_correct / t.questions_solved) * 100, 2)
            
        writer.writerow([
            t.id,
            t.name,
            t.weight,
            f"{t.relevance_percentage:.2f}%",
            t.study_recommendation,
            status_mapping.get(t.status, "Não Iniciado"),
            t.questions_solved,
            t.questions_correct,
            f"{aproveitamento}%"
        ])
        
    csv_data = output.getvalue().encode("utf-8-sig")
    output.close()
    
    return StreamingResponse(
        io.BytesIO(csv_data),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=plano_de_estudos_{edital_id}.csv"
        }
    )
