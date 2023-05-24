from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)

from app.auth import login_required, only_admin
from app.models import Announcement, Member, db

bp = Blueprint('announcements', __name__, url_prefix='/announcements')


@bp.route('/')
@login_required
def announcements():
    announcements = db.session.query(Announcement).order_by(
        Announcement.created_at.desc()).all()

    return render_template('announcements/index.html', announcements=announcements)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
@only_admin
def create():
    if request.method == 'POST':
        error = None

        title = request.form['title']
        description = request.form['description']

        if not title:
            error = 'O título é obrigatório.'
        if not description:
            error = 'A descrição é obrigatória'

        if error is not None:
            flash(error)
        else:
            new_announcement = Announcement(
                title=title, description=description, author_id=g.member.id)
            db.session.add(new_announcement)
            db.session.commit()

            return redirect(url_for('announcements.announcement', id=new_announcement.id))

    return render_template('announcements/create.html')


@bp.route('/<int:id>')
@login_required
def announcement(id):

    announcement = db.session.query(Announcement.id, Announcement.title, Announcement.description, Announcement.created_at, Member.name.label('member_name')).filter_by(id=id).join(
        Member, Member.id == Announcement.author_id, isouter=True).first()

    if announcement is None:
        abort(404)

    return render_template('announcements/announcement.html', announcement=announcement)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
@only_admin
def edit(id):
    announcement = Announcement.query.filter_by(id=id).first()

    if request.method == 'POST':
        error = None

        title = request.form['title']
        description = request.form['description']

        if not title:
            error = 'O título é obrigatório.'
        if not description:
            error = 'A descrição é obrigatória'

        if error is not None:
            flash(error)
        else:
            announcement.title = title
            announcement.description = description

            db.session.commit()

            return redirect(url_for('announcements.announcement', id=id))

    return render_template('announcements/edit.html', announcement=announcement)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
@only_admin
def delete(id):
    announcement = Announcement.query.filter_by(id=id).first()
    db.session.delete(announcement)
    db.session.commit()

    flash('Comunicado apagado com sucesso!')

    return redirect(url_for('announcements.announcements'))
