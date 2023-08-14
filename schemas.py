from pydantic import BaseModel


class CursoBase(BaseModel):
    titulo: str
    descricao: str
    carga_horaria: int
    qtd_exercicios: int
    active: bool


class CursoRequest(CursoBase):
    ...


class CursoResponse(CursoBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True


class AlunoBase(BaseModel):
    nome: str
    sobrenome: str
    email: str
    idade: int
    cpf: int
    id_curso: int


class AlunoRequest(AlunoBase):
    ...


class AlunoResponse(AlunoBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
