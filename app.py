from flask import Flask, render_template
from controllers.user_controller import user_blueprint
from controllers.episode_controller import episode_blueprint
from controllers.genre_controller import genre_blueprint

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(episode_blueprint, url_prefix='/episodes')
app.register_blueprint(genre_blueprint, url_prefix='/genres')


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
