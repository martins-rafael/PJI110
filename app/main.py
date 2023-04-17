import datetime

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from app.auth import login_required, only_admin
from app.db import get_db

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()

    total_members = db.execute(
        'SELECT COUNT(*) FROM member '
    ).fetchone()

    last_members_created = db.execute(
        'SELECT * FROM member ORDER BY id DESC LIMIT 3'
    ).fetchall()

    data = [total_members, last_members_created]

    return render_template('main/index.html', data=data)


@bp.route('/<int:id>/password', methods=('GET', 'POST'))
@login_required
def password(id):
    if not g.member['is_admin'] and g.member['id'] != id:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        db = get_db()
        error = None

        member = db.execute(
            "SELECT password FROM member WHERE id = ?", (id,)
        ).fetchone()

        current_password = request.form['password']
        new_password = request.form['new_password']
        new_password_repeat = request.form['new_password_repeat']

        if not check_password_hash(member['password'], current_password):
            error = 'Senha atual incorreta.'
        elif new_password != new_password_repeat:
            error = 'Os campos nova senha e confirmar nova senha precisam ser iguais.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                "UPDATE member SET password = ?"
                " WHERE id = ?",
                (generate_password_hash(new_password), id)
            )
            db.commit()

            return redirect(url_for('main.index'))

    return render_template('main/password.html')


@bp.route('/members', methods=('GET', 'POST'))
@login_required
@only_admin
def members():
    db = get_db()
    members = db.execute(
        'SELECT id, name, created_at FROM member ORDER BY created_at DESC'
    ).fetchall()

    return render_template('main/members.html', members=members)


@bp.route('/<int:id>')
@login_required
def member(id):
    if not g.member['is_admin'] and g.member['id'] != id:
        return redirect(url_for('main.index'))

    db = get_db()
    member = db.execute(
        "SELECT * FROM member WHERE id = ?", (id,)
    ).fetchone()

    if member is None:
        abort(404)

    return render_template('main/member.html', member=member)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
@only_admin
def create():
    if request.method == 'POST':
        db = get_db()
        error = None

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        rg = request.form['rg']
        cpf = request.form['cpf']
        birth = datetime.datetime.strptime(
            request.form['birth'], '%Y-%m-%d') if request.form['birth'] else None
        is_admin = request.form['admin']
        address = request.form['address']

        if not name:
            error = 'O nome é obrigatório.'
        if not email:
            'O email é obrigatório'
        if not password:
            'A senha é obrigatória.'
        if password != password_repeat:
            error = 'Os campos nova senha e confirmar senha precisam ser iguais.'

        email_already_exists = db.execute(
            'SELECT email FROM member WHERE email = ?', (email,)
        ).fetchone()

        if email_already_exists:
            error = 'Email já cadastrado.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO member (name, email, password, rg, cpf, address, birth, is_admin)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (name, email, generate_password_hash(
                    password), rg, cpf, address, birth, is_admin)
            )
            db.commit()
            return redirect(url_for('main.members'))

    return render_template('main/create.html')


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    if not g.member['is_admin'] and g.member['id'] != id:
        return redirect(url_for('main.index'))

    db = get_db()
    member = db.execute(
        "SELECT * FROM member WHERE id = ?", (id,)
    ).fetchone()

    if request.method == 'POST':
        error = None

        name = request.form['name']
        email = request.form['email']
        rg = request.form['rg']
        cpf = request.form['cpf']
        birth = datetime.datetime.strptime(
            request.form['birth'], '%Y-%m-%d') if request.form['birth'] else None
        is_admin = request.form['admin']
        address = request.form['address']

        if not name:
            error = 'O nome é obrigatório.'
        if not email:
            'O email é obrigatório'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE member SET name = ?, email = ?, rg = ?, cpf = ?, address = ?, birth = ?, is_admin = ?'
                ' WHERE id = ?',
                (name, email, rg, cpf, address, birth, is_admin, id)
            )
            db.commit()
            return redirect(url_for('main.member', id=id))

    return render_template('main/edit.html', member=member)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM member WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('main.members'))
