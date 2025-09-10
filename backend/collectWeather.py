import requests
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import time
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import random

directory = './species_csvs'
min_rows = 2000
num_files = 150

load_dotenv()

all_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
valid_files = []


for f in all_files:
    path = os.path.join(directory, f)
    try:
        df = pd.read_csv(path)
        if len(df) >= min_rows:
            valid_files.append(f)
    except Exception as e:
        print(f"Skipping {f} during validation: {e}")

files_to_process = random.sample(valid_files, min(num_files, len(valid_files)))


output_file = "species_poisson_results.csv"
if not os.path.exists(output_file):
    pd.DataFrame(columns=["species", "weights", "aic"]
                 ).to_csv(output_file, index=False)

for filename in files_to_process:
    path = os.path.join(directory, filename)
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"Failed to read {filename}: {e}")
        continue

    try:
        df = df.dropna(subset=['eventDate', 'decimalLatitude',
                       'decimalLongitude', 'individualCount'])
        if len(df) < 2000:
            print(f"{filename} has fewer than 2000 rows after dropping NA, skipping")
            continue

        df = df.sample(n=min(2500, len(df)),
                       random_state=42).reset_index(drop=True)
        print(df['individualCount'].mean())

        for index, row in df.iterrows():
            date_key = row["eventDate"].replace("-", "")
            url = "https://power.larc.nasa.gov/api/temporal/daily/point"
            params = {
                "latitude": row["decimalLatitude"],
                "longitude": row["decimalLongitude"],
                "start": date_key,
                "end": date_key,
                "parameters": "T2M,PRECTOTCORR,WS10M_MAX,ALLSKY_SFC_SW_DWN,ALLSKY_KT,RH2M,PS",
                "community": "AG",
                "format": "JSON"
            }
            try:
                response = requests.get(url, params=params, timeout=(30, 30))
                data = response.json()
                df.at[index, "temperature"] = data["properties"]["parameter"]["T2M"][date_key]
                df.at[index, "precipitation"] = data["properties"]["parameter"]["PRECTOTCORR"][date_key]
                df.at[index, "wind_speed"] = data["properties"]["parameter"]["WS10M_MAX"][date_key]
                df.at[index, "solar_insolation"] = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"][date_key]
                df.at[index, "clearness_index"] = data["properties"]["parameter"]["ALLSKY_KT"][date_key]
                df.at[index, "relative_humidity"] = data["properties"]["parameter"]["RH2M"][date_key]
                df.at[index, "pressure"] = data["properties"]["parameter"]["PS"][date_key]
            except Exception as e:
                print(f"NASA API error for {filename}, row {index}: {e}")
                df.at[index, ["temperature", "precipitation", "wind_speed",
                              "solar_insolation", "clearness_index", "relative_humidity", "pressure"]] = 0
            if index % 10 == 0:
                print(f"{filename} index {index}")
        df.fillna(0, inplace=True)

        feature_cols = ["decimalLatitude", "decimalLongitude", "temperature", "precipitation",
                        "wind_speed", "solar_insolation", "clearness_index", "relative_humidity", "pressure"]
        X = df[feature_cols]
        y = df["individualCount"]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled = sm.add_constant(X_scaled)

        poisson_model = sm.GLM(y, X_scaled, family=sm.families.Poisson())
        poisson_results = poisson_model.fit()

        result_dict = {
            "species": filename.replace('.csv', ''),
            "weights": list(poisson_results.params),
            "aic": poisson_results.aic
        }
        y_pred = poisson_results.predict(X_scaled)
        mae = mean_absolute_error(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))

        result_dict["MAE"] = mae
        result_dict["RMSE"] = rmse
        pd.DataFrame([result_dict]).to_csv(
            output_file, mode='a', header=False, index=False)
        print(f"Finished {filename} with AIC {poisson_results.aic:.2f}")

        time.sleep(5)

    except Exception as e:
        print(f"General error with {filename}: {e}")
        continue

print("All done! Results saved to", output_file)
