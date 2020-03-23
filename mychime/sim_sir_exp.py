import pandas as pd
import numpy as np

import sim_sir as sir

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

# Hospital Market Share (%)
BH_market_share = market_share / 100

# Regional Population
S = S_default

# Currently Known Regional Infections (only used to compute detection rate - does not change projections
initial_infections = known_infections

# ------ Intermediate SIR model variables

# Seems like estimating initial number of total infections in the population *region*
# we are modeling (i.e. that we put population numbers in above) by inferring from the
# number we have in hospital and then inflating by both our market share and then
# the hospitalization rate of infecteds. So, total_infections is in our entire
# region.

total_infections = current_hosp / BH_market_share / hosp_rate

# Estimate prob[detection | infected]. Will be used to initialize size of I.
detection_prob = initial_infections / total_infections

# Compute initial values for S, I, and R (susceptible, infectious, recovered)
# Note that initial value for S was set up above based on input params
# I is initialized by reflecting the fact that there are a bunch of undetected
# cases out there and R is initially set to 0.
S, I, R = S, initial_infections / detection_prob, 0

# Since this model lets user input the doubling time (time for I -> 2I), we can back into the
# implied intrinsic growth rate of the pandemic. We'll use this below to get to
# key model terms like "basic reproduction number"
intrinsic_growth_rate = 2 ** (1 / doubling_time) - 1

# recovery_days = 14.0 # Hmm, was hard coded. I moved up into input params.
# mean recovery rate, gamma, (in 1/days).
gamma = 1 / recovery_days

# Contact rate, beta
beta = (
    intrinsic_growth_rate + gamma
) / S * (1-relative_contact_rate) # {rate based on doubling time} / {initial S}

# Now can compute the "basic reproduction number". It's kind of like the
# rho term in queueing models. When > 1, epidemic grows.
r_t = beta / gamma * S # r_t is r_0 after distancing
r_naught = r_t / (1-relative_contact_rate)
doubling_time_t = 1/np.log2(beta*S - gamma +1) # doubling time after distancing

# ------- Run SIR model

# Assume no beta decay for now.
beta_decay = 0.0

# Call the main simulation function.
s, i, r = sir.sim_sir(S, I, R, beta, gamma, n_days, beta_decay=beta_decay)

# ------- Compute resource needs based on SIR

# Compute arrays of resource use at each time step
# Note that the three resources included in the base model are just using
# "multipliers" to compute hospital specific guesstimates of resource needs.
# A similar kind of thing might be appropriate for many resources such
# as needs for numbers of certain kinds of staff.

hosp = i * hosp_rate * BH_market_share
icu = i * icu_rate * BH_market_share
vent = i * vent_rate * BH_market_share

# ------- Prep results for plotting and analysis

# Now read to create master DataFrame to drive plots

# Need array of the days
days = np.array(range(0, n_days + 1))

# Combine arrays for days and all resource related arrays.
# Obviously, as new resource computations are added above,
# need to add those arrays to data_list and data_dict.
data_list = [days, hosp, icu, vent]

# Create a dictionary from data_list to use to easily create pandas DataFrame.
data_dict = dict(zip(["day", "hosp", "icu", "vent"], data_list))

# Create the main DataFrame containing resource projections.
projection = pd.DataFrame.from_dict(data_dict)

# ------ Compute projected admits from projection results

# New cases (computing lag 1 difference)
projection_admits = projection.iloc[:-1, :] - projection.shift(1)
projection_admits[projection_admits < 0] = 0

plot_projection_days = n_days - 10
projection_admits["day"] = range(projection_admits.shape[0])

# ------ Compute census and other resource usage

# The following function I left exactly as is from the UPenn model. Need
# to dig into it in more detail to best understand how to incorporate
# new resources. We might want to have a separate function that does
# similar thing for any resources we add.
def _census_table(projection_admits, hosp_los, icu_los, vent_los) -> pd.DataFrame:
    """ALOS for each category of COVID-19 case (total guesses)"""

    los_dict = {
        "hosp": hosp_los,
        "icu": icu_los,
        "vent": vent_los,
    }

    census_dict = dict()
    for k, los in los_dict.items():
        census = (
            projection_admits.cumsum().iloc[:-los, :]
            - projection_admits.cumsum().shift(los).fillna(0)
        ).apply(np.ceil)
        census_dict[k] = census[k]

    census_df = pd.DataFrame(census_dict)
    census_df["day"] = census_df.index
    census_df = census_df[["day", "hosp", "icu", "vent"]]

    census_table = census_df[np.mod(census_df.index, 7) == 0].copy()
    census_table.index = range(census_table.shape[0])
    census_table.loc[0, :] = 0
    census_table = census_table.dropna().astype(int)

    return census_table


census_projection = _census_table(projection_admits, hosp_los, icu_los, vent_los)

print(census_projection)