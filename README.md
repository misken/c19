# Resources for COVID-19 hospital impact modelling

This repo is just a place to store some links, notes, code and other resources related to c19
hospital impact modeling work I'm doing. Some of the work is based on the CHIME
project at UPenn.

## CHIME related links

* [Online hospital impact simulator](https://penn-chime.phl.io/) - v1.1.5 (2020-04-08) still running
* [https://github.com/CodeForPhilly/chime](https://github.com/CodeForPhilly/chime) 
* [Bayes CHIME](https://github.com/pennsignals/chime_sims) - all public facing activity appears ceased
* [CHIME docs](https://code-for-philly.gitbook.io/chime/)
* [CHIME pub in Annals of Internal Medicine](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7153364/)
* [#covid19-chime-penn Slack channel](https://codeforphilly.org/chat/covid19-chime-penn)
* [Announcing CHIME blog post](http://predictivehealthcare.pennmedicine.org/2020/03/14/accouncing-chime.html)

## Other prominent Covid-19 models

### Imperial College of London

* [Main reports page](https://www.imperial.ac.uk/mrc-global-infectious-disease-analysis/covid-19/covid-19-reports/)
* [State level model explainer page](https://mrc-ide.github.io/covid19usa/#/)
* [Nature paper - June 2020](https://www.nature.com/articles/s41586-020-2405-7.pdf)
* [Report 13 - Flaxman](https://www.imperial.ac.uk/mrc-global-infectious-disease-analysis/covid-19/report-13-europe-npi-impact/)
* [State level tracking in the US](https://www.medrxiv.org/content/10.1101/2020.07.13.20152355v1.full.pdf)
* [Source code for Report 13 state level model](https://github.com/ImperialCollegeLondon/covid19model)
* [Source code for Report 9 microsimulation model](https://github.com/mrc-ide/covid-sim)
* [Report 9 - Ferguson](https://www.imperial.ac.uk/mrc-global-infectious-disease-analysis/covid-19/report-9-impact-of-npis-on-covid-19/)

### IHME model

* [IHME - COVID-19 Projections](https://covid19.healthdata.org/projections) - paper describing methodology is [here](http://www.healthdata.org/research-article/forecasting-covid-19-impact-hospital-bed-days-icu-days-ventilator-days-and-deaths)
* [America’s most influential coronavirus model just revised its estimates downward. But not every model agrees.](https://www.washingtonpost.com/health/2020/04/06/americas-most-influential-coronavirus-model-just-revised-its-estimates-downward-not-every-model-agrees/)
* [The IMHE COVID-19 model is fatally flawed](https://medium.com/@robertbracco1/the-ihme-covid19-model-is-dangerously-flawed-c19928464db1)

## Some of my work

Jump to:
* [modeling multiple mitigation dates and relative contact rates](#dynamic-relative-contact-rates) - added functionality to `sim_chime_scenario_runner` to model relative contact rates that change over time as social distancing policies change.
* [chime_flow_resources_p2 notebook](#chime_flow_resources_p2) - a queueing based approach to census modeling in CHIME
* [Impact of mitigation date, contact rate, infectious days on projection accuracy](#impact-of-mitigation-date-contact-rate-infectious-days-on-projection-accuracy) - scenario analysis
* [`sim_chime_scenario_runner`](#sim_chime_scenario_runnerpy) - CHIME wrapper (Python) that can be used from command line or as importable library
* [chime_flow_resources_p1 notebook](#chime_flow_resources_p1) - modeling principles, math and code behind the resource modeling in CHIME
* [Early model calibration/validation](#early-model-calibration-and-validation) - comparison of actual hospital admits to projections during early growth phase of virus
* [Download and prep NY Times Covid-19 data](#jupyter-notebook-for-downloading-covid-19-time-series-data) - state and county level data
* [Capacity driven census and admission adjustments to CHIME model](#capacity-driven-census-and-admission-adjustments-to-chime-model) - idea notes
* [Cheat sheet for installing CHIME locally](#cheat-sheet-for-installing-chime-locally)



## More resources related to COVID-19 modeling and analysis

### Johns Hopkins projects

* [https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19)
    - do git pull to get updated data including daily and time series (csv)
    - for US can get data both at state and county level 
    - [Dashboard](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)
    - links to Lancet article and many data sources
* [CSSE dept at JHU](https://systems.jhu.edu/)

## Articles, blog posts, vids

* https://www.nytimes.com/interactive/2020/05/12/upshot/coronavirus-models.html
* [Inside a Chicago hospital built to deal with a pandemic](https://www.washingtonpost.com/video/national/health-science/inside-a-chicago-hospital-built-to-deal-with-a-pandemic/2020/04/09/c09e900a-91af-4292-b480-4bc6946eed54_video.html)
* [mathbabe post on covid-19](https://mathbabe.org/2020/03/30/comments-on-covid-19/)
* [Coronavirus modelers factor in new public health risk: Accusations their work is a hoax](https://www.washingtonpost.com/health/2020/03/27/coronavirus-models-politized-trump/)
* [A War Footing: Surfing the Curve](https://medium.com/swlh/a-war-footing-surfing-the-curve-f5ffe6134e37)
* [The Flaw of Averages in Flattening the Curve](https://www.probabilitymanagement.org/blog/2020/3/19/the-flaw-of-averages-in-flattening-the-curve)
* [A combination of coronavirus and the flaw of averages can drive you nuts](https://www.probabilitymanagement.org/blog/2020/1/30/a-combination-of-coronavirus-and-the-flaw-of-averages-can-drive-you-nuts)



## Other Covid19 data and simulators

* https://www.covid19sim.org/ (MIT, Ga Tech, Harvard) - Shiny App
* https://covidtracking.com/ - state level data including testing and grades
* https://alhill.shinyapps.io/COVID19seir/
* https://metasd.com/2020/03/interactive-coronavirus-models/
* https://metasd.com/2020/03/community-coronavirus-model-bozeman/
* https://forio.com/app/jeroen_struben/corona-virus-covid19-seir-simulator/index.html#introduction.html
* http://covidsim.eu/
* https://www.hsye.org/covid-19-capacity-mgmt (Healthcare Systems Engineering Institute at Northeastern U.) 

## Systems dynamics modeling in Python

Simulating SD models in Python - https://pysd.readthedocs.io/en/master/

Can read Vensim .mdl files. They are just text files.

## Agent based modeling in Python

Mesa - https://github.com/projectmesa/mesa and https://mesa.readthedocs.io/en/master/index.html

## Some project work

### Dynamic relative contact rates

Added ability to specify multiple mitigation dates and associated relative contact rate values.
See [demo notebook](https://github.com/misken/sim_chime_scenario_runner/blob/master/demos/dynamic_rcr_runner.ipynb) for details. This should be useful for projecting impact of various changes in social distancing policies.

**WARNING** - NEEDS TESTING AND VALIDATION - IDEA SEEMS REASONABLE - USE AT YOUR OWN RISK

### Impact of mitigation date, contact rate, infectious days on projection accuracy

I wanted to see how sensitive the CHIME projections are to values of the
key input variables. Using my [sim_chime_scenario_runner](https://github.com/misken/sim_chime_scenario_runner) tool, I ran 560 scenarios based on the following ranges for each input factor:

* `mitigation-date` : 2020-03-21 through 2020-03-27
* `relative-contact-rate` : 0.05 to 0.80 in 0.05 increments
* `infectious-days` : 8, 9, 10, 11 and 12 days

[R based analysis knitted to pdf](https://drive.google.com/file/d/170-AwiHZ1l4ORhaIG-SebY-ZYJJDZmC0/view?usp=sharing)

### chime_flow_resources_p1

**Created:** 2020-04-02

The goal for this notebook is to try to help people better understand the modeling principles, math and code behind the resource modeling in CHIME. It walks through how admits and census are computed for hospitalizations, ICU beds and vents. It also discusses some basic modeling issues related to using CHIME for assessing resource impacts of covid-19.

[chime_flow_resources_p1.ipynb](https://github.com/misken/c19/blob/master/mychime/modeling/chime_flow_resources_p1.ipynb)

### chime_flow_resources_p2

In part 2, I developed a queueing model based approximation for the census distribution over time. This will allow us to include census distribution bands instead of just a deterministic point
estimate of mean census. 

[chime_flow_resources_p2.ipynb](https://github.com/misken/c19/blob/master/mychime/modeling/chime_flow_resources_p2.ipynb)

### sim_chime_scenario_runner.py 

**Updated 2020-04-08 for consistency with penn-chime v1.1.3**

**NOTE** - Input parameter file for CHIME has a few changes. See https://github.com/misken/sim_chime_scenario_runner.

A simple Python module for working with the penn_chime model from the command line or as importable functions. 

Has its own repo now: https://github.com/misken/sim_chime_scenario_runner

* A Jupyter notebook demo showing its use: [using_sim_chime_scenario_runner.ipynb](https://github.com/misken/sim_chime_scenario_runner/blob/master/demos/using_sim_chime_scenario_runner.ipynb)

* assumes that you've pip installed `penn_chime` per [these instructions](https://github.com/misken/c19/blob/master/penn_chime_cli_quickstart.md)
* [OPTIONAL] You can do a `pip install .` of `sim_chime_scenario_runner` from the directory containing setup.py if you want to install into a virtual environment
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

### Early model calibration and validation

**Based on CHIME model as of 2020-03-30**

I took our actual admits (from 2020-02-20 to a 2020-03-25) and just fit an exponential growth model, got the implied growth rate and implied doubling time. Plotted actual admits vs predicted (just using simple exp growth model) and got very nice fit. Then used implied doubling time of 3.61 in CHIME model and got spot on match with the exponential fit to admits and thus, to the actual admits. Super happy to see this!

You can see the results in this notebook: [model_calibration_validation.ipynb](https://github.com/misken/c19/blob/master/mychime/calibration_validation/model_calibration_validation.ipynb)

### Jupyter notebook for downloading COVID-19 time series data

Downloads latest time series data from https://github.com/nytimes/covid-19-data

- does a bunch of data wrangling to create global as well as US datasets (at county and state level) that are amenable to analysis
- all dataframes are created both in semi-wide and long forms. The semi-wide forms have been date melted but contain separate columns for confirmed, deaths, and recovered. The long forms are measure melted in addition to date melted.
- csvs explorted to path of your choosing
- basic line plot at bottom for demo.

https://github.com/misken/c19/blob/master/get_c19_data_nytimes.ipynb

### Capacity driven census and admission adjustments to CHIME model

Had idea for adjusting census and admission during **early stages** of virus spread to deal with census at time 0 problem. 

Basic idea is that underlying epidemic has its dynamics that will play out almost independent of resources. But for capacity constrained resources it seems like there are a few phases during the early growth stage and then later stages of the virus. See my [modeling notes README page](https://github.com/misken/c19/tree/master/mychime/modeling).

### Cheat sheet for installing CHIME locally

The docs for CHIME are great. I created this to help folks with limited
exposure to this kind of stuff get CHIME installed in either Windows or Linux.
The hospital based analysts we are trying to help with this work are all on Windows. 

https://github.com/misken/c19/tree/master/mychime/docs

### Jupyter notebook version of early CHIME model

**NOTE: This was based on a very early version of the CHIME model. Nevertheless,
the comments might still be useful to someone trying to understand the basic
logic of the model. It should NOT be used for actual work.**

I've added tons of code comments and other descriptive text throughout the notebook to help others understand exactly how this works and how we might adapt it for our use.

https://github.com/misken/c19/blob/master/mychime/archive/chime_earlyversion_annotated.ipynb



