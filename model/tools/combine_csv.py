import pandas as pd
import os

df = pd.DataFrame()

for f in os.listdir("data"):
    new_df = pd.read_csv("data/{}".format(f))
    df = pd.concat([df, new_df])

df.set_index("id").to_csv("data.csv")
