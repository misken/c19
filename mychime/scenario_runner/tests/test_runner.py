import pytest

from datetime import datetime
from penn_chime.constants import CHANGE_DATE
from penn_chime.parameters import Parameters, Disposition
from penn_chime.models import SimSirModel as Model
import penn_chime.models as models
import penn_chime.cli as cli

from pandas import DataFrame
import numpy as np
import pandas as pd

import sys
import json

import sim_chime_scenario_runner as runner

@pytest.fixture
def admits_dt361_df():
    return pd.read_csv('tests/output/dt361_projected_admits.csv', parse_dates=['date'])

@pytest.fixture
def census_dt361_df():
    return pd.read_csv('tests/output/dt361_projected_census.csv', parse_dates=['date'])

@pytest.fixture
def admits_fd20200220_df():
    return pd.read_csv('tests/output/fd20200220_projected_admits.csv', parse_dates=['date'])

@pytest.fixture
def census_fd20200220_df():
    return pd.read_csv('tests/output/fd20200220_projected_census.csv', parse_dates=['date'])


def test_import():


    p_dt361 = runner.create_params_from_file('tests/cli_inputs_semi_dt3.61.cfg')
    p_fd20200220 = runner.create_params_from_file('tests/cli_inputs_semi_fd2020-02-20.cfg')

    scenario = 'runner_import_dt361'
    model, results_dt361 = runner.sim_chime(scenario, p_dt361)

    scenario = 'runner_import_fd20200220'
    model, results_fd20200220 = runner.sim_chime(scenario, p_fd20200220)

    print(results_dt361['intermediate_variables_dict'])