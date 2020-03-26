"""
Command line interface.
"""

from argparse import (
    Action,
    ArgumentParser,
)

from datetime import datetime

from penn_chime.settings import DEFAULTS
from penn_chime.parameters import Parameters
from penn_chime.models import SimSirModel
from penn_chime.utils import RateLos

import json


class FromFile(Action):
    """From File."""

    def __call__(self, parser, namespace, values, option_string=None):
        with values as f:
            parser.parse_args(f.read().split(), namespace)


def validator(cast, min_value, max_value):
    """Validator."""

    def validate(string):
        """Validate."""
        value = cast(string)
        if min_value is not None:
            assert value >= min_value
        if max_value is not None:
            assert value <= max_value
        return value

    return validate


def parse_args():
    """Parse args."""
    parser = ArgumentParser(description="CHIME-SEMI")

    parser.add_argument("--file", type=open, action=FromFile)
    parser.add_argument("--use-defaults", action='store_true',
                        help="If True, overrides --file and other args (default=False")
    parser.add_argument(
        "--output-path", type=str, default="", help="location for output file writing",
    )
    parser.add_argument(
        "--scenario", type=str, default=datetime.now().strftime("%Y.%m.%d.%H.%M."),
        help="Prepended to output filenames."
    )
    parser.add_argument("--quiet", action='store_true',
                        help="If True, suppresses output messages (default=False")

    for arg, cast, min_value, max_value, help in (
        (
            "--current-hospitalized",
            int,
            0,
            None,
            "Currently Hospitalized COVID-19 Patients (>= 0)",
        ),
        (
            "--doubling-time",
            float,
            0.0,
            None,
            "Doubling time before social distancing (days)",
        ),
        ("--hospitalized-los", int, 0, None, "Hospitalized Length of Stay (days)"),
        (
            "--hospitalized-rate",
            float,
            0.00001,
            1.0,
            "Hospitalized Rate: 0.00001 - 1.0",
        ),
        ("--icu-los", int, 0, None, "ICU Length of Stay (days)"),
        ("--icu-rate", float, 0.0, 1.0, "ICU Rate: 0.0 - 1.0"),
        (
            "--known-infected",
            int,
            0,
            None,
            "Currently Known Regional Infections (>=0) (only used to compute detection rate - does not change projections)",
        ),
        (
            "--market_share",
            float,
            0.00001,
            1.0,
            "Hospital Market Share (0.00001 - 1.0)",
        ),
        ("--n-days", int, 0, None, "Nuber of days to project >= 0"),
        (
            "--relative-contact-rate",
            float,
            0.0,
            1.0,
            "Social Distancing Reduction Rate: 0.0 - 1.0",
        ),
        ("--susceptible", int, 1, None, "Regional Population >= 1"),
        ("--ventilated-los", int, 0, None, "Hospitalized Length of Stay (days)"),
        ("--ventilated-rate", float, 0.0, 1.0, "Ventilated Rate: 0.0 - 1.0"),
    ):
        parser.add_argument(arg, type=validator(cast, min_value, max_value))
    return parser.parse_args()


def sim_chime(p, scenario):

    input_params_dict = vars(p)

    # Run the model
    m = SimSirModel(p)

    # Get the output dfs
    raw_sir_df = m.raw_df
    dispositions_df = m.dispositions_df
    admits_df = m.admits_df
    census_df = m.census_df

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
        'scenario_str': scenario,
        'input_params_dict': input_params_dict,
        'intermediate_variables_dict': intermediate_variables,
        'raw_sir_df': m.raw_df,
        'dispositions_df': m.dispositions_df,
        'admits_df': m.admits_df,
        'census_df': m.census_df,
    }
    return results


def write_results(rslt, scen, out):

    # Results dataframes
    for df, name in (
        (rslt["raw_sir_df"], "raw_sir"),
        (rslt["dispositions_df"], "dispositions"),
        (rslt["admits_df"], "admits"),
        (rslt["census_df"], "census"),
    ):
        df.to_csv(out + scen + '_' + name + ".csv", index=False)

    # Variable dictionaries
    with open(out + scen + "_inputs.json", "w") as f:
        json.dump(rslt['input_params_dict'], f)

    with open(out + scen + "_key_vars.json", "w") as f:
        json.dump(rslt['intermediate_variables_dict'], f)


if __name__ == "__main__":
    a = parse_args()
    scenario = a.scenario
    output_path = a.output_path

    if a.use_defaults:
        p = Parameters(
            current_hospitalized=DEFAULTS.current_hospitalized,
            doubling_time=DEFAULTS.doubling_time,
            known_infected=DEFAULTS.known_infected,
            market_share=DEFAULTS.market_share,
            n_days=DEFAULTS.n_days,
            relative_contact_rate=DEFAULTS.relative_contact_rate,
            susceptible=DEFAULTS.region.susceptible,
            hospitalized=RateLos(DEFAULTS.hospitalized.rate,
                                 DEFAULTS.hospitalized.length_of_stay),
            icu=RateLos(DEFAULTS.icu.rate,
                        DEFAULTS.icu.length_of_stay),
            ventilated=RateLos(DEFAULTS.ventilated.rate,
                               DEFAULTS.ventilated.length_of_stay),
        )
    else:
        p = Parameters(
            current_hospitalized=a.current_hospitalized,
            doubling_time=a.doubling_time,
            known_infected=a.known_infected,
            market_share=a.market_share,
            n_days=a.n_days,
            relative_contact_rate=a.relative_contact_rate,
            susceptible=a.susceptible,
            hospitalized=RateLos(a.hosp_rate, a.hosp_los),
            ventilated=RateLos(a.vent_rate, a.vent_los),
        )

    results = sim_chime(p, scenario)

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


