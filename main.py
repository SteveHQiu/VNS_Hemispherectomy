#%%
import json, re

# Data sci
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(palette="pastel")

#%%
df = pd.read_csv(R"data/data.csv")

#%% Pie graphs
def genPieLabel(values):
    def _genPieLabel(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d} ({p:.1f}%)'.format(p=pct,v=val)
    return _genPieLabel

def genPieChart(col: str, title: str, file_name: str = None):
    data = df[col].value_counts()
    data_keys = [s.strip().capitalize() for s in data.keys()]
    data_zipped = list(zip(data_keys, data)) # For future use

    plt.pie(data, labels=data_keys, autopct=genPieLabel(data))
    plt.title(title)
    
    if file_name:
        plt.savefig(RF"figures/{file_name}.png", dpi=300, format="png")
        
    plt.show()
    
genPieChart("semiology",
            "Distribution of Patient Seizure Semiologies",
            "Fig1",
            )

genPieChart("sex",
            "Distribution of Patient Sex",
            "Fig2",
            )

genPieChart("laterality",
            "Hemispherectomy Laterality",
            "Fig3",
            )

genPieChart("indication",
            "Indication for Hemispherectomy",
            "Fig4",
            )



#%% Boxplots
def genBoxScatter(col: str, title: str, x_lab: str,
                  file_name: str = None):
    sns.boxplot(x=df[col]) # Reminder that orientation determined by x/y variable rather than kwarg 'orient'
    sns.stripplot(x=df[col], color=".25")
    plt.title(title)
    plt.xlabel(x_lab)
    
    if file_name:
        plt.savefig(RF"figures/{file_name}.png", dpi=300, format="png")

    plt.show()

genBoxScatter("age_onset",
              "Age of Symptom Onset",
              "Age (years)",
              "Fig5",
              )

genBoxScatter("age_hemispherectomy_yrs",
              "Patient Age at Date of Hemispherectomy",
              "Age (years)",
              "Fig6",
              )
#%% Trends
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

engel_imm = df["engel_immediate"]
engel_late = df["engel_late"]
engel_vns = df["engel_vns"]

engel_imm_dt = df["engel_immediate_time_wks"]
engel_late_dt = df["engel_late_time_wks"]

df_engels = pd.concat([engel_imm, engel_late, engel_vns], axis=1).T
df_engels = df_engels.applymap(lambda x: engel_table[x.upper()])
df_engels = df_engels.set_axis([F"Patient #{i}" for i in range(1, len(df_engels.columns) + 1)],
                               axis=1)
df_engels = df_engels.set_axis([
                                "Early\nPost-hemispherectomy",
                                "Late\nPost-hemispherectomy",
                                "Post-VNS",
                                ],
                               axis=0
                               )

file_name = "Fig7"

sns.lineplot(data=df_engels)
plt.title("Trend of Engel Class for Patient Cohort")
plt.ylabel("Engel Classification")
# plt.xticks(rotation=45)
plt.yticks(list(engel_table.values()), list(engel_table.keys()))
plt.savefig(RF"figures/{file_name}.png", dpi=300, format="png")
plt.show()

#%% Tables
df_raw = df[[
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

print(df_raw["engel_immediate_time_wks"].describe())
print(df_raw["engel_late_time_wks"].describe())

df_raw = df_raw.set_axis([
                        "Age at Hemispherectomy",
                        "Sex",
                        "Age at Symptom Onset",
                        "Epileptic Seizure Semiology",
                        "Indication for Hemispherectomy",
                        "Laterality of Hemispherectomy",
                        "Engel Class Early Post-hemispherectomy",
                        "Weeks Post-op to Early Engel Class Measurement",
                        "Engel Class Post-hemispherectomy",
                        "Weeks Post-op to Late Engel Class Measurement",
                        "Engel Class Post-VNS",
                        "Surgical Complications",
                        ],
                        axis=1
                        )

def roundCells(x):
        if isinstance(x, (int, float)):
            return round(x, 1)
        else:
            return x

df_raw = df_raw.applymap(roundCells)

print(df_raw.to_markdown())
