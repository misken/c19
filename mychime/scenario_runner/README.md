## sim_chime_scenario_runner

I wanted to have a simple Python module for working with the penn_chime model
that: 

* allowed running simulations from command line (like cli.py in penn_chime)
* allowed running simulations from custom Python function calls
* included a few additional command line (or passable) arguments, including:
  - standard CHIME input config filename is a required input
  - a scenario name (prepended to output filenames)
  - output path
* after a simulation scenario was run, a results dictionary is created that contains:
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
- call penn_chime.cli.parse_args() to parse the input config file
- the main simululation function signature is `sim_chime(scenario: str, p: Parameters):`
- `sim_chime()` returns a tuple containing the model object and the results dictionary described above.

Here's a Jupyter notebook showing its use: [using_sim_chime_scenario_runner.ipynb]()
