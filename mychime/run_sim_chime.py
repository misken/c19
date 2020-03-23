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


# ---- Run one scenario

proj, proj_admits, proj_census = \
    chime.sim_chime(S_default,known_infections, known_cases,
              market_share, n_days,
              doubling_time, relative_contact_rate,
              recovery_days,
              hosp_rate, icu_rate, vent_rate,
              hosp_los, icu_los, vent_los)

print(proj)
print(proj_admits)
print(proj_census)