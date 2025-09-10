import pandas as pd
import os

chunksize = 5_000_000
chunks = pd.read_csv("bigfile.csv", sep="\t", chunksize=chunksize)

output_folder = "species_csvs"
os.makedirs(output_folder, exist_ok=True)

for chunk in chunks:

    for species, group in chunk.groupby("species"):
        if not group.empty:

            filename = f"{output_folder}/{species.replace(' ', '_')}.csv"

            group.to_csv(filename, mode='a', index=False,
                         header=not os.path.exists(filename))
