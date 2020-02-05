from app import db,app
from flask import render_template

@app.errorhandler(404)
def page_404(error):
    return render_template("404.html")

@app.errorhandler(500)
def page_500(error):
    db.session.rollback()
    return render_template("500.html")

