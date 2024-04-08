import numpy as np
import datetime
from enum import Enum
from typing import Callable

class RACE(Enum):
    WHITE = 1 # White, non-Hispanic
    BLACK = 2 # Black, non-Hispanic
    HISPANIC = 4 # Hispanic/Latino
    ASIAN = 5 # Asian, non-Hispanic
    NATIVE = 6 # Amer Ind/Alaska Native, Non-Hispanic
    PACIFIC = 7 # Native Hawaiian/other Pacific Islander, Non-Hispanic
    MULTI = 9 # Multiracial, Non-Hispanic

class BLOOD_TYPE(Enum):
    O = 1
    A = 2
    B = 3
    AB = 4
    A1 = 5
    A2 = 6
    A1B = 7
    A2B = 8

class DIABETIC(Enum):
    NONE: 1
    TYPE1: 2
    TYPE2: 3
    OTHER: 4

class Agent:
    # demographics
    age: int # in years
    race: RACE # what race are they?
    height: float # in inches
    weight: float # in pounds
    location: int # zip code
    wealth: float # net worth in 2010 USD
    income: float # annual income in 2010 USD
    college: bool # graduated college?
    insurance: bool # has health insurance?

    # behavioral characteristics
    altruism_factor: float # utility derived from utility gain of others
    nonrational_factor: float # non-rational utility or disutility of transplant
    time_discounting: float # hyperbolic time discounting parameter
    prospect_curve: Callable # gain/loss utility function based on prospect theory; encompasses risk tolerance

    # health stats
    ckd: bool # do they have CKD?
    esrd: bool # do they have ESRD?
    crcl: float # creatinine clearance
    gfr: float # glomerular filtration rate
    blood_type: BLOOD_TYPE # ABO blood type
    hla_type: list[str] # List of HLA alleles
    diabetic: DIABETIC # diabetes status
    hypertension: bool # history of hypertension?
    comorbidities: bool # history of CMV, HepB/C, HIV, cancer, etc.
    prior_donor: bool # previously donated a kidney
    prior_recipient: bool # previously had another organ transplant

    # assessment stats
    cpra: float # estimated percentage of incompatible donors
    psychosocial: bool # eligible to donate based on psychosocial survey
    urgent: bool # classified as medically urgent by OPTN standards
    kdpi: float # Kidney Donor Profile Index (KDPI) score

    # registration and tracking
    dialysis_date: datetime.date # when (if at all) did they get on dialysis?
    registration_date: datetime.date # when (if at all) did they register as a donor/recipient?
    transplant_date: datetime.date # the date of the surgery
    death_date: datetime.date # date of patient death
    waiting_time: float # official waiting time as measured by the OPTN standards

    # outcomes
    morbidity_rate: Callable # morbidity rate over time
    incurred_costs: float # total costs (transportation, medical costs, lost wages etc. incurred as result of transplant)
    subsidies: float # additional fees, taxes, and subsidies associated with transplant

    # generates a recipient agent based on last 10 years of US OPTN demographics
    # essentially draws from the US population distribution conditional on having ESRD
    def generate_US_recipient():
        