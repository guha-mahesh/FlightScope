from dotenv import load_dotenv
import os
import sqlite3
import requests

load_dotenv()

api_key = os.getenv("api_key_ebird")


def get_common_name(scientific_name):
    print(scientific_name)
    problematic = ["Aratinga_acuticaudata", "Acanthis_hornemanni"]
    solutions = ['Blue-crowned parakeet', 'Hoary Redpoll']
    if scientific_name in problematic:
        return solutions[problematic.index(scientific_name)]

    scientific_name = scientific_name.replace("_", " ")

    url = f"https://api.ebird.org/v2/ref/taxonomy/ebird?species={scientific_name}"
    headers = {'X-eBirdApiToken': api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.text.split("\n")[1]

        common = data.split(",")

        return common[1]

    return None


def insertWeights(db):

    with open("species_poisson_results.csv", "r") as file:
        print("insertingWeights")

        cursor = db.cursor()
        file.readline()
        for line in file:

            data = line.split(",")
            species = get_common_name(data[0])
            weights = data[1:11]
            print(weights)
            for i in range(len(weights)):
                weights[i] = weights[i].replace("[", "")
                weights[i] = weights[i].replace('"', "")
            weightstring = ",".join(weights)

            try:
                cursor.execute("INSERT INTO birdWeights (species, weights) VALUES(?, ?)", [
                    species, weightstring])
            except Exception as e:
                print("error:", e)
        db.commit()
        cursor.close()
