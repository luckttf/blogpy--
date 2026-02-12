from flask import Flask, render_template, url_for
from fakepinterest import app
from fakepinterest.models import Usuario, Foto
from flask_login import login_required
from fakepinterest.forms import FormLogin, FormCriarConta

@app.route('/',  methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    return render_template('homepage.html', form=formlogin)

@app.route('/criar-conta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        usuario = Usuario(username=formcriarconta.username.data, email=formcriarconta.email.data
                          , senha=formcriarconta.senha.data)
    return render_template('criarconta.html', form=formcriarconta)

@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)
