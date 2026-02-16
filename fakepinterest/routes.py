from flask import Flask, render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta

@app.route('/',  methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario:
            bcrypt.check_password_hash(usuario.senha, formlogin.senha.data)
            login_user(usuario)
            return redirect(url_for('perfil', usuario=usuario.username))
    return render_template('homepage.html', form=formlogin)

@app.route('/criar-conta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, email=formcriarconta.email.data
                          , senha=senha)
        
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('perfil', usuario=usuario.username))
        print(formcriarconta.errors)
    return render_template('criarconta.html', form=formcriarconta)

@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))