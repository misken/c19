"""
Prototype post-processor for t_0 census adjustment



"""

from argparse import (
    Action,
    ArgumentParser,
)

from datetime import datetime

from penn_chime.settings import DEFAULTS
from penn_chime.parameters import Parameters
from penn_chime.models import SimSirModel
from penn_chime.utils import RateLos

import numpy as np
import pandas as pd
import json

def t0_census_adjust(params: Parameters = None,
              current_hospitalized: int = None,
              doubling_time: float = None,
              known_infected: int = None,
              relative_contact_rate: float = None,
              susceptible: int = None,
              hospitalized: RateLos = None,
              icu: RateLos = None,
              ventilated: RateLos = None,
              market_share: float = None,
              n_days: int = None,
              recovery_days: float = None,)