from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.edital import Edital
from app.models.topic import Topic
from app.models.session import StudySession
from app.services.pdf_service import pdf_service
from app.services.gemini_service import gemini_service
from app.schemas.edital import AnalysisResponse, TopicUpdate, SessionResponse, SessionCreate, TopicAnalysis, MetadataAnalysis
from typing import List

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_edital(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Recebe um edital em formato PDF, extrai seu texto, processa utilizando
    a inteligência artificial (Google Gemini) para gerar as estatísticas de estudo
    e salva o plano de estudos no banco de dados para o usuário autenticado.
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
        
        # Criando o Edital no banco de dados
        db_edital = Edital(
            user_id=current_user.id,
            filename=file.filename,
            file_size=len(contents),
            general_strategy=analysis_result.get("general_strategy", "")
        )
        db.add(db_edital)
        db.commit()
        db.refresh(db_edital)
        
        # Criando os Tópicos no banco de dados
        saved_topics = []
        for topic_data in analysis_result.get("topics", []):
            db_topic = Topic(
                edital_id=db_edital.id,
                name=topic_data.get("name"),
                weight=topic_data.get("weight"),
                relevance_percentage=topic_data.get("relevance_percentage"),
                study_recommendation=topic_data.get("study_recommendation"),
                status="to_study",
                questions_solved=0,
                questions_correct=0
            )
            db.add(db_topic)
            saved_topics.append(db_topic)
            
        db.commit()
        
        # Refresh para obter os IDs do banco de dados
        for t in saved_topics:
            db.refresh(t)
            
        # Montar a resposta incluindo os IDs gerados pelo banco
        response_topics = [
            TopicAnalysis(
                id=t.id,
                name=t.name,
                weight=t.weight,
                relevance_percentage=t.relevance_percentage,
                study_recommendation=t.study_recommendation,
                status=t.status,
                questions_solved=t.questions_solved,
                questions_correct=t.questions_correct
            )
            for t in saved_topics
        ]
        
        return AnalysisResponse(
            metadata=MetadataAnalysis(
                edital_id=db_edital.id,
                extracted_topics_count=len(response_topics),
                status=analysis_result.get("metadata", {}).get("status", "Sucesso")
            ),
            topics=response_topics,
            general_strategy=db_edital.general_strategy
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao processar o arquivo: {str(e)}"
        )

@router.get("/latest", response_model=AnalysisResponse)
def get_latest_edital(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Recupera o plano de estudos do último edital processado pelo usuário autenticado.
    """
    db_edital = db.query(Edital).filter(Edital.user_id == current_user.id).order_by(Edital.created_at.desc()).first()
    if not db_edital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum plano de estudos de edital encontrado para este usuário. Por favor, envie um edital."
        )
    
    db_topics = db.query(Topic).filter(Topic.edital_id == db_edital.id).all()
    
    response_topics = [
        TopicAnalysis(
            id=t.id,
            name=t.name,
            weight=t.weight,
            relevance_percentage=t.relevance_percentage,
            study_recommendation=t.study_recommendation,
            status=t.status,
            questions_solved=t.questions_solved,
            questions_correct=t.questions_correct
        )
        for t in db_topics
    ]
    
    return AnalysisResponse(
        metadata=MetadataAnalysis(
            edital_id=db_edital.id,
            extracted_topics_count=len(response_topics),
            status="Sucesso"
        ),
        topics=response_topics,
        general_strategy=db_edital.general_strategy or ""
    )

@router.put("/topics/{topic_id}", response_model=TopicAnalysis)
def update_topic_progress(
    topic_id: int,
    topic_update: TopicUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza o progresso de um tópico de estudo (status e contagem de questões).
    """
    topic = db.query(Topic).join(Edital).filter(
        Topic.id == topic_id,
        Edital.user_id == current_user.id
    ).first()
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tópico não encontrado ou você não tem permissão para alterá-lo."
        )
        
    topic.status = topic_update.status
    topic.questions_solved = topic_update.questions_solved
    topic.questions_correct = topic_update.questions_correct
    
    db.commit()
    db.refresh(topic)
    return topic

@router.post("/topics/{topic_id}/session", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_study_session(
    topic_id: int,
    session_in: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Registra uma sessão de estudo (ex: ciclo do Pomodoro finalizado) vinculada a um tópico.
    """
    # Valida se o tópico pertence ao usuário
    topic = db.query(Topic).join(Edital).filter(
        Topic.id == topic_id,
        Edital.user_id == current_user.id
    ).first()
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tópico não encontrado ou você não tem permissão para esta operação."
        )
        
    db_session = StudySession(
        user_id=current_user.id,
        topic_id=topic_id,
        duration_minutes=session_in.duration_minutes
    )
    db.add(db_session)
    
    # Se o status do tópico era 'to_study', ao registrar uma sessão ele muda para 'studying'
    if topic.status == "to_study":
        topic.status = "studying"
        
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/sessions", response_model=List[SessionResponse])
def list_study_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna a lista de todas as sessões de estudo registradas pelo usuário autenticado.
    """
    sessions = db.query(StudySession).filter(StudySession.user_id == current_user.id).order_by(StudySession.created_at.desc()).all()
    return sessions

@router.get("/health")
def health_check():
    """
    Endpoint simples para monitorar a saúde da API.
    """
    return {
        "status": "online",
        "gemini_api_configured": gemini_service.is_configured
    }
