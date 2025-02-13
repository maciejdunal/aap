from flask import Blueprint, render_template, request
from app.models import Watch

main = Blueprint('main', __name__)

@main.route('/')
def index():
    category = request.args.get('category', 'all')
    search_query = request.args.get('search', '').strip().lower()

    # Filtrowanie według kategorii
    if category == 'all':
        watches = Watch.query
    elif category == 'men':
        watches = Watch.query.filter_by(sex='male')
    elif category == 'women':
        watches = Watch.query.filter_by(sex='female')
    elif category == 'luxury':
        watches = Watch.query.filter_by(category='luxury')
    elif category == 'sport':
        watches = Watch.query.filter_by(category='sport')
    else:
        watches = Watch.query

    # Dodanie wyszukiwania do zapytania
    if search_query:
        watches = watches.filter(Watch.brand.ilike(f'%{search_query}%'))

    # Pobranie wyników jako lista
    watches = watches.all()

    return render_template('index.html', watches=watches)
