import pandas as pd
import numpy as np

import sim_chime as chime

# Population parameters
wayne = 1778396
oakland = 1248141
macomb = 867502
genesee = 414657
washtenaw = 326058
saintclair = 158313
monroe = 153436
lapeer = 79723
S_default = wayne + oakland + macomb + genesee + washtenaw + saintclair + monroe + lapeer

known_infections = 787  # update daily
known_cases = 457  # update daily

market_share = 28.0
#

# ------ SIR and resource model input parameter base values

# Number of days to run model
n_days = 120

# Currently Hospitalized COVID-19 Patients
current_hosp = known_cases
# Doubling time before social distancing (days)
doubling_time = 6
# Social distancing (% reduction in social contact)
relative_contact_rate = 0.25
# Recovery days
recovery_days = 14

# Hospitalization %(total infections)
hosp_rate = 0.05
# ICU %(total infections)
icu_rate = 0.02
# Ventilated %(total infections)
vent_rate = 0.01
# Hospital average Length of Stay (days)
hosp_los = 7
# ICU average Length of Stay (days)
icu_los = 9
# Vent average Length of Stay (days)
vent_los = 10

# New resource related parameters
pct_ped_vent = 0.10


# ---- Run one scenario

scenario = 'base_test'
proj, proj_admits, proj_census, proj_resources, scenario_inputs = \
    chime.sim_chime(scenario, S_default, known_infections, known_cases,
                    market_share, n_days,
                    doubling_time, relative_contact_rate,
                    recovery_days,
                    hosp_rate, icu_rate, vent_rate,
                    hosp_los, icu_los, vent_los,
                    pct_ped_vent)

print(proj)
print(proj_admits)
print(proj_census)
print(proj_resources)
print(scenario_inputs)


# ---- Explore range of a single input

# Create a range of social distances

soc_dists = np.arange(0.05,0.90, 0.05)
# array([0.05, 0.1 , 0.15, 0.2 , 0.25, 0.3 , 0.35, 0.4 , 0.45, 0.5 , 0.55,
#        0.6 , 0.65, 0.7 , 0.75, 0.8 , 0.85])

# We can store outputs any way we want. For this demo, just going to
# use a master list. # This will be a list of dicts of the
# result dataframes (+ 1 dict containing the scenario inputs)
results_list = []

for sdpct in soc_dists:
    scenario = 'test_soc_{:.0f}'.format(100 * sdpct)
    proj, proj_admits, proj_census, proj_resources, scenario_inputs = \
        chime.sim_chime(scenario, S_default, known_infections, known_cases,
                        market_share, n_days,
                        doubling_time, relative_contact_rate,
                        recovery_days,
                        hosp_rate, icu_rate, vent_rate,
                        hosp_los, icu_los, vent_los,
                        pct_ped_vent)

    results = {
        'projection': proj,
        'projection_admits': proj_admits,
        'projection_census': proj_census,
        'projection_resources': proj_resources,
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

for key, item in results_list[5].items():
    print(key)
    print(item)

for key, item in results_list[-1].items():
    print(key)
    print(item)