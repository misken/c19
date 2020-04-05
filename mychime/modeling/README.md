# CHIME modeling related notes and projects

## chime_flow_resources_p1.ipynb (2020-04-02)

The goal for this notebook is to try to help people better understand the modeling principles, math and code behind the resource modeling in CHIME. It walks through how admits and census are computed for hospitalizations, ICU beds and vents. It also discusses some basic modeling issues related to using CHIME for assessing resource impacts of covid-19.

[chime_flow_resources_p1.ipynb](https://github.com/misken/c19/blob/master/mychime/modeling/chime_flow_resources_p1.ipynb)

## sim_chime_scenario_runner.py (2020-04-01)

A simple Python module for working with the penn_chime model from the command line or as importable functions. More details below and at following:

* A Jupyter notebook demo showing its use: [using_sim_chime_scenario_runner.ipynb](https://github.com/misken/c19/blob/master/mychime/scenario_runner/using_sim_chime_scenario_runner.ipynb)

**Note**: Assumes that you've pip installed `penn_chime` per https://github.com/CodeForPhilly/chime/pull/249 from a local clone of the chime repohttps://github.com/misken/c19

## Model calibration/validation for new (2020-03-30) CHIME model

So, I took our actual admits (from 2020-02-20 to a 2020-03-25) and just fit an exponential growth model, got the implied growth rate and implied doubling time. Plotted actual admits vs predicted (just using simple exp growth model) and got very nice fit. Then used implied doubling time of 3.61 in CHIME model and got spot on match with the exponential fit to admits and thus, to the actual admits. Super happy to see this!

You can see the results in this notebook: [model_calibration_validation.ipynb](https://github.com/misken/c19/blob/master/mychime/calibration_validation/model_calibration_validation.ipynb)


## Capacity driven census and admission adjustments to CHIME model

Had idea for adjusting census and admission sduring **early stages** of virus spread to deal with census at time 0 problem. 

Basic idea is that underlying epidemic has its dynamics that will play out almost independent of resources. But for capacity constrained resources it seems like there are a few phases during the early growth stage and then later stages of the virus. Let's just use hospital beds as the example resource.

### growth phase - haven't hit capacity yet and epidemic in exponential growth phase

In this phase, we have the "zero census" problem with the underlying model. But if we are in growth phase, should be easy to just solve for $t_{0}^{*} \lt t_0$ in the basic exponential growth equation to "reconstruct" the admission history and use that along with LOS to compute census for the period $(t_{0}^{*}, t_0)$ and thus have a better estimate of starting census at $t_0$ as well as decent approximation of the mix of how far along those patients are in there stay to better model them leaving - as opposed to assuming all patients at $t_0$ just started there stay, which causes a weird census spike at start of model projections.

**NOTE (2020-03-29)** Looks like Issue [#255](https://github.com/CodeForPhilly/chime/issues/255) is going to address this and go live on Monday, 2020-03-30. Implemented solution is to:

* have user enter day of first covid admit (in addition to current number in hospital)
* use brute force line search to find doubling time that minimizes squared error loss between actual and  predicted census at current time.

Approach makes sense and has benefit of only one additional user input. Hospitals will be happy. 

A complication is that the virus grew at intrinsic growth rate for a while and then
when social distancing started, grew at implied growth rate. Hmm, I wonder if this
matters? **NOTE (2020-04-05)** - `mitigation-date` and `current-date` added to input
parameters and CHIME model now handles this complication.

Hacked around in Excel so I could see what I was doing and this appears to make some sense for this phase. 

See 'model' sheet in [explore_census_adj.xlsx](https://github.com/misken/c19/blob/master/mychime/modeling/explore_census_adj.xlsx).

### flat phase - at capacity

I'm guessing we are going to hit capacity constraints well before epidemic passes inflection point
in the standard logistic model of its exponential spread and then eventual slowing growth.

At this stage, no matter how many admits predicting by underlying SIR model, we have our max admission rate, $A^{*}$ and max census $C^{*}$. We will stay in this state until the underlying SIR model has admission rate $A \lt A^{*}$. So, resource use is flat, though there will be much adaptive behavior
by hospitals as they cope with insufficient resources which will likely affect recovery rates,
death rates, and resource use rates.

### decay phase

When $A \lt A^{*}$, the underlying growth rate in the epidemic must be slowing and now, we can use $A$ to compute census in normal way.

### Plan

I'm going to try to put a procedure together that uses standard outputs from the current chime model to implement these ideas. It would likely require user to input capacity for each resource being modelled (will just start with beds).


## Jupyter notebook version of early CHIME model

**NOTE: This was based on a very early version of the CHIME model. Nevertheless,
the comments might still be useful to someone trying to understand the basic
logic of the model. It should NOT be used for actual work.**

I've added tons of code comments and other descriptive text throughout the notebook to help others understand exactly how this works and how we might adapt it for our use.

https://github.com/misken/c19/blob/master/mychime/archive/chime_earlyversion_annotated.ipynb

