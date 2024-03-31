from maitai.config import global_config

@property
def api_key():
    return global_config.api_key

@api_key.setter
def api_key(value):
    global_config.api_key = value

@property
def application_id():
    return global_config.application_id

@application_id.setter
def application_id(value):
    global_config.application_id = value

from maitai._eval_request import EvalRequest as EvalRequest
from maitai._loadable import Loadable as Loadable
from maitai._maitai_object import MaiTaiObject as MaiTaiObject
from maitai._evaluator import Evaluator as Evaluator