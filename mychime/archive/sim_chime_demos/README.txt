Running CHIME scenarios
=======================

Modifications
-------------

v0.01 - 2020-03-23
^^^^^^^^^^^^^^^^^^

* Added demo of adding new resource. I did a partition of vent into adult and ped using a new parameter pct_ped_vent.
    - function is called _resource_table()
    - added new parameter at top
    - output csvs now include the resource table to give idea of what that could look like
    - the _resource_table function is a great place to add other new resource logic as I first create a dataframe that combines the cencus and admits columns so that you can use any combination of them you'd like to compute something new.

Main overview
-------------

Wanted to create framework to make it easy to run the CHIME model
for one or many scenarios. Here's first demo of the idea. I did
the following:

* put the sir() and sim_sir() functions into its own module called sim_sir.py
* created a function called sim_chime() and saved in its own module called sim_chime.py
    - this function takes as inputs all the base parameters and runs sim_sir() one time with those inputs
    - returns a tuple containing the projection, projection_admits, and projection_census dataframes as well as a dictionary containing the scenario_inputs
* created a demo "chime sim runner" called run_sim_chime.py.
    - this is the only file you need to actually look at and edit/run.
    - you'll see that it's got all the base input variables at the top. 
    - then I demo how you call sim_chime() to run a single scenario
    - then I demo how you could call sim_chime() within a loop to run a bunch of scenarios. For example, right now I have it run for a range of social distances. 
    - right now I have it output csv files that contain the results for all scenarios with a column containing the scenario name.
    - it also gathers all the results into a list of dictionaries and obviously we can post-process anyway we want.
    - it's all commented and pretty straight forward.
    
BOTTOM LINE: If you simply run run_sim_chime.py, e.g. 

>>> python run_sim_chime.py

and look in the output/ folder you'll see the result files. Then go through run_sim_chime.py as this is just a demo and this is the file that people would be modifying and extending.

Be really nice if there was someone who knew enough Python (or R) and had the bandwidth to start working on code that would post process the csv files this creates and turns them into summary tables and plots. Again, this is just a first demo and we can easily change the inputs and outputs as this evolves.
