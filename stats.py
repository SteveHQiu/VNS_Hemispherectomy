#%%
import json, re

# Data sci
import pandas as pd
from scipy.stats import wilcoxon, ranksums, describe, linregress
import seaborn as sns
import matplotlib.pyplot as plt

#%%
sns.set_theme(palette="pastel")

engel_table = {
                "1A": 1,
                "1B": 2,
                "1C": 3,
                "1D": 4,
                "2A": 5,
                "2B": 6,
                "2C": 7,
                "2D": 8,
                "3A": 9,
                "3B": 10,
                "4A": 11,
                "4B": 12,
                "4C": 13,
               }
#%% Whole data 
df3 = pd.read_csv(R"data/data_whole.csv")
df_raw = df3[[
    "age_hemispherectomy_yrs",
    "sex",
    "age_onset",
    "semiology",
    "indication",
    "laterality",
    "engel_immediate",
    "engel_immediate_time_wks",
    "engel_late",
    "engel_late_time_wks",
    "engel_vns",
    "complications",
    ]]

print(describe(df3["age_hemispherectomy_yrs"]))
print(describe(df3["age_onset"]))

measure = pd.to_numeric(df3["engel_late_time_wks"], errors="coerce").dropna()
print(describe(measure))

for indication in df3["indication"].unique():
    print(indication)

#%%
df3 = pd.read_csv(R"data/data_whole.csv")
df3 = df3[df3["engel_late"] != "na"]

df_male = df3[df3["sex"] == "M"]
df_female = df3[df3["sex"] == "F"]

engel_male = [engel_table[i] for i in df_male["engel_late"]]
engel_female = [engel_table[i] for i in df_female["engel_late"]]

print(describe(engel_male))
print(describe(engel_female))

print(ranksums(engel_male, engel_female))
#%%
df3 = pd.read_csv(R"data/data_whole.csv")
df3 = df3[df3["engel_immediate"] != "na"]

df_male = df3[df3["sex"] == "M"]
df_female = df3[df3["sex"] == "F"]

outcome = "engel_immediate"
engel_male = [engel_table[i] for i in df_male[outcome]]
engel_female = [engel_table[i] for i in df_female[outcome]]

print(describe(engel_male))
print(describe(engel_female))

print(ranksums(engel_male, engel_female))
#%%
df3 = pd.read_csv(R"data/data_whole.csv")

outcome = "engel_late"
outcome = "engel_immediate"
df3 = df3[df3[outcome] != "na"]

df_func = df3[df3["indication"].str.contains(R"lennox-gastaut|mre nyd|status epilepticus")]
df_nonfx = df3[~df3["indication"].str.contains(R"lennox-gastaut|mre nyd|status epilepticus")]


engel_func = [engel_table[i] for i in df_func[outcome]]
engel_nonfx = [engel_table[i] for i in df_nonfx[outcome]]

print(describe(engel_func))
print(describe(engel_nonfx))

print(ranksums(engel_func, engel_nonfx, "greater"))
#%% Regression 
df3 = pd.read_csv(R"data/data_whole.csv")
x_label = "engel_late_time_wks"
y_label = "engel_late"
x_label = "engel_immediate_time_wks"
y_label = "engel_immediate"

df3 = df3[df3[y_label] != "na"]
df3[y_label] = df3[y_label].apply(lambda x: engel_table[x])
df3[x_label] = pd.to_numeric(df3[x_label], errors="coerce")
df3 = df3.dropna(subset=[x_label])

sns.scatterplot(x=df3[x_label], y=df3[y_label])
plt.xlabel("Weeks post-op to Engel Class assessment")
plt.ylabel("Engel Classification")
plt.yticks(list(engel_table.values()), list(engel_table.keys()))
print(linregress(df3[x_label], df3[y_label]))

#%% VNS only 

df3 = pd.read_csv(R"data/data.csv")

df_male = df3[df3["sex"] == "M"]
df_female = df3[df3["sex"] == "F"]

outcome = "engel_vns"
engel_male = [engel_table[i] for i in df_male[outcome]]
engel_female = [engel_table[i] for i in df_female[outcome]]

print(describe(engel_male))
print(describe(engel_female))

print(ranksums(engel_male, engel_female))
#%%

outcome = "engel_immediate"
engel_male = [engel_table[i] for i in df_male[outcome]]
engel_female = [engel_table[i] for i in df_female[outcome]]

print(describe(engel_male))
print(describe(engel_female))

print(ranksums(engel_male, engel_female))
#%%

outcome = "engel_late"
engel_male = [engel_table[i] for i in df_male[outcome]]
engel_female = [engel_table[i] for i in df_female[outcome]]

print(describe(engel_male))
print(describe(engel_female))

print(ranksums(engel_male, engel_female))
#%%
outcome1 = "engel_late"
outcome2 = "engel_vns"
diff_male = [engel_table[i[0]] - engel_table[i[1]] for i in
             zip(df_male[outcome1], df_male[outcome2])]
diff_female = [engel_table[i[0]] - engel_table[i[1]] for i in
             zip(df_female[outcome1], df_female[outcome2])]

print(describe(diff_male))
print(describe(diff_female))

print(ranksums(diff_male, diff_female))

#%%

#%% Paired analysis 


df1 = pd.read_csv(R"data/data_pairs1.csv")
df2 = pd.read_csv(R"data/data.csv")

engel_con = df1["engel_late"]
engel_exp = df2["engel_late"] # Assume that engel_vns is taken around the same time as 



rank_con = [engel_table[i] for i in engel_con]
rank_exp = [engel_table[i] for i in engel_exp]

print(rank_con)
print(rank_exp)