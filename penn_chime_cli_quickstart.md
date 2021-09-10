## Get started with the penn-chime CLI

### code-help-desk post by @jlubken on 2020-04-08 11:18 AM
* Install the module: `pip install .`
* Run `penn_chime --help`
* Look at the example `cli.cfg` in `./defaults/cli.cfg`
* Make sure that you set the `--current-date` and `--mitigation-date` appropriate for your scenario. Set either the `--date-first-hospitalized` XOR `--doubling-time`, not both.
