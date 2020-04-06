## sim_chime_scenario_runner

**Note Monday 2020-04-06** - this script uses the `penn_chem.cli` module and right now
the CLI is a little out of sync with the web app. The two most recently
added parameters `mitigation-date` and `current-date` haven't yet made it into
the CLI on the `develop` branch. It looks like a fix was done yesterday and
that it should get merged shortly. For myself, I just hacked in the two new
parameters into the arg parser in `cli.py` until the fix goes live (just copied
and modifed the `add_argument` line from one of the other date args).

Here's a Jupyter notebook showing its use: [using_sim_chime_scenario_runner.ipynb](https://github.com/misken/c19/blob/master/mychime/scenario_runner/using_sim_chime_scenario_runner.ipynb)

A simple Python module for working with the penn_chime model
that: 

* assumes that you've pip installed `penn_chime` per https://github.com/CodeForPhilly/chime/pull/249 from a local clone of the chime repo
* allows running simulations from command line (like cli.py in penn_chime)
* is importable so can also run simulations via function call
* includes a few additional command line (or passable) arguments, including:
  - standard CHIME input config filename is a required input
  - a scenario name (prepended to output filenames)
  - output path
* after a simulation scenario is run, a results dictionary is created that contains:
  - the scenario name
  - the standard admits, census, and sim_sir_w_date dataframes
  - the dispositions dataframe
  - a dictionary containing the input parameters
  - a dictionary containing important intermediate variable values such as beta, doubling_time, ...
* writes out the results 
  - dataframes to csv
  - dictionaries to json
* (WIP) runs multiple scenarios corresponding to user specified ranges for one or more input variables.

I borrowed some code from the CHIME project (https://github.com/CodeForPhilly/chime) but did my best
to make my code easy to maintain if CHIME changes.

- created arg parser just for my added input parameters
- uses standard CHIME input config file
- call `penn_chime.cli.parse_args()` to parse the input config file
- the main simulation function signature is `sim_chime(scenario: str, p: Parameters):`
- `sim_chime()` returns a tuple containing the model object and the results dictionary described above.


