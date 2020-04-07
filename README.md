# Resources for COVID-19 hospital impact modelling

This repo is just a place store some notes and code related to c19
hospital impact modeling. Some of the work is based on the amazing CHIME
project:

* [Online hospital impact simulator](https://penn-chime.phl.io/)
* [https://github.com/CodeForPhilly/chime](https://github.com/CodeForPhilly/chime)
* [CHIME docs](https://code-for-philly.gitbook.io/chime/)
* [Announcing CHIME blog post](http://predictivehealthcare.pennmedicine.org/2020/03/14/accouncing-chime.html)

## A few of my projects

### chime_flow_resources_p1.ipynb (2020-04-02)

The goal for this notebook is to try to help people better understand the modeling principles, math and code behind the resource modeling in CHIME. It walks through how admits and census are computed for hospitalizations, ICU beds and vents. It also discusses some basic modeling issues related to using CHIME for assessing resource impacts of covid-19.

[chime_flow_resources_p1.ipynb](https://github.com/misken/c19/blob/master/mychime/modeling/chime_flow_resources_p1.ipynb)

**WIP** In part 2, I'm working on a queueing model based approximation for the census distribution over time. This will allow us to include census distribution bands instead of just a deterministic point
estimate of mean census. Still much to do but came up with nice way to model time dependent admits.

[chime_flow_resources_p2.ipynb](https://github.com/misken/c19/blob/master/mychime/modeling/chime_flow_resources_p2.ipynb)

### sim_chime_scenario_runner.py (updated 2020-04-07)

A simple Python module for working with the penn_chime model from the command line or as importable functions. 

Has it's own repo now: https://github.com/misken/sim_chime_scenario_runner

* A Jupyter notebook demo showing its use: [using_sim_chime_scenario_runner.ipynb](https://github.com/misken/sim_chime_scenario_runner/blob/master/demos/using_sim_chime_scenario_runner.ipynb)

* assumes that you've pip installed `penn_chime` either per https://github.com/CodeForPhilly/chime/pull/249 from a local clone of the chime repo or from pypi if it's eventually put up there
* [OPTIONAL] You can do a `pip install .` from the directory containing setup.py if you want to install into a virtual environment
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

### Model calibration/validation for new (2020-03-30) CHIME model

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

Had idea for adjusting census and admission sduring **early stages** of virus spread to deal with census at time 0 problem. 

Basic idea is that underlying epidemic has its dynamics that will play out almost independent of resources. But for capacity constrained resources it seems like there are a few phases during the early growth stage and then later stages of the virus. See my [modeling notes README page](https://github.com/misken/c19/tree/master/mychime/modeling).

### Cheat sheets for installing CHIME locally

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

## More resources related to COVID-19 modeling and analysis

### Johns Hopkins projects

* [https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19)
    - do git pull to get updated data including daily and time series (csv)
    - for US can get data both at state and county level 
    - [Dashboard](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)
    - links to Lancet article and many data sources
* [CSSE dept at JHU](https://systems.jhu.edu/)

## Articles, blog posts, vids

* [The IMHE COVID-19 model is fatally flawed](https://medium.com/@robertbracco1/the-ihme-covid19-model-is-dangerously-flawed-c19928464db1)
* [IHME - COVID-19 Projections](https://covid19.healthdata.org/projections) - paper describing methodology is [here](http://www.healthdata.org/research-article/forecasting-covid-19-impact-hospital-bed-days-icu-days-ventilator-days-and-deaths)
* [mathbabe post on covid-19](https://mathbabe.org/2020/03/30/comments-on-covid-19/)
* [Coronavirus modelers factor in new public health risk: Accusations their work is a hoax](https://www.washingtonpost.com/health/2020/03/27/coronavirus-models-politized-trump/)
* [A War Footing: Surfing the Curve](https://medium.com/swlh/a-war-footing-surfing-the-curve-f5ffe6134e37)
* [The Flaw of Averages in Flattening the Curve](https://www.probabilitymanagement.org/blog/2020/3/19/the-flaw-of-averages-in-flattening-the-curve)
* [A combination of coronavirus and the flaw of averages can drive you nuts](https://www.probabilitymanagement.org/blog/2020/1/30/a-combination-of-coronavirus-and-the-flaw-of-averages-can-drive-you-nuts)

## Kaggle data, kernels, challenges

* https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset
* https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks
...

## Other Covid19 data and simulators

* https://alhill.shinyapps.io/COVID19seir/
* https://metasd.com/2020/03/interactive-coronavirus-models/
* https://metasd.com/2020/03/community-coronavirus-model-bozeman/
* https://forio.com/app/jeroen_struben/corona-virus-covid19-seir-simulator/index.html#introduction.html
* http://covidsim.eu/
* https://www.hsye.org/covid-19-capacity-mgmt (Healthcare Systems Engineering Institute at Northeastern U.) 

## PySD

Simulating SD models in Python - https://pysd.readthedocs.io/en/master/

Can read Vensim .mdl files. They are just text files.

## INFORMS Forum post

This post appeared in March sometime in the [INFORMS](https://www.informs.org/) daily forum.

----- START -----
Multiple folks from the System Dynamics (SD) community have built models. Tom Fiddaman also made a video

Tom Fiddaman's model/video
metasd.com/2020/03/community-coronavirus-model-bozeman

Jeroen Struben's model
forio.com/app/jeroen_struben/...

Tom Fiddaman's review of Struben's model
metasd.com/2020/03/interactive-coronavirus-models

Tom Fiddaman's review of Jack Homer's COVID-19 model
metasd.com/2020/03/model-covid-19-us


Bob Eberlein's model

exchange.iseesystems.com/public/isee/covid-19-simulator/...
https://exchange.iseesystems.com/models/player/isee/covid-19-model


Bob Eberlein will be presenting his work this Friday, March 27th 2-3PM ET in a Worcester Polytechnic Institute (WPI) System Dynamics Collective Learning Meeting (CLM). I am waiting on details from him about the presentation. Please follow/join WPI SD for more info 

twitter.com/WPISDclub

www.linkedin.com/groups/1916314

Below is a link to sign up to be on the WPI System Dynamics Club mailing list:

eepurl.com/dzmA4j


Wish you and yours health and happiness!

Sincerely,

WPI System Dynamics Social Media Manager

Forgot to share the System Dynamics Society's page on COVID-19 with INFORMS folks...and I should share the INFORMS page on COVID-19 with SD folks
https://www.systemdynamics.org/covid-19

----- END -----



