# https://github.com/CodeForPhilly/chime/pull/249
# PR above describes how to install as a package and use both
# in CLI and module form

"""Command line interface."""

from argparse import (
    Action,
    ArgumentParser,
)
from datetime import datetime

from pandas import DataFrame

from penn_chime.constants import CHANGE_DATE
from penn_chime.parameters import Parameters, Disposition
from penn_chime.models import SimSirModel as Model
import penn_chime.cli as cli

import sys


def parse_args():
    """Parse args."""
    parser = ArgumentParser(description="SEMI-CHIME")
    parser.add_argument(
        "--scenario", type=str, default=datetime.now().strftime("%Y.%m.%d.%H.%M."),
        help="Prepended to output filenames."
    )
    parser.add_argument(
        "--output-path", type=str, default="", help="location for output file writing",
    )
    parser.add_argument("--file", type=str, help="CHIME config (cfg) file")
    parser.add_argument("--use-defaults", action='store_true',
                        help="If True, overrides --file and other args (default=False")

    parser.add_argument(
        "--scenarios", type=str,
        help="Undocumented feature: if not None, sim_chimes() function is called and a whole bunch of scenarios are run."
    )
    parser.add_argument("--quiet", action='store_true',
                        help="If True, suppresses output messages (default=False")

    return parser.parse_args()


def main():
    """Main."""
    my_args = parse_args()
    my_args_dict = vars(my_args)

    # Update sys.arg so we can call cli.parse_args()
    sys.argv = [sys.argv[0], '--file', my_args_dict['file']]

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

    m = Model(p)

    for df, name in (
        (m.sim_sir_w_date_df, "sim_sir_w_date"),
        (m.admits_df, "projected_admits"),
        (m.census_df, "projected_census"),
    ):
        df.to_csv(f"{p.current_date}_{name}.csv")


if __name__ == "__main__":
    main()
