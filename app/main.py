from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    member = db.execute(
        'SELECT name'
        ' FROM member'
        ' WHERE id = ?', (g.member['id'],)
    ).fetchone()

    return render_template('main/index.html', member=member)


@bp.route('/password', methods=('GET', 'POST'))
def password():
    return render_template('main/password.html')


@bp.route('/members', methods=('GET', 'POST'))
def members():
    return render_template('main/members.html')


@bp.route('/member', methods=('GET', 'POST'))
def member():
    return render_template('main/member.html')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('main/create.html')


@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    return render_template('main/edit.html')
