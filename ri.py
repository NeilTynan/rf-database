import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from functions import clean_currency

url = "/workspaces/rf-database/ritemp.csv"
ri = pd.read_csv(url, encoding="cp1252")

# Fix data types
ri['Start Date'] = pd.to_datetime(ri['Start Date'], dayfirst=True, errors='coerce')
ri['End Date'] = pd.to_datetime(ri['End Date'], dayfirst=True, errors='coerce')
ri['Current Total Commitment'] = clean_currency(ri['Current Total Commitment'])

# Strip out unnessary columns
ri = ri.drop(columns=['Sub-Programme','ORCID ID','Lead Applicant','Research Body','Research Body ROR ID','Funder ROR ID'])

# Drop all supplements
ri = ri[ri['Supplement'].isna()]
ri = ri.drop(columns=['Supplement'])

# Remove refunds
ri = ri[ri["Propossal ID"].str.contains("(N)", regex=False, na=False) == False]

# Aggregation
ric = ri.groupby("Programme Name").agg(awardno=("Propossal ID", "nunique"), totalaward=("Current Total Commitment", "sum"), meanaward=("Current Total Commitment", "mean"), 
                                       minaward=("Current Total Commitment", "min"), maxaward=("Current Total Commitment", "max"))

dsum = ri.pivot_table(index="Programme Name",columns="Discipline",values="Current Total Commitment",aggfunc="sum")
dsum.columns = [f"{col.lower()} TotalAward" for col in dsum.columns]

dmean = ri.pivot_table(index="Programme Name",columns="Discipline",values="Current Total Commitment",aggfunc="mean")
dmean.columns = [f"{col.lower()} MeanAward" for col in dmean.columns]

dmin = ri.pivot_table(index="Programme Name",columns="Discipline",values="Current Total Commitment",aggfunc="min")
dmin.columns = [f"{col.lower()} MinAward" for col in dmin.columns]

dmax = ri.pivot_table(index="Programme Name",columns="Discipline",values="Current Total Commitment",aggfunc="max")
dmax.columns = [f"{col.lower()} MaxAward" for col in dmax.columns]

ricf = (ric.join(dmean).join(dmin).join(dmax).reset_index())
print(ricf.head(31))
