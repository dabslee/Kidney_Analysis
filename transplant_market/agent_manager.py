import pandas as pd
import numpy as np
from ipumspy import readers, ddi

class AgentManager:

    def __init__(self):
        self.init_kidpan_data()
        self.init_nhis_data()

    def init_kidpan_data(self):
        # download the data
        kidpan_data_columns = {
            "WL_ORG" : 0,
            "NUM_PREV_TX" : 2,
            "GFR" : 7,
            "GENDER" : 24,
            "EDUCATION" : 33,
            "DIAB" : 37,
            "INIT_AGE" : 54,
            "ETHCAT" : 63,
            "WORK_INCOME_TCR" : 99,
            "DON_TY" : 194,
        }
        self.kidpan_data = pd.read_csv(
            "C:/Users/brand/Desktop/STAR_Delimited/Delimited Text File 202312/Kidney_ Pancreas_ Kidney-Pancreas/KIDPAN_DATA.DAT",
            sep="\t",
            usecols=list(kidpan_data_columns.values())
        )
        self.kidpan_data.columns = list(kidpan_data_columns.keys())
        # restrict to non-foreign donors, kidney-only donations, and white/black/hispanic race only
        self.kidpan_data = self.kidpan_data[self.kidpan_data["WL_ORG"] == "KI"]
        self.kidpan_data = self.kidpan_data[self.kidpan_data["DON_TY"] != "F"]
        self.kidpan_data = self.kidpan_data[
            (self.kidpan_data["ETHCAT"] == 1) | (self.kidpan_data["ETHCAT"] == 2) | (self.kidpan_data["ETHCAT"] == 4)
        ]
        # clean up data
        self.kidpan_data = self.kidpan_data.replace(".", np.nan)
        for numeric_column in ["INIT_AGE", "GFR", "NUM_PREV_TX", "DIAB", "EDUCATION"]:
            self.kidpan_data[numeric_column] = self.kidpan_data[numeric_column].astype(float)
        # find na values and then drop them
        self.kidpan_data = self.kidpan_data.replace({
            "ETHCAT" : {998 : np.nan},
            "ETHCAT_DON" : {998 : np.nan},
            "EDUCATION" : {996 : np.nan, 998 : np.nan},
            "EDUCATION_DON" : {996 : np.nan, 998 : np.nan,},
            "PRI_PAYMENT_TCR_KI" : {15 : np.nan},
            "DIAB" : {5 : np.nan, 998 : np.nan,},
            "WORK_INCOME_TCR" : {"U" : np.nan}
        })
        self.kidpan_data = self.kidpan_data.dropna()
        # create dummy variables
        self.kidpan_data["IS_MALE"] = (self.kidpan_data["ETHCAT"] == 1)
        self.kidpan_data["IS_WHITE"] = (self.kidpan_data["ETHCAT"] == 1)
        self.kidpan_data["IS_BLACK"] = (self.kidpan_data["ETHCAT"] == 2)
        self.kidpan_data["IS_HISPANIC"] = (self.kidpan_data["ETHCAT"] == 4)
        self.kidpan_data["HAS_DIABETES"] = (self.kidpan_data["ETHCAT"] != 1)
        self.kidpan_data["PRIOR_TRANSPLANT"] = (self.kidpan_data["NUM_PREV_TX"] > 0)
        self.kidpan_data["WORK_INCOME_TCR"] = (self.kidpan_data["WORK_INCOME_TCR"] == "Y")

    def init_nhis_data(self):
        # download the data
        self.nhis_data = readers.read_microdata(
            ddi=readers.read_ipums_ddi("C:/Users/brand/Desktop/STAR_Delimited/IPUMS Population Data/nhis_00001.dat/nhis_00001.xml"),
            filename="C:/Users/brand/Desktop/STAR_Delimited/IPUMS Population Data/nhis_00001.dat/nhis_00001.dat"
        )
        # restrict to 2019 data, people over 18 and without diabetes, and white/black/hispanic race only
        self.nhis_data = self.nhis_data[self.nhis_data["YEAR"] == 2019]
        self.nhis_data = self.nhis_data[self.nhis_data["AGE"] >= 18]
        self.nhis_data = self.nhis_data[self.nhis_data["DIABTYPE"] == 0]
        # identify na values and correct them
        self.nhis_data = self.nhis_data.replace({
            "SEX" : {7 : np.nan, 8 : np.nan, 9 : np.nan},
            "HEIGHT" : {0 : np.nan, 95 : np.nan, 96 : np.nan, 97 : np.nan, 98 : np.nan, 99 : np.nan},
            "WEIGHT" : {0 : np.nan, 996 : np.nan, 997 : np.nan, 998 : np.nan, 999 : np.nan},
            "AGE" : {997 : np.nan, 998 : np.nan, 999 : np.nan},
            "DIABTYPE" : {7 : np.nan, 8 : np.nan, 9 : np.nan},
            "RACENEW" : {997 : np.nan, 998 : np.nan, 999 : np.nan},
            "EDUC" : {996 : np.nan, 997 : np.nan, 998 : np.nan, 999 : np.nan},
        })
        # drop unimportant columns and remove nas
        self.nhis_data = self.nhis_data[["AGE", "RACENEW", "SEX", "HEIGHT", "WEIGHT", "EDUC", "DIABTYPE", "HISPETH"]]
        self.nhis_data = self.nhis_data.dropna()
        # create dummy variables
        self.nhis_data["IS_MALE"] = (self.nhis_data["SEX"] == 1)
        self.nhis_data["BMI"] = self.nhis_data["WEIGHT"] / (self.nhis_data["HEIGHT"])**2 * 703.07 # psi => kg/m^2
        self.nhis_data["HAS_DIABETES"] = (self.nhis_data["DIABTYPE"] != 0)
        self.nhis_data["IS_WHITE"] = (self.nhis_data["RACENEW"] == 100)
        self.nhis_data["IS_BLACK"] = (self.nhis_data["RACENEW"] == 200)
        self.nhis_data["IS_HISPANIC"] = (self.nhis_data["HISPETH"] != 10) & (self.nhis_data["HISPETH"] < 90)
        # restrict to white/black/hispanic only
        self.nhis_data = self.nhis_data[
            self.nhis_data["IS_WHITE"] | self.nhis_data["IS_BLACK"] | self.nhis_data["IS_HISPANIC"]
        ]

    def generate_recipient(self):
        return self.kidpan_data.iloc[np.random.randint(0,self.kidpan_data.shape[0])]

    def generate_giver(self):
        return self.nhis_data.iloc[np.random.randint(0,self.nhis_data.shape[0])]
    
    def giver_income(self, agent, age):
        return -12720 + 1812.2356*age - 17.3636*age**2 + 3.08*10**(-11)*agent["IS_MALE"] + 3630.4875*agent["IS_WHITE"] - 11990*agent["IS_BLACK"] - 8098.4875*agent["IS_HISPANIC"] + 33090*(agent["EDUC"] >= 300)
    
    def giver_mortality(self, agent, age):
        bmi_std = (agent["BMI"] - np.mean(self.nhis_data["BMI"]))/np.std(self.nhis_data["BMI"])
        covariates = []
        covariates += [bmi_std, bmi_std**2, bmi_std**3]
        covariates += [agent["IS_BLACK"], agent["IS_HISPANIC"], 0, 0, 0, 0]
        try:
            covariates += [agent["EDUC"] == 103, agent["EDUC"] == 201, agent["EDUC"] == 302, agent["EDUC"] == 301, agent["EDUC"] == 400, (agent["EDUC"] >= 500) & (agent["EDUC"] <= 505), 0]
        except:
            covariates += [0, 0, 0, 1, 0, 0, 0]
        covariates += [0] * 31
        covariates += [0] * 6
        covariates += [0] * 8
        covariates += [0] * 5
        covariates += [0] * 5
        covariates += [agent["HAS_DIABETES"]]
        covariates += [(agent["AGE"] - np.mean(self.nhis_data["AGE"]))/np.std(self.nhis_data["AGE"])]
        covariates += [(agent["HEIGHT"] - np.mean(self.nhis_data["HEIGHT"]))/np.std(self.nhis_data["HEIGHT"])]
        if agent["IS_MALE"]:
            beta = np.array([0.02, 0.09, -0.01, 0.05, -0.22, -0.18, -0.12, 0.03, 0.07, 0.02, -0.04, -0.06, -0.05, -0.12, -0.19, 0.05, 0.06, 0.15, 0.21, 0.31, 0.36, 0.43, 0.32, 0.49, 0.59, 0.68, 0.55, 0.68, 0.49, 0.55, 0.74, 0.78, 0.87, 0.92, 0.71, 0.8, 0.92, 1.22, 1, 0.71, 0.77, 0.99, 1.13, 1.29, 1.31, 1.25, 0.36, -0.11, -0.23, -0.25, -0.31, -0.31, -0.17, -0.19, -0.22, -0.18, -0.06, -0.03, 0.01, -0.05, 0.08, 0.17, 0.36, 0.7, 1.25, 0.52, 0.22, 0.22, 0.19, 0.31, 0.05, 0.47, -0.03, 0.08])
        else:
            beta = np.array([0.01, 0.07, -0.01, -0.02, -0.19, -0.28, -0.24, 0.14, 0.12, 0.05, 0.04, 0.02, 0.03, -0.01, -0.05, 0.09, 0.04, 0.21, 0.35, 0.42, 0.34, 0.55, 0.28, 0.44, 0.52, 0.77, 0.58, 0.99, 0.34, 0.58, 0.71, 0.81, 0.54, 0.64, 0.56, 0.89, 1.03, 1.07, 1.02, 0.44, 0.86, 1.12, 1.23, 1.39, 1.45, 1.53, 0.4, -0.11, -0.24, -0.26, -0.31, -0.27, -0.18, -0.18, -0.11, -0.06, 0.15, 0, 0.05, 0.01, 0.37, 0.12, 0.34, 0.67, 1.1, 0.52, 0.15, 0.12, 0.1, 0.27, 0.2, 0.62, -0.09, 0.05])
        mort = (0.000034 * np.exp(0.092899 * age) + 0.000915) * np.exp(beta @ np.array(covariates))
        return np.clip(mort, a_max=1)

    def recipient_income_dialysis(self, agent, age):
        return 0.23 * self.giver_income(agent, age) + 0.77 * 12140
    
    def recipient_income_transplant(self, agent, time_since_transplant, age):
        employment =  1 / (1 + np.exp(-(-1.1378 + 0.3020 * time_since_transplant + 1.9305 * agent["WORK_INCOME_TCR"])))
        return employment * self.giver_income(agent, age)

    def receipient_mortality_dialysis(self, agent, age):
        beta = 0.0064 * agent["GFR"] + 0.0362 * agent["HAS_DIABETES"]
        if agent["IS_WHITE"]: h = 0.030377 * np.exp(0.035875 * age) + 0.020246
        elif agent["IS_BLACK"]: h =  0.006207 * np.exp(0.052413 * age) + 0.061768
        elif agent["IS_HISPANIC"]: h =  0.015619 * np.exp(0.042351 * age) + 0.005365
        mort = h * (1 - beta) + beta
        return np.clip(mort, a_max=1)
    
    def recipient_mortality_transplant(self, agent, waitlist_time, age):
        mort = 0.000022685 * np.exp(0.083531722 * age) + 0.000000229*waitlist_time + 0.000452195*agent["PRIOR_TRANSPLANT"] + 0.000824622*agent["HAS_DIABETES"] - 0.000020527*agent["GFR"] + 0.000093482*agent["IS_WHITE"]
        return np.clip(mort, a_max=1)