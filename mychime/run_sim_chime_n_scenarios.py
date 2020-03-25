import pandas as pd
import numpy as np
import math

from datetime import datetime

from pandas import DataFrame

from penn_chime.parameters import Parameters
from penn_chime.models import SimSirModel
from penn_chime.utils import RateLos


# ---- Base input values



known_infections = 1581  # update daily
known_cases = 250  # update daily

market_share = 0.28  # 0 - 1.0

# -- SIR and resource model input parameter base values

# Number of days to run model
n_days = 120

# Currently Hospitalized COVID-19 Patients
current_hosp = known_cases
# Doubling time before social distancing (days)
doubling_time = 4
# Social distancing (% reduction in social contact)
relative_contact_rate = 0.50
# Recovery days
recovery_days = 14

# Hospitalization %(total infections)
hosp_rate = 0.025
# ICU %(total infections)
icu_rate = 0.0075
# Ventilated %(total infections)
vent_rate = 0.005
# Hospital average Length of Stay (days)
hosp_los = 7
# ICU average Length of Stay (days)
icu_los = 9
# Vent average Length of Stay (days)
vent_los = 10

p = Parameters(
    current_hospitalized=current_hosp,
    doubling_time=doubling_time,
    known_infected=known_infections,
    market_share=market_share,
    n_days=n_days,
    relative_contact_rate=relative_contact_rate,
    susceptible=S_default,

    hospitalized=RateLos(hosp_rate, hosp_los),
    icu=RateLos(icu_rate, icu_los),
    ventilated=RateLos(vent_rate, vent_los),
)

# ---- Run one scenario

scenario = 'base_test'



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
    scenario = 'test_soc_{:.0f}'.format(100 * sdpct)

    # Update the parameters for this scenario
    p.relative_contact_rate = sdpct

    # Run the model
    m = SimSirModel(p)

    # Get the output dfs


    # Get key input/output variables

    intrinsic_growth_rate = m.intrinsic_growth_rate
    gamma = m.gamma  # Recovery rate
    beta = m.beta  # Contact rate

    # r_t is r_0 after distancing
    r_t = m.r_t
    r_naught = m.r_naught
    doubling_time_t = m.doubling_time_t
    results = {
        'raw_sir_df': m.raw_df,
        'dispositions_df': m.dispositions_df,
        'admits_df': m.admits_df,
        'census_df': m.census_df,
        'scenario_inputs': scenario_inputs
    }

    results_list.append(results)

# Just printing out a few to show
# Obviously we can do whatever we want with the results
# In fact, first I'll concat all the scenario dataframes
# and export to csvs

projection_df_list = [results['projection'] for results in results_list]
projection_df = pd.concat(projection_df_list)
projection_df.to_csv("./output/projection_df_demo.csv", index=False)

projection_admits_df_list = [results['projection_admits'] for results in results_list]
projection_admits_df = pd.concat(projection_admits_df_list)
projection_admits_df.to_csv("./output/projection_admits_df_demo.csv", index=False)

projection_census_df_list = [results['projection_census'] for results in results_list]
projection_census_df = pd.concat(projection_census_df_list)
projection_census_df.to_csv("./output/projection_census_df_demo.csv", index=False)

projection_resources_df_list = [results['projection_resources'] for results in results_list]
projection_resources_df = pd.concat(projection_resources_df_list)
projection_resources_df.to_csv("./output/projection_resources_df_demo.csv", index=False)

for key, item in results_list[0].items():
    print(key)
    print(item)

for key, item in results_list[math.ceil(num_scenarios / 2)].items():
    print(key)
    print(item)

for key, item in results_list[-1].items():
    print(key)
    print(item)