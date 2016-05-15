import pandas as pd
import numpy as np

def show_datasets( infofilename, pairfilename ):
    info = pd.read_csv(infofilename, encoding="utf-8")
    df = pd.read_csv(pairfilename)
    info = info.drop(['title','description','attrsJSON'], axis = 1)
    df = pd.merge(pd.merge(df, info, how = 'inner', left_on = 'itemID_1', right_on = 'itemID'), info, how = 'inner', left_on = 'itemID_2', right_on = 'itemID')
    df.to_csv("input/merged.csv")

show_datasets("input/ItemInfo_train.csv", "input/ItemPairs_train.csv")
