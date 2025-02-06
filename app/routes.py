from flask import Blueprint, render_template
from .models import Watch

main = Blueprint('main', __name__)

@main.route('/')
def index():
    watches = Watch.query.all()
    return render_template('index.html', watches=watches)
