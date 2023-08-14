from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.openapi.utils import get_openapi
from models import Curso, Aluno
from database import engine, Base, get_db
from repositories import CursoRepository, AlunoRepository
from schemas import CursoRequest, CursoResponse, AlunoRequest, AlunoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/api/cursos", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def create(request: CursoRequest, db: Session = Depends(get_db)):
    curso = CursoRepository.save(db, Curso(**request.dict()))
    return CursoResponse.from_orm(curso)


@app.get("/api/cursos", response_model=list[CursoResponse])
def find_all(db: Session = Depends(get_db)):
    cursos = CursoRepository.find_all(db)
    return [CursoResponse.from_orm(curso) for curso in cursos]


@app.get("/api/cursos/{id}", response_model=list[CursoResponse])
def find_by_id(id: int, db: Session = Depends(get_db)):
    curso = CursoRepository.find_by_id(db, id)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso nao encontrado!")
    else:
        return [CursoResponse.from_orm(curso)]


@app.delete("/api/cursos/{id}", response_model=list[CursoResponse])
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if CursoRepository.exists_by_id(db, id) is False:
        raise HTTPException(status_code=404, detail="Curso nao encontrado!")
    else:
        CursoRepository.delete_by_id(db, id)
        raise HTTPException(status_code=204, detail="Curso deletado!")


@app.put("/api/cursos/{id}", response_model=list[CursoResponse])
def update_by_id(id: int, request: CursoRequest, db: Session = Depends(get_db)):
    if CursoRepository.exists_by_id(db, id) is False:
        raise HTTPException(status_code=404, detail="Curso nao encontrado!")
    else:
        curso = CursoRepository.save(db, Curso(id=id, **request.dict()))
        return [CursoResponse.from_orm(curso)]


@app.post("/api/alunos", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def create(request: AlunoRequest, db: Session = Depends(get_db)):
    if (CursoRepository.exists_by_id(db, request.id_curso) is True):
        aluno = AlunoRepository.save(db, Aluno(**request.dict()))
        return AlunoResponse.from_orm(aluno)
    else:
        raise HTTPException(
            status_code=404, detail="Id do curso nao encontrado!")


@app.get("/api/alunos", response_model=list[AlunoResponse])
def find_all(db: Session = Depends(get_db)):
    alunos = AlunoRepository.find_all(db)
    return [AlunoResponse.from_orm(aluno) for aluno in alunos]


@app.get("/api/alunos/{id}", response_model=list[AlunoResponse])
def find_by_id(id: int, db: Session = Depends(get_db)):
    aluno = AlunoRepository.find_by_id(db, id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado!")
    else:
        return [AlunoResponse.from_orm(aluno)]


@app.delete("/api/alunos/{id}", response_model=list[AlunoResponse])
def delete_by_id(id: int, db: Session = Depends(get_db)):
    aluno = AlunoRepository.find_by_id(db, id)
    idCurso = aluno.id_curso
    curso = CursoRepository.find_by_id(db, idCurso)
    ativo = curso.active
    if AlunoRepository.exists_by_id(db, id) is False:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado!")
    elif (ativo is True):
        raise HTTPException(
            status_code=404, detail="Nao foi possivel excluir o aluno, pois ele esta vinculado a um curso ativo")
    else:
        AlunoRepository.delete_by_id(db, id)
        raise HTTPException(status_code=204, detail="Aluno deletado!")


@app.put("/api/alunos/{id}", response_model=list[AlunoResponse])
def update_by_id(id: int, request: AlunoRequest, db: Session = Depends(get_db)):
    if AlunoRepository.exists_by_id(db, id) is False:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado!")
    else:
        aluno = AlunoRepository.save(db, Aluno(id=id, **request.dict()))
        return [AlunoResponse.from_orm(aluno)]


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Ambiente Virtual de Aprendizagem",
        version="1.0.0",
        summary="Alunos EAD",
        description="Sistema de Ambiente Virtual de Aprendizagem para auxiliar alunos 100% EAD",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
