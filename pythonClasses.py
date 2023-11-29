from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class AreaFormacao(Enum):
    INFORMATICA = 'Informática'
    ELETROELETRONICA = 'Eletroeletrônica'
    AGROPECUARIA = 'Agropecuária'

class StatusEstagio(Enum):
    INATIVO = 'Inativo'
    ATIVO = 'Ativo'
    CONCLUIDO = 'Concluído'
    REPROVADO = 'Reprovado'

class UserType(Enum):
    ALUNO = 'Aluno'
    ORIENTADOR = 'Orientador'
    SUPERVISOR = 'Supervisor'
    ADMIN = 'Admin'
    AVALIADOR = 'Avaliador'

class CustomUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    data_criacao = db.Column(db.DateTime, default=timezone.now)

    is_active = db.Column(db.Boolean, default=True)
    is_staff = db.Column(db.Boolean, default=False)

    matricula = db.Column(db.String(20), nullable=True)
    fase = db.Column(db.String(20), nullable=True)
    area_formacao = db.Column(db.String(20), nullable=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=True)
    user_type = db.Column(db.String(20), default=UserType.ALUNO.value)

    groups = db.relationship('Group', secondary='customuser_group', backref=db.backref('customusers', lazy='dynamic'))
    user_permissions = db.relationship('Permission', secondary='customuser_permission', backref=db.backref('customusers', lazy='dynamic'))

    def __repr__(self):
        return f"CustomUser('{self.email}')"

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False)
    nota = db.Column(db.Float, default=0.0)

class Estagio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('custom_user.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('custom_user.id'), nullable=False)
    orientador_id = db.Column(db.Integer, db.ForeignKey('custom_user.id'), nullable=False)
    avaliador_id = db.Column(db.Integer, db.ForeignKey('custom_user.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_final = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    
class Banca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('custom_user.id'), nullable=False)
    orientador_id = db.Column(db.Integer, db.ForeignKey('custom_user.id'), nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('custom_user.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)

class Ata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('custom_user.id'), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)

class Relatorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('custom_user.id'), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)

class Avaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('custom_user.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
    nota = db.Column(db.Float, nullable=False)
    comentario = db.Column(db.Text, nullable=False)

class Vaga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    requisitos = db.Column(db.Text, nullable=False)
    area_formacao = db.Column(db.String(20), nullable=False)
    remunerada = db.Column(db.Boolean, default=False)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)