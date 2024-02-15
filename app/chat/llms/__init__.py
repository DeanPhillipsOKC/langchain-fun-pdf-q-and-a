from functools import partial
from .chatopenai import build_llm

llm_map = {
    # The idea here is to do something like this...
    # llm_builder = llm_map["gpt-4"]
    # llm_builder() # produce an llm based on gpt-4
    # partial creates a new function that calls build_llm and
    # passes in a kwarg of gpt-4
    "gpt-4": partial(build_llm, model_name="gpt-4"),
    "gpt-3.5-turbo": partial(build_llm, model_name="gpt-3.5-turbo")
}