from app import db
from app.errors import bp
from flask import render_template

@bp.errorhandler(404)
def page_404(error):
    return render_template("404.html")

@bp.errorhandler(500)
def page_500(error):
    db.session.rollback()
    return render_template("500.html")

