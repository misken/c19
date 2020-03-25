import pandas as pd
import numpy as np
import math
import json
import pprint

from datetime import datetime

from pandas import DataFrame

from penn_chime.settings import DEFAULTS as d
from penn_chime.parameters import Parameters
from penn_chime.models import SimSirModel
from penn_chime.utils import RateLos

# Default values (uses values in settings.py) - you can modify them below this section
susceptible_default = d.region.susceptible
current_hospitalized_default = d.current_hospitalized
doubling_time_default = d.doubling_time
known_infected_default = d.known_infected
relative_contact_rate_default = d.relative_contact_rate

hosp_rate_default = d.hospitalized.rate
icu_rate_default = d.icu.rate
vent_rate_default = d.ventilated.rate

hosp_los_default = d.hospitalized.length_of_stay
icu_los_default = d.icu.length_of_stay
vent_los_default = d.ventilated.length_of_stay

market_share_default = d.market_share
n_days_default = d.n_days
recovery_days_default = d.recovery_days


# ------ CHIME model input parameter base values (YOU CAN SET OR CHANGE THESE)

scenario = 'base_test'
output_path = './output/'

# Regional population
susceptible = susceptible_default

# Number of days to run model
n_days = n_days_default

# Known infected in region (# update daily)
#   (only used to compute detection rate, doesn't affect projections)
known_infected = known_infected_default

# Currently Hospitalized COVID-19 Patients (# update daily)
current_hospitalized = current_hospitalized_default

# Doubling time before social distancing (days)
doubling_time = doubling_time_default
# Social distancing (% reduction in social contact)
relative_contact_rate = relative_contact_rate_default
# Recovery days
recovery_days = recovery_days_default

# Hospitalization %(total infections) (values in 0.0-1.0)
hosp_rate = hosp_rate_default
# ICU %(total infections) (values in 0.0-1.0)
icu_rate = icu_rate_default
# Ventilated %(total infections) (values in 0.0-1.0)
vent_rate = vent_rate_default

# Hospital average Length of Stay (int days)
hosp_los = hosp_los_default
# ICU average Length of Stay (int days)
icu_los = icu_los_default
# Vent average Length of Stay (int days)
vent_los = vent_los_default

# Market share
market_share = market_share_default  # (values in 0.0-1.0)

# Create penn_chime parameter object

p = Parameters(
    current_hospitalized=current_hospitalized,
    doubling_time=doubling_time,
    known_infected=known_infected,
    market_share=market_share,
    n_days=n_days,
    relative_contact_rate=relative_contact_rate,
    susceptible=susceptible,

    hospitalized=RateLos(hosp_rate, hosp_los),
    icu=RateLos(icu_rate, icu_los),
    ventilated=RateLos(vent_rate, vent_los),
)

input_params_dict = vars(p)

# ---- Run one scenario

# Run the model
m = SimSirModel(p)

# Get the output dfs
raw_sir_df = m.raw_df
dispositions_df = m.dispositions_df
admits_df = m.admits_df
census_df = m.census_df

# Get key input/output variables

intrinsic_growth_rate = m.intrinsic_growth_rate
gamma = m.gamma # Recovery rate
beta = m.beta   # Contact rate

# r_t is r_0 after distancing
r_t = m.r_t
r_naught = m.r_naught
doubling_time_t = m.doubling_time_t

intermediate_variables = {
    "intrinsic_growth_rate": intrinsic_growth_rate,
    "gamma": gamma,
    "beta": beta,
    "r_naught": r_naught,
    "r_t": r_t,
    "doubling_time_t": doubling_time_t,
}

results = {
    'scenario_str': scenario,
    'input_params_dict': input_params_dict,
    'intermediate_variables_dict': intermediate_variables,
    'raw_sir_df': m.raw_df,
    'dispositions_df': m.dispositions_df,
    'admits_df': m.admits_df,
    'census_df': m.census_df,
}

print("\nInput parameters")
print("{}".format(50 * '-'))
#print(param_dict)
print(json.dumps(param_dict, indent=4, sort_keys=False))
# pprint.pprint(param_dict)

print("\nIntermediate variables")
print("{}".format(50 * '-'))
#print(intermediate_variables)
print(json.dumps(intermediate_variables, indent=4, sort_keys=False))
# pprint.pprint(intermediate_variables)
print("\n")

# Intermediate model variables
print('Intrinsic growth rate: {:.3f}'.format(intrinsic_growth_rate))
print('gamma (recovery rate): {:.3f}'.format(gamma))
print('beta (contact rate): {:.3f}'.format(beta))
print('Basic reproductive rate: {:.3f}'.format(r_naught))
print('Adjusted reproductive rate (after social distancing): {:.3f}'.format(r_t))
print('Adjusted doubling time in days (after social distancing): {:.0f}'.format(doubling_time_t))

# Results dataframes
raw_sir_df.to_csv("{}raw_sir_{}.csv".format(output_path, scenario), index=False)
dispositions_df.to_csv("{}dispositions_{}.csv".format(output_path, scenario), index=False)
admits_df.to_csv("{}admits_{}.csv".format(output_path, scenario), index=False)
census_df.to_csv("{}census_{}.csv".format(output_path, scenario), index=False)



