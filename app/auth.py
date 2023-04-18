import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import Member, db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        member = Member.query.filter_by(email=email).first()

        if member is None:
            error = 'Email incorreto.'
        elif not check_password_hash(member.password, password):
            error = 'Senha incorreta.'

        if error is None:
            session.clear()
            session['member_id'] = member.id

            return redirect(url_for('index'))

        flash(error)

    if g.member:
        return redirect(url_for('index'))

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_member():
    member_id = session.get('member_id')

    if member_id is None:
        g.member = None
    else:
        g.member = db.session.query(
            Member.id, Member.name, Member.is_admin).filter_by(id=member_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.member is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def only_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.member.is_admin:
            return redirect(url_for('main.index'))

        return view(**kwargs)

    return wrapped_view
