from app import create_app
from app.recommender.collaborative import build_recommendation_model
from app.recommender.content_based import build_content_model

app = create_app()

with app.app_context():
    build_recommendation_model()
    build_content_model()

if __name__ == "__main__":
    app.run(debug=True)
