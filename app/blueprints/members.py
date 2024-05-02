from datetime import datetime

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from app.blueprints.auth import login_required, only_admin
from app.models import Member, db

bp = Blueprint('members', __name__, url_prefix='/members')


@bp.route('/')
@login_required
@only_admin
def members():
    members = db.session.query(Member.id, Member.name, Member.created_at).order_by(
        Member.created_at.desc()).all()

    return render_template('members/index.html', members=members)


@bp.route('/<int:id>')
@login_required
def member(id):
    if not g.member.is_admin and g.member.id != id:
        return redirect(url_for('main.index'))

    member = Member.query.filter_by(id=id).first()

    if member is None:
        abort(404)

    return render_template('members/member.html', member=member)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
@only_admin
def create():
    new_member = None

    if request.method == 'POST':
        error = None

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        rg = request.form['rg']
        cpf = request.form['cpf']
        birth = datetime.strptime(
            request.form['birth'], '%Y-%m-%d') if request.form['birth'] else None
        is_admin = int(request.form['admin'])
        address = request.form['address']

        if not name:
            error = 'O nome é obrigatório.'
        if not email:
            error = 'O email é obrigatório'
        if not password:
            error = 'A senha é obrigatória.'
        if password != password_repeat:
            error = 'Os campos nova senha e confirmar senha precisam ser iguais.'

        email_already_exists = Member.query.filter_by(email=email).first()

        if email_already_exists:
            error = 'Email já cadastrado.'

        if error is not None:
            flash(error)
        else:
            new_member = Member(name=name, email=email, password=generate_password_hash(
                password), rg=rg, cpf=cpf, birth=birth, is_admin=is_admin, address=address)
            db.session.add(new_member)
            db.session.commit()

            return redirect(url_for('members.member', id=new_member.id))

    return render_template('members/create.html', member=new_member)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    if not g.member.is_admin and g.member.id != id:
        return redirect(url_for('main.index'))

    member = Member.query.filter_by(id=id).first()

    if member is None:
        abort(404)

    if request.method == 'POST':
        error = None

        name = request.form['name']
        email = request.form['email']
        rg = request.form['rg']
        cpf = request.form['cpf']
        birth = datetime.strptime(
            request.form['birth'], '%Y-%m-%d') if request.form['birth'] else None
        is_admin = int(request.form['admin'])
        address = request.form['address']

        if not name:
            error = 'O nome é obrigatório.'
        if not email:
            error = 'O email é obrigatório'

        if error is not None:
            flash(error)
        else:
            member.name = name
            member.email = email
            member.rg = rg
            member.cpf = cpf
            member.birth = birth
            member.is_admin = is_admin
            member.address = address

            db.session.commit()

            return redirect(url_for('members.member', id=id))

    return render_template('members/edit.html', member=member)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    member = Member.query.filter_by(id=id).first()
    db.session.delete(member)
    db.session.commit()

    flash('"{}" foi apagado com sucesso!'.format(member.name))

    return redirect(url_for('members.members'))


@bp.route('/<int:id>/password', methods=('GET', 'POST'))
@login_required
def password(id):
    if not g.member.is_admin and g.member.id != id:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        error = None

        member = Member.query.filter_by(id=id).first()

        current_password = request.form['password']
        new_password = request.form['new_password']
        new_password_repeat = request.form['new_password_repeat']

        if not check_password_hash(member.password, current_password):
            error = 'Senha atual incorreta.'
        elif new_password != new_password_repeat:
            error = 'Os campos nova senha e confirmar nova senha precisam ser iguais.'

        if error is not None:
            flash(error)
        else:
            member.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Senha alterada com sucesso!')

            return redirect(url_for('members.member', id=member.id))

    return render_template('members/password.html')
