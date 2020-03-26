"""
THIS HAS BARELY BEEN STARTED. JUST A PLACEHOLDER
"""



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

scenario_prefix = 'test_'
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

# ---- Explore range of a single input

# Create a range of social distances

soc_dists = np.arange(0.05,0.90, 0.05)
# array([0.05, 0.1 , 0.15, 0.2 , 0.25, 0.3 , 0.35, 0.4 , 0.45, 0.5 , 0.55,
#        0.6 , 0.65, 0.7 , 0.75, 0.8 , 0.85])

num_scenarios = len(soc_dists)

# We can store outputs any way we want. For this demo, just going to
# use a master list. # This will be a list of dicts of the
# result dataframes (+ 1 dict containing the scenario inputs)
results_list = []

for sdpct in soc_dists:
    scenario = '{}{:.0f}'.format(scenario_prefix, 100 * sdpct)

    # Update the parameters for this scenario
    p.relative_contact_rate = sdpct
    input_params_dict = vars(p)

    # Run the model
    m = SimSirModel(p)

    # Get the output dfs

    # Get the output dfs
    raw_sir_df = m.raw_df
    dispositions_df = m.dispositions_df
    admits_df = m.admits_df
    census_df = m.census_df

    # Get key input/output variables

    intrinsic_growth_rate = m.intrinsic_growth_rate
    gamma = m.gamma  # Recovery rate
    beta = m.beta  # Contact rate

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

    # Get key input/output variables

    results = {
        'scenario_str': scenario,
        'input_params_dict': input_params_dict,
        'intermediate_variables_dict': intermediate_variables,
        'raw_sir_df': m.raw_df,
        'dispositions_df': m.dispositions_df,
        'admits_df': m.admits_df,
        'census_df': m.census_df,
    }

    results_list.append(results)

# Just printing out a few to show
# Obviously we can do whatever we want with the results
# In fact, first I'll concat all the scenario dataframes
# and export to csvs

# projection_df_list = [results['projection'] for results in results_list]
# projection_df = pd.concat(projection_df_list)
# projection_df.to_csv("./output/projection_df_demo.csv", index=False)
#
# projection_admits_df_list = [results['projection_admits'] for results in results_list]
# projection_admits_df = pd.concat(projection_admits_df_list)
# projection_admits_df.to_csv("./output/projection_admits_df_demo.csv", index=False)
#
# projection_census_df_list = [results['projection_census'] for results in results_list]
# projection_census_df = pd.concat(projection_census_df_list)
# projection_census_df.to_csv("./output/projection_census_df_demo.csv", index=False)
#
# projection_resources_df_list = [results['projection_resources'] for results in results_list]
# projection_resources_df = pd.concat(projection_resources_df_list)
# projection_resources_df.to_csv("./output/projection_resources_df_demo.csv", index=False)

for key, item in results_list[0].items():
    print(key)
    print(item)

for key, item in results_list[math.ceil(num_scenarios / 2)].items():
    print(key)
    print(item)

for key, item in results_list[-1].items():
    print(key)
    print(item)
