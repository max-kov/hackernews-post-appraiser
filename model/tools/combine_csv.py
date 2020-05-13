import pandas as pd
import os

df = pd.DataFrame()
data = "by,id,score,url,title,time,type\n"


for f in os.listdir("data"):
    filename = "data/{}".format(f)
    with open(filename, "r") as fp:
        #drop header line
        fp.readline()
        data += fp.read()

with open("data.csv", "w+") as fp:
    fp.write(data)

