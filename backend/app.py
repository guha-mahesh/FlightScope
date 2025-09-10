from flask import Flask, g, jsonify
from flask_cors import CORS
import sqlite3

from routes.weights import bird_bp
from insertWeights import insertWeights

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": ["http://localhost:5173", "http://127.0.0.1:5173"]
}})

app.register_blueprint(bird_bp)

DATABASE = "database.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS birdWeights ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "species VARCHAR(20) NOT NULL, "
        "weights VARCHAR(80))"
    )
    cursor.execute("DELETE FROM birdWeights;")

    conn.commit()


@app.route("/health", methods=["GET"])
def health():
    return "healthy"


if __name__ == "__main__":
    with app.app_context():
        db = get_db()
        insertWeights(db)
    app.run(debug=True, host="0.0.0.0", port=5000)
