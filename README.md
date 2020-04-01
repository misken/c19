# Resources for COVID-19 hospital impact modelling

This repo is just a place store some notes and code related to c19
hospital impact modeling. Some of the work is based on the amazing CHIME
project done by the folks at [UPenn's Predictive Healthcare group](http://predictivehealthcare.pennmedicine.org/) and
the [CodeForPhilly CHIME project](https://codeforphilly.org/projects/chime). 

## CHIME project

* [Online hospital impact simulator](https://penn-chime.phl.io/)
* [https://github.com/CodeForPhilly/chime](https://github.com/CodeForPhilly/chime)
* [CHIME docs](https://code-for-philly.gitbook.io/chime/)
* [Announcing CHIME blog post](http://predictivehealthcare.pennmedicine.org/2020/03/14/accouncing-chime.html)

## Some stuff I created that's in this repo

### Model calibration/validation for new (2020-03-30) CHIME model

This version deals with the census at time 0 problem by doing something similar to the idea sketched below. It minimizes squared error loss between actual and predicted census to find implied doubling time (given first actual admit date) or implied first admit (given a doubling time). 

So, I took our actual admits (from 2/20/2020 to a few days ago) and just fit an exponential growth model, got the implied growth rate and implied doubling time. Plotted actual admits vs predicted (just using simple exp growth model) and got very nice fit. Then used implied doubling time of 3.61 in CHIME model and got spot on match with the exponential fit to admits and thus, to the actual admits. Super happy to see this!

You can see the results in this notebook: [model_calibration_validation.ipynb](https://github.com/misken/c19/blob/master/mychime/calibration_validation/model_calibration_validation.ipynb)

### Capacity driven census and admission adjustments to CHIME model

Had idea for adjusting census and admission sduring **early stages** of virus spread to deal with census at time 0 problem. 

Basic idea is that underlying epidemic has its dynamics that will play out almost independent of resources. But for capacity constrained resources it seems like there are a few phases during the early growth stage and then later stages of the virus. Let's just use hospital beds as the example resource.

#### growth phase - haven't hit capacity yet and epidemic in exponential growth phase

In this phase, we have the "zero census" problem with the underlying model. But if we are in growth phase, should be easy to just solve for $t_{0}^{*} \lt t_0$ in the basic exponential growth equation to "reconstruct" the admission history and use that along with LOS to compute census for the period $(t_{0}^{*}, t_0)$ and thus have a better estimate of starting census at $t_0$ as well as decent approximation of the mix of how far along those patients are in there stay to better model them leaving - as opposed to assuming all patients at $t_0$ just started there stay, which causes a weird census spike at start of model projections.

**NOTE (2020-03-29)** Looks like Issue [#255](https://github.com/CodeForPhilly/chime/issues/255) is going to address this and go live on Monday, 2020-03-30. Implemented solution is to:

* have user enter day of first covid admit (in addition to current number in hospital)
* use brute force line search to find doubling time that minimizes squared error loss between actual and  predicted census at current time.

Approach makes sense and has benefit of only one additional user input. Hospitals will be happy. 

A complication is that the virus grew at intrinsic growth rate for a while and then
when social distancing started, grew at implied growth rate. Hmm, I wonder if this
matters? 

Hacked around in Excel so I could see what I was doing and this appears to make some sense for this phase. Talking
it through with a few colleagues and then Pythonizing it as a post-processing tool that can be used
with standard CHIME output and as few as possible new user inputs.

See 'model' sheet in [explore_census_adj.xlsx](https://github.com/misken/c19/blob/master/mychime/modeling/explore_census_adj.xlsx).

#### flat phase - at capacity

I'm guessing we are going to hit capacity constraints well before epidemic passes inflection point
in the standard logistic model of its exponential spread and then eventual slowing growth.

At this stage, no matter how many admits predicting by underlying SIR model, we have our max admission rate, $A^{*}$ and max census $C^{*}$. We will stay in this state until the underlying SIR model has admission rate $A \lt A^{*}$. So, resource use is flat, though there will be much adaptive behavior
by hospitals as they cope with insufficient resources which will likely affect recovery rates,
death rates, and resource use rates.

#### decay phase

When $A \lt A^{*}$, the underlying growth rate in the epidemic must be slowing and now, we can use $A$ to compute census in normal way.

### Plan

I'm going to try to put a procedure together that uses standard outputs from the current chime model to implement these ideas. It would likely require user to input capacity for each resource being modelled (will just start with beds).


### sim_chime_scenario_runner.py (WIP)

We adapted the CLI application in the CHIME project (https://github.com/CodeForPhilly/chime).

- added scenario and output_path parameters (separate from main Parameters object)
- uses standard CHIME input config file
- added ability to import this and call sim_chime() function from external apps so that we can run tons of scenarios over ranges of input parameters
- output is a dictionary of the standard CHIME dataframes as well as dictionaries
containing parameter and variable values.
- also writes out csvs of the dataframes and json for the dictionaries


### Cheat sheets for installing CHIME locally

The docs for CHIME are great. I created this to help folks with limited
exposure to this kind of stuff get CHIME installed in either Windows or Linux.
The hospital based analysts we are trying to help with this work are all on Windows. 

https://github.com/misken/c19/tree/master/mychime/docs

### Jupyter notebook version of early CHIME model

**NOTE: This was based on a very early version of the CHIME model. Nevertheless,
the comments might still be useful to someone trying to understand the basic
logic of the model.**

I've added tons of code comments and other descriptive text throughout the notebook to help others understand exactly how this works and how we might adapt it for our use.

https://github.com/misken/c19/blob/master/mychime/chime_earlyversion_annotated.ipynb

### Jupyter notebook for downloading COVID-19 time series data

Downloads latest time series data from https://github.com/nytimes/covid-19-data

NOTE: Using NY Times data for now while some issues getting ironed out with the JH data

- does a bunch of data wrangling to create global as well as US datasets (at county and state level) that are amenable to analysis
- all dataframes are created both in semi-wide and long forms. The semi-wide forms have been date melted but contain separate columns for confirmed, deaths, and recovered. The long forms are measure melted in addition to date melted.
- csvs explorted to path of your choosing
- basic line plot at bottom for demo.

https://github.com/misken/c19/blob/master/get_c19_data_nytimes.ipynb

## Johns Hopkins projects

* [https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19)
    - do git pull to get updated data including daily and time series (csv)
    - for US can get data both at state and county level 
    - [Dashboard](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)
    - links to Lancet article and many data sources
* [CSSE dept at JHU](https://systems.jhu.edu/)

## Articles, blog posts, vids

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


## PySD

Simulating SD models in Python - https://pysd.readthedocs.io/en/master/

Can read Vensim .mdl files. They are just text files.



