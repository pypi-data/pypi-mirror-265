from dataclasses import dataclass
import pandas as pd
from copy import deepcopy
from typing import Union, Optional, Callable, Any
import inspect
from inspect import Signature, signature
import logging
import logging.config
import functools


@dataclass
class Job:
    function: Callable
    name: Optional[str] = None
    inputs: Optional[list[Any]] = None
    dependencies: Optional[list[Union["Job", "Pipeline"]]] = None
    output = None
    executed = False

    def __post_init__(self):
        if self.name is None:
            self.name = self.function.__name__

    def run(self):
        if self.dependencies is not None:
            for dep in self.dependencies:
                if not dep.executed:
                    dep.run()
            dependencies = [dep.output for dep in self.dependencies]
        if self.inputs is not None and self.dependencies is not None:
            inputs = dependencies + self.inputs.copy()
        elif self.inputs is None and self.dependencies is not None:
            inputs = dependencies
        elif self.inputs is not None and self.dependencies is None:
            inputs = self.inputs.copy()
        else:
            raise Exception("Please provide either inputs or dependencies for this job")
        output = self.function(*inputs)
        self.output = output
        self.executed = True

    def __call__(self):
        self.run()

def job(function:Optional[Callable]=None, *, name=None, inputs=None, dependencies=None):
    if function is None:
        return functools.partial(job, name=name, inputs=inputs, dependencies=dependencies)
    
    return Job(function, name=name, inputs=inputs, dependencies=dependencies)
    



@dataclass
class Pipeline:
    name: str
    steps: list[Union[Job, "Pipeline"]]
    output = None
    executed = False
    verbose = True
    nested = False

    def __post_init__(self):
        dependency_map = {
            step.name: [dep.name for dep in step.dependencies]
            for step in self.steps
            if isinstance(step, Job) and step.dependencies is not None
        }
        dm = {step.name: list() for step in self.steps}
        for step_name, dependant_step_names in dm.items():
            for (
                dependant_step_name,
                dependant_step_dependancy_names,
            ) in dependency_map.items():
                if step_name in dependant_step_dependancy_names:
                    dependant_step_names.append(dependant_step_name)
        dm = {
            step_name: dep_step_names
            for step_name, dep_step_names in dm.items()
            if len(dep_step_names) > 0
        }
        self.dmap = dm

    def run(self):
        if self.verbose:
            print(
                f"""
===================================================
Starting pipeline run: {self.name}
==================================================="""
            )
        for step in self.steps:
            if self.verbose:
                print(f"Running {step.name}")
            step.run()
            for step_name in list(
                self.dmap.keys()
            ):  # can't edit dictionary while iterating over it, see line 73
                step_to_alter = [step for step in self.steps if step.name == step_name][
                    0
                ]
                self.dmap[step_name] = [
                    dep_step_name
                    for dep_step_name in self.dmap[step_name]
                    if dep_step_name != step.name
                ]
                if (
                    len(self.dmap[step_name]) == 0
                ):  # no more steps dependant on this step so output can be removed
                    step_to_alter.output = None
                    del self.dmap[step_name]

        final_step = self.steps[-1]
        try:
            output = final_step.output.copy()
        except AttributeError:
            output = final_step.output
        if self.nested:
            for step in self.steps:
                step.output = None
                step.executed = False
            return output
        self.output = output
        self.executed = True
        if self.verbose:
            print(
                f"""
===================================================
Finished pipeline run: {self.name}
==================================================="""
            )
