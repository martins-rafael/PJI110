from datetime import datetime

from flask import Blueprint, g, render_template
from sqlalchemy import extract

from app.blueprints.auth import login_required
from app.models import Member, db

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    if g.member.is_admin:
        members = db.session.query(Member)
        total_members = members.count()
        last_members_created = members.order_by(Member.id.desc()).limit(3)
        birthdays = members.filter(extract(
            'month', Member.birth) == datetime.today().month).count()

        data = [total_members, last_members_created, birthdays]

        return render_template('main/index.html', data=data)
    else:
        return render_template('main/index.html')
