import pandas as pd
import numpy as np
import math

import sim_sir as sir


def sim_chime(scenario, population, known_infections, known_cases,
              market_share=28, n_days=120,
              doubling_time=6, relative_contact_rate=0.25,
              recovery_days=14,
              hosp_rate=0.05, icu_rate=0.02, vent_rate=0.02,
              hosp_los=7, icu_los=9, vent_los=10,
              pct_ped_vent=0.10):
    """

    :param scenario:
    :param population:
    :param known_infections:
    :param known_cases:
    :param market_share:
    :param n_days:
    :param doubling_time:
    :param relative_contact_rate:
    :param recovery_days:
    :param hosp_rate:
    :param icu_rate:
    :param vent_rate:
    :param hosp_los:
    :param icu_los:
    :param vent_los:
    :param pct_ped_vent:
    :return: projection, projection_admits, projection_census
    """

    # Store all input parameters in a dictionary to return later
    scenario_inputs = {'scenario': scenario,
                       'population': population,
                       'known_infections': known_infections,
                       'known_cases': known_cases,
                       'market_share': market_share,
                       'n_days': n_days,
                       'doubling_time': doubling_time,
                       'relative_contact_rate': relative_contact_rate,
                       'recovery_days': recovery_days,
                       'hosp_rate': hosp_rate,
                       'icu_rate': icu_rate,
                       'vent_rate': vent_rate,
                       'hosp_los': hosp_los,
                       'icu_los': icu_los,
                       'vent_los': vent_los,
                       'pct_ped_vent': pct_ped_vent}


    # Regional Population
    S = population

    # Currently Known Regional Infections (only used to compute detection rate
    # - does not change projections
    initial_infections = known_infections

    # Currently Hospitalized COVID-19 Patients
    current_hosp = known_cases

    market_share = market_share / 100


    # ------ Intermediate SIR model variables

    # Seems like estimating initial number of total infections in the population *region*
    # we are modeling (i.e. that we put population numbers in above) by inferring from the
    # number we have in hospital and then inflating by both our market share and then
    # the hospitalization rate of infecteds. So, total_infections is in our entire
    # region.

    total_infections = current_hosp / market_share / hosp_rate

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
           ) / S * (1 - relative_contact_rate)  # {rate based on doubling time} / {initial S}

    # Now can compute the "basic reproduction number". It's kind of like the
    # rho term in queueing models. When > 1, epidemic grows.
    r_t = beta / gamma * S  # r_t is r_0 after distancing
    r_naught = r_t / (1 - relative_contact_rate)
    doubling_time_t = 1 / np.log2(beta * S - gamma + 1)  # doubling time after distancing

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

    hosp = i * hosp_rate * market_share
    icu = i * icu_rate * market_share
    vent = i * vent_rate * market_share

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
    projection_admits = (projection.iloc[:-1, :] - projection.shift(1)).apply(np.ceil)
    projection_admits[projection_admits < 0] = 0
    projection_admits.loc[0, :] = 0

    plot_projection_days = n_days - 10
    projection_admits["day"] = range(projection_admits.shape[0])

    # ------ Compute census and other resource usage

    census_table, projection_census = _census_table(projection_admits,
                                                    hosp_los, icu_los, vent_los)

    # Add scenario info to result dataframes
    projection['scenario'] = scenario
    projection_admits['scenario'] = scenario
    projection_census['scenario'] = scenario

    projection_resources = _resource_table(projection_admits, projection_census,
                                           pct_ped_vent)
    # Return projections
    return (projection, projection_admits, projection_census,
            projection_resources, scenario_inputs)


# The following function I left as is from the UPenn model, except
# now returns daily census version as well as every 7 day
# version used in CHIME for the plot.
# We might want to have a separate function that does
# similar thing for any resources we add.
def _census_table(projection_admits, hosp_los, icu_los, vent_los):
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

    # Modified following lines to convert NaN to 0 in first row of census_df
    # and to return the full census_df along with the table that only contains
    # every 7 days.
    census_df.loc[0, :] = 0
    census_df.fillna(0, inplace=True)
    return census_table, census_df


def _resource_table(projection_admits, projection_census, pct_ped_vent) -> pd.DataFrame:
    """Use admissions, census, and base inputs to compute resource needs"""

    # Copy the census projections to use as base for resource projections
    projection_resources = projection_census.copy()

    census_rename_dict = {
        "hosp": 'hosp_census',
        "icu": 'icu_census',
        "vent": 'vent_census',
    }

    projection_resources = projection_resources.rename(census_rename_dict, axis='columns')
    print(projection_resources)

    dfs_to_concat = [projection_resources, projection_admits.iloc[:, 1:-1]]
    projection_resources = pd.concat(dfs_to_concat, axis=1)

    admit_rename_dict = {
        "hosp": 'hosp_admit',
        "icu": 'icu_admit',
        "vent": 'vent_admit',
    }
    projection_resources = projection_resources.rename(admit_rename_dict, axis='columns')

    # Computing number of pediatric and adult ventilators
    projection_resources['vent_census_ped'] = projection_resources['vent_census'] * pct_ped_vent

    projection_resources['vent_census_ped'] = \
        projection_resources['vent_census_ped'].map(lambda x: math.ceil(x))

    projection_resources['vent_census_adult'] = projection_resources['vent_census'] - projection_resources[
        'vent_census_ped']

    # Compute number of GPs needed - should this be based on census or admits?

    return projection_resources

