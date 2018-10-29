from flask import Flask, Response, jsonify, request, render_template, redirect, flash, url_for, Session 
from flask_cors import CORS, cross_origin
from flask_security import SQLAlchemyUserDatastore, Security
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from controller.models import Users, Files
from functions.methods import *
import datetime, base64
import pandas as pd
import os


connection_string = 'mysql+pymysql://%s@%s:%s/%s' % (
            "root",
            "localhost",
            "3306",
            "prototype"
        )
app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = "what is a man a miserable pile of secrets"
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SECURITY_REGISTERABLE'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOWED_EXTENSIONS'] = set(['xls','xlsx','csv'])

compress = Compress(app)
COMPRESS_MIMETYPES = ['text/html','text/css','text/xml','application/json','application/javascript']
COMPRESS_LEVEL = 8
COMPRESS_CACHE_KEY = None
COMPRESS_CACHE_BACKEND = None

SESSION_TYPE = 'sqlalchemy'
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

cors = CORS(app)


@lm.user_loader
def load_user(id):
    return db.session.query(Users).filter_by(id=id).first()


#Routes

#-----------------------------------PAGINA DE CADASTRO-----------------------------------------------
@app.route("/create", methods=["GET","POST"])
@cross_origin()
def signUp():
    if (request.method=="POST"):
        user = Users(request.form["Name"],request.form["Email"],request.form["Senha"])
        query = db.session.query(Users).filter_by(email=user.email).first()
        if (query):
            flash("Usuário já cadastrado")
        else:
            db.session.add(user)
            db.session.commit()
            work_dir = os.getcwd()+r'/upload/'
            try:
                confirm = bd.session.query(Users).filter_by(email=user.email).first()
                os.mkdir(os.path.join(work_dir,confirm.id))
            except:
                print ('diretorio ja existe')   
            flash("Usuário cadastrado com sucesso")
    return render_template("cadastro.html")

#------------------------------------TELA INICIAL------------------------------------------------------
@app.route("/", methods=['GET','POST'])
@cross_origin()
def login():
    try:
        user = db.session.query(Users).filter_by(email=request.form['Email']).first()
        print (request)
        if (user and user.password==request.form['password']):
            try:
                rm = request.form['remember']
                login_user(user, remember=True)
            except:
                login_user(user, remember=False)
            return redirect(url_for('home'))
        else:
            flash("Credenciais inválidas")
            return render_template('login.html')
    except:
        return render_template('login.html') #trocar para a pagina inicial do usuario
    
#-----------------------------------ENCERRAR SESSÃO--------------------------------------------------
@app.route('/logout')
@login_required
@cross_origin()
def logOut():
    logout_user()
    return render_template('login.html')

#-----------------------------------HOME SCREEN DO USUARIO------------------------------------------
@app.route('/home')
@cross_origin()
@login_required
def home():
    user = db.session.query(Users).filter_by(id=current_user.get_id()).first()
    files = db.session.query(Files).filter_by(id_user=user.id).all()
    data = []
    for i in files:
        data.append(i.serialize())
    return render_template("main.html", user=user.name, data=data, action="true")

#-----------------------------------PAGINA DE UPLOAD-----------------------------------------------
@app.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    # return current_user.get_id()
    return render_template("upload.html", user=current_user.get_id())

#-----------------------------------UPLOAD E EXIBIÇÃO DE TABELAS-----------------------------------
@app.route("/result",  methods=['GET','POST'])
@login_required
def up():
    if (request.method == 'POST'):
        arquivo = request.files['file']
        files = Files(current_user.get_id(), arquivo.filename, arquivo.read(), datetime.date.today())
        pesos = [float(request.form['peso_1']),float(request.form['peso_2']),float(request.form['peso_3']),float(request.form['peso_4'])]

        try: # tenta adicionar informações ao banco
            db.session.add(files)
            db.session.commit()
        except:
            db.session.rollback()

        
        try: #with header
            check = request.form['header']
            if ((checkType(files.filename)=='.xls') or (checkType(files.filename)=='.xlsx')):
                dados=str(Processa_xls(arquivo, pesos, check))
            elif (checkType(arquivo.filename)=='.cvs'):
                dados=str(Processa_csv(arquivo, pesos, check))
        except: #without header
            if ((checkType(arquivo.filename)=='.xls') or (checkType(files.filename)=='.xlsx')):
                dados=dados=str(Processa_xls(arquivo, pesos, ''))
            else:
                dados=dados=str(Processa_xls(arquivo, pesos, ''))
            
                
        return render_template("result.html",dados=dados,user=current_user.get_id())

    return render_template('result.html')


#-----------------------------------REMOÇÃO DE ARQUIVOS--------------------------------------------------------------
@app.route('/remove')
@login_required
def remove():
    file = db.session.query(Files).filter_by(filename=request.args.get('file', type=str)).first()
    # return str(file.serialize())
    try:
        db.session.delete(file)
        db.session.commit()
        # os.chdir(os.getcwd, r'/upload/'+ current_user.get_id() +r'/')
        # os.remove(file.filename)
    except:
        db.session.rollback()
    return redirect(url_for('home'))
    

#----------------------------------------Visualizar Arquivos---------------------------------------------------------
@app.route('/view', methods=['get'])
@login_required
def view():
    os.chdir(os.getcwd()+r'/upload/'+current_user.get_id())
    arquivo = request.args.get('file',type=str)
    if (arquivo[-3:]=='csv'):
        dados = csvToJson(arquivo,'on')
    else:
        dados = xlsToJson(arquivo,'on')
    return render_template('result.html', dados=dados)

#--------------------------------------------------------------------------------------------------------------------
# @app.errorhandler(400)
# def erro400(error):
#     return render_template('erro400.html', user = current_user.get_id())


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0',debug=True, threaded=True)
