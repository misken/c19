"""
A combined CLI and callable version of the CHIME simulation model.

We adapted the CLI application in the CHIME project (https://github.com/CodeForPhilly/chime).

- added scenario and output_path parameters (separate from main Parameters object)
- added ability to use an input file, command line args, or DEFAULTS to instantiate model
- added ability to import this and call sim_chime() function from external apps so that we can run tons of scenarios over ranges of input parameters
- output is a dictionary of the standard CHIME dataframes as well as dictionaries
containing parameter and variable values.
- also writes out csvs
- it's in very early stages.

"""

from argparse import (
    Action,
    ArgumentParser,
)
from datetime import datetime

from pandas import DataFrame

from penn_chime.constants import CHANGE_DATE
from penn_chime.parameters import Parameters, Disposition
from penn_chime.models import SimSirModel as Model
import penn_chime.models as models
import penn_chime.cli as cli

import sys
import json


def parse_args():
    """Parse args."""
    parser = ArgumentParser(description="SEMI-CHIME")
    parser.add_argument("file", type=str, help="CHIME config (cfg) file")
    parser.add_argument(
        "--scenario", type=str, default=datetime.now().strftime("%Y.%m.%d.%H.%M."),
        help="Prepended to output filenames. (default is current datetime)"
    )
    parser.add_argument(
        "--output-path", type=str, default="", help="location for output file writing",
    )

    parser.add_argument(
        "--scenarios", type=str,
        help="Undocumented feature: if not None, sim_chimes() function is called and a whole bunch of scenarios are run."
    )
    parser.add_argument("--quiet", action='store_true',
                        help="If True, suppresses output messages (default=False")

    return parser.parse_args()


def sim_chime(scenario: str, p: Parameters
              ):
    """
    Run one chime simulation.

    If `params` is not None, then it is used to initialize all parameters. Any
    parameter values set to something other than None in the following
    optional args will update that parameter value. If `params` is None, then
    all additional args must be other than None.

    :param scenario:
    :param p:
    """


    input_params_dict = vars(p)

    # Run the model
    m = Model.SimSirModel(p)

    # Gather results
    results = gather_sim_results(m, sim_scenario, input_params_dict)
    return results


def write_results(rslt, sim_scenario, out):

    # Results dataframes
    for df, name in (
        (rslt["raw_sir_df"], "raw_sir"),
        (rslt["dispositions_df"], "dispositions"),
        (rslt["admits_df"], "admits"),
        (rslt["census_df"], "census"),
    ):
        df.to_csv(out + sim_scenario + '_' + name + ".csv", index=False)

    # Variable dictionaries
    with open(out + sim_scenario + "_inputs.json", "w") as f:
        json.dump(rslt['input_params_dict'], f)

    with open(out + sim_scenario + "_key_vars.json", "w") as f:
        json.dump(rslt['intermediate_variables_dict'], f)


def gather_sim_results(m, scenario, input_params_dict):

    # Get the output dfs
    # raw_sir_df = m.raw_df
    # dispositions_df = m.dispositions_df
    # admits_df = m.admits_df
    # census_df = m.census_df

    # Get key input/output variables
    intrinsic_growth_rate = m.intrinsic_growth_rate
    gamma = m.gamma     # Recovery rate
    beta = m.beta       # Contact rate

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
        'scenario': scenario,
        'input_params_dict': input_params_dict,
        'intermediate_variables_dict': intermediate_variables,
        'raw_sir_df': m.raw_df,
        'dispositions_df': m.dispositions_df,
        'admits_df': m.admits_df,
        'census_df': m.census_df,
    }
    return results


def sim_chimes(scenarios: str, params: Parameters = None,
               current_hospitalized: int = None,
               doubling_time: float = None,
               known_infected: int = None,
               relative_contact_rate: float = None,
               susceptible: int = None,
               hospitalized: RateLos = None,
               icu: RateLos = None,
               ventilated: RateLos = None,
               market_share: float = None,
               n_days: int = None,
               recovery_days: float = None,
               ):
    """
    Run many chime simulations.

    If `params` is not None, then it is used to initialize all parameters. Any
    parameter values set to something other than None in the following
    optional args will update that parameter value. If `params` is None, then
    all additional args must be other than None. These settings are just
    for the base parameter values. We can run stuff over ranges as we see it.

    :param scenarios:
    :param params:
    :param current_hospitalized:
    :param doubling_time:
    :param known_infected:
    :param relative_contact_rate:
    :param susceptible:
    :param hospitalized:
    :param icu:
    :param ventilated:
    :param market_share:
    :param n_days:
    :param recovery_days:
    :return:
    """

    if params is not None:
        params_dict = vars(params)
    else:
        params_dict = {"current_hospitalized": None,
                       "doubling_time": None,
                       "known_infected": None,
                       "relative_contact_rate": None,
                       "susceptible": None,
                       "hospitalized": None,
                       "icu": None,
                       "ventilated": None,
                       "market_share": None,
                       "n_days": None,
                       "recovery_days": None,
                       }

    # Check for parameter updates passed
    vals_passed = {key: value for (key, value) in vars().items()
                   if key not in ['scenario', 'params']}

    for key, value in vals_passed.items():
        if value is not None:
            params_dict[key] = value

    # Create Parameters object
    p = Parameters(
        current_hospitalized=params_dict['current_hospitalized'],
        doubling_time=params_dict['doubling_time'],
        known_infected=params_dict['known_infected'],
        market_share=params_dict['market_share'],
        n_days=params_dict['n_days'],
        relative_contact_rate=params_dict['relative_contact_rate'],
        susceptible=params_dict['susceptible'],
        hospitalized=params_dict['hospitalized'],
        icu=params_dict['icu'],
        ventilated=params_dict['ventilated'],
    )

    base_input_params_dict = vars(p)

    # Create a range of social distances

    soc_dists = np.arange(0.05, 0.60, 0.05)
    # array([0.05, 0.1 , 0.15, 0.2 , 0.25, 0.3 , 0.35, 0.4 , 0.45, 0.5 , 0.55,
    #        0.6 , 0.65, 0.7 , 0.75, 0.8 , 0.85])

    num_scenarios = len(soc_dists)

    # We can store outputs any way we want. For this demo, just going to
    # use a master list. # This will be a list of dicts of the
    # result dataframes (+ 1 dict containing the scenario inputs)

    results_list = []

    for sdpct in soc_dists:
        sim_scenario = '{}{:.0f}'.format(scenarios, 100 * sdpct)

        # Update the parameters for this scenario
        p.relative_contact_rate = sdpct
        input_params_dict = vars(p)

        # Run the model
        m = SimSirModel(p)

        # Gather results
        results = gather_sim_results(m, sim_scenario, input_params_dict)

        # Append results to results list

        results_list.append(results.copy())

    return results_list


if __name__ == "__main__":
    my_args = parse_args()
    my_args_dict = vars(my_args)

    # Update sys.arg so we can call cli.parse_args()
    sys.argv = [sys.argv[0], '--file', my_args_dict['file']]

    scenario = my_args.scenario
    output_path = my_args.output_path

    # Read chime params from configuration file
    a = cli.parse_args()

    p = Parameters(
        current_hospitalized=a.current_hospitalized,
        date_first_hospitalized=a.date_first_hospitalized,
        doubling_time=a.doubling_time,
        infectious_days=a.infectious_days,
        market_share=a.market_share,
        n_days=a.n_days,
        relative_contact_rate=a.relative_contact_rate,
        population=a.population,

        hospitalized=Disposition(a.hospitalized_rate, a.hospitalized_days),
        icu=Disposition(a.icu_rate, a.icu_days),
        ventilated=Disposition(a.ventilated_rate, a.ventilated_days),
    )

    if my_args.scenarios is None:
        # Just running one scenario
        results = sim_chime(scenario, p)

        if not a.quiet:
            print("Scenario: {}\n".format(results['scenario_str']))
            print("\nInput parameters")
            print("{}".format(50 * '-'))
            print(json.dumps(results['input_params_dict'], indent=4, sort_keys=False))

            print("\nIntermediate variables")
            print("{}".format(50 * '-'))
            print(json.dumps(results['intermediate_variables_dict'], indent=4, sort_keys=False))
            print("\n")

        write_results(results, scenario, output_path)
    else:
        # Running a bunch of scenarios using sim_chimes()
        results_list = sim_chimes(a.scenarios, p)

        for results in results_list:
            sim_scenario = results['scenario_str']
            if not a.quiet:
                print("Scenario: {}\n".format(results['scenario_str']))
                print("\nInput parameters")
                print("{}".format(50 * '-'))
                print(json.dumps(results['input_params_dict'], indent=4, sort_keys=False))

                print("\nIntermediate variables")
                print("{}".format(50 * '-'))
                print(json.dumps(results['intermediate_variables_dict'], indent=4, sort_keys=False))
                print("\n")

            write_results(results, sim_scenario, output_path)

"""
MIT License

Copyright (c) 2020 Mark Isken
Copyright (c) 2020 The Trustees of the University of Pennsylvania

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


