import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        member = db.execute(
            "SELECT * FROM member WHERE email = ?", (email,)
        ).fetchone()

        if member is None:
            error = 'Email incorreto.'
        elif not check_password_hash(member['password'], password):
            error = 'Senha incorreta.'

        if error is None:
            session.clear()
            session['member_id'] = member['id']

            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_member():
    member_id = session.get('member_id')

    if member_id is None:
        g.member = None
    else:
        g.member = get_db().execute(
            'SELECT * FROM member WHERE id = ?', (member_id,)
        ).fetchone()


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
