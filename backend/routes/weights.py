from scipy.stats import poisson
from flask import Blueprint, jsonify, request, g
import requests
import sqlite3
import numpy as np
from datetime import date
import random

bird_bp = Blueprint("bird", __name__, url_prefix="/birds")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("database.db")
        g.db.row_factory = sqlite3.Row
    return g.db


@bird_bp.route("/weights/<id>", methods=["GET"])
def get_weights(id):
    db = get_db()
    cursor = db.cursor()
    if (id != '""'):
        try:
            id = int(id)
            cursor.execute("SELECT * FROM birdWeights WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                weights = row[2].split(",")
                response = {
                    "species": row[1],
                    "const": weights[0],
                    "lat": weights[1],
                    "long": weights[2],
                    "temp": weights[3],
                    "percipitation": weights[4],
                    "wind_speed": weights[5],
                    "solar_insolation": weights[6],
                    "clearness_index": weights[7],
                    "relative_humidity": weights[8],
                    "pressure": weights[9],
                }
                return jsonify(response)
            else:
                return jsonify({"error": "Species not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif (id == '""'):
        cursor.execute("SELECT * FROM birdWeights")
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        return jsonify(results)


@bird_bp.route('/species', methods=['GET'])
def getSpecies():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT species, id FROM birdWeights')
    rows = cursor.fetchall()
    if rows:
        results = [dict(row) for row in rows]
        return jsonify(results)
    else:
        return jsonify({"error": "No species found"}), 404


@bird_bp.route('/prediction', methods=["POST"])
def prediction():

    lat_factor = 90
    lng_factor = 180
    temp_factor = 50
    precip_factor = 100
    wind_factor = 50
    solar_factor = 1000
    clearness_factor = 1
    rh_factor = 100
    pressure_factor = 1200

    data = request.get_json()
    try:

        latitude = float(data.get("lat", 0))
        longitude = float(data.get("long", 0))
        const = float(data.get('const', 1))
        temp = float(data.get("temp", 20))
        precipitation = float(data.get("percipitation", 0))
        wind_speed = float(data.get("wind_speed", 0))
        solar_insolation = float(data.get("solar_insolation", 0))
        clearness_index = float(data.get("clearness_index", 0))
        relative_humidity = float(data.get("relative_humidity", 50))
        pressure = float(str(data.get("pressure", 101)).replace("]", ""))
        latWeight = float(data.get("latWeight", 0))
        lngWeight = float(data.get("lngWeight", 0))
        expected = float(data.get("expected", 1))

        scaled_features = [
            latitude / lat_factor,
            longitude / lng_factor,
            temp / temp_factor,
            precipitation / precip_factor,
            wind_speed / wind_factor,
            solar_insolation / solar_factor,
            clearness_index / clearness_factor,
            relative_humidity / rh_factor,
            pressure / pressure_factor
        ]

        weights = [const, latWeight, lngWeight, temp, precipitation, wind_speed,
                   solar_insolation, clearness_index, relative_humidity, pressure]

        features_with_const = [1.0] + scaled_features
        x = np.array(features_with_const)

        linear_pred = np.dot(weights, x)
        prediction = np.exp(linear_pred)

        if prediction <= 0:
            prediction = random.uniform(1, 5)

        k = int(expected)
        prob_at_least_k = 1 - poisson.cdf(k - 1, prediction)

        return jsonify({"prob_at_least_k": float(prob_at_least_k),
                        "fallback_value": float(prediction)})

    except Exception as e:
        fallback = random.uniform(1, 5)
        return jsonify({"prob_at_least_k": 0.5, "fallback_value": fallback})
