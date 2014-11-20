# coding: utf-8
import datetime
from flask import render_template, Blueprint, flash, redirect, url_for, abort, request
from ..models import db, Blog, Post, ApprovementLog
from ..utils.permissions import AdminPermission
from ..forms import BlogForm

bp = Blueprint('admin', __name__)


@bp.route('/approve')
@AdminPermission()
def approve():
    logs = ApprovementLog.query.order_by(ApprovementLog.status.asc(),
                                         ApprovementLog.updated_at.desc())
    return render_template('admin/approve.html', logs=logs)


@bp.route('/approve_blog/<int:uid>', methods=['POST'])
@AdminPermission()
def approve_blog(uid):
    blog = Blog.query.get_or_404(uid)
    is_approved = True if 'yes' in request.form else False
    # 更新blog
    blog.is_approved = is_approved
    db.session.add(blog)
    # 更新log
    log = ApprovementLog.query.filter(ApprovementLog.blog_id == uid).first_or_404()
    log.updated_at = datetime.datetime.now()
    log.status = 1 if is_approved else 0
    log.message = request.form.get('message')
    db.session.add(log)
    db.session.commit()
    flash('操作成功')
    return redirect(request.referrer)


@bp.route('/edit_blog/<int:uid>', methods=['GET', 'POST'])
@AdminPermission()
def edit_blog(uid):
    blog = Blog.query.get_or_404(uid)
    form = BlogForm(obj=blog)
    if form.validate_on_submit():
        form.populate_obj(blog)
        db.session.add(blog)
        db.session.commit()
        flash('操作成功')
        return redirect(request.form.get('referer') or request.referrer)
    return render_template('admin/edit_blog.html', form=form)
