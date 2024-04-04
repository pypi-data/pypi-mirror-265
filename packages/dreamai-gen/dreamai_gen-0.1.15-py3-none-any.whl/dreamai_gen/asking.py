from collections import OrderedDict
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

from pydantic import BaseModel, Field
from termcolor import colored

from . import prompting
from .llms import ask_oai
from .message import MESSAGES_TYPE, last_user_message, user_message
from .prompting.prompt_fns import (
    create_template_functions,
    process_prompt,
)
from .tools import use_tool
from .utils import (
    flatten_list,
    get_function_name,
    get_param_names,
    get_required_param_names,
)

TEMPLATE_FUNCTIONS = create_template_functions([prompting])
ASKER = ask_oai


def check_exit(messages: MESSAGES_TYPE = None) -> bool:
    if not messages:
        return False
    last_content = messages[-1]["content"]
    if isinstance(last_content, str) and last_content.lower() == "exit":
        messages.pop(-1)
        return True
    last_user_msg = last_user_message(messages)
    if last_user_msg:
        last_user_content = last_user_msg["message"]["content"]
        if isinstance(last_user_content, str) and last_user_content.lower() == "exit":
            messages.pop(last_user_msg["index"])
            return True
    return False


def run_task(
    task: Any, assets: dict | None = None, asset_key: str | None = None
) -> dict:
    if asset_key and asset_key == "skip":
        return assets
    assets = assets or OrderedDict()
    assets.setdefault("messages", [])
    if isinstance(task, dict):
        return run_dict_task(task, assets)
    return run_list_task(task, assets, asset_key)


def run_dict_task(task: dict, assets: dict) -> dict:
    for asset_key, subtask in task.items():
        assets = run_task(
            task=subtask,
            assets=assets,
            asset_key=asset_key,
        )
    return assets


def run_list_task(task, assets: dict, asset_key: str | None = None) -> dict:
    task = [task] if not isinstance(task, list) else task
    task = flatten_list(task)
    for subtask in task:
        if check_exit(assets["messages"]):
            break
        if isinstance(subtask, dict):
            current_asset_key, subtask = list(subtask.items())[0]
        else:
            current_asset_key = asset_key
        assets = process_subtask(subtask, assets, current_asset_key)
    return assets


def process_subtask(subtask, assets: dict, asset_key: str | None = None) -> dict:
    if callable(subtask):
        assets = use_tool(
            tool=subtask,
            assets=assets,
            asset_key=asset_key,
        )
    elif isinstance(subtask, (str, Path)):
        task_content = process_prompt(subtask, template_functions=TEMPLATE_FUNCTIONS)
        assets["messages"].append(user_message(content=task_content))
        if asset_key:
            assets[asset_key] = task_content
    else:
        raise TypeError(f"Invalid task type: {type(subtask)}")
    return assets


def ask(*tasks, assets: dict | None = None) -> dict:
    assets = assets or OrderedDict()
    assets.setdefault("messages", [])
    messages = assets["messages"]
    tasks = list(tasks)
    # print(f"\n\nASK TASKS: {tasks}\n\n")
    # print(f"\n\nASK MESSAGES: {messages}\n\n")
    if len(messages) > 0 and messages[-1]["role"] == "user":
        if tasks[0] != messages[-1]["content"]:
            tasks.insert(0, messages.pop(-1)["content"])
    for task in tasks:
        try:
            # if isinstance(task, Task):
            #     if task.condition(assets):
            #         assets = run_task(task=task.subtasks, assets=assets)
            # else:
            assets = run_task(task=task, assets=assets)
        except Exception as e:
            print(colored(f"\n\nASK ERROR: {e}\n\n", "red"))
        if check_exit(assets["messages"]):
            break
    return assets


def default_assets(assets: dict = None) -> dict:
    assets = assets or OrderedDict()
    assets.setdefault("messages", [])
    return assets


class Task(BaseModel):
    name: str = ""
    condition: Callable = Field(default_factory=lambda: lambda x: True)
    task: Any

    def do_task(self, assets: dict | None = None, **kwargs) -> dict:
        assets = default_assets(assets=assets)
        result_dict = {}
        if isinstance(self.task, (str, Path)):
            task_result = process_prompt(
                prompt=self.task, template_functions=TEMPLATE_FUNCTIONS
            )
            assets["messages"].append(user_message(content=task_result))
            result_name = self.name or "_".join(str(self.task).split()[:2]) + "_result"
            result_dict[result_name] = task_result
        elif callable(self.task):
            params = {"assets": assets, **assets, **kwargs}
            task_name = get_function_name(self.task)
            task_params = get_param_names(self.task)
            task_required_params = get_required_param_names(self.task)
            result_name = self.name or f"{task_name}_result"
            if "kwargs" in task_params:
                call_params = params
            else:
                call_params = {k: v for k, v in params.items() if k in task_params}
            if call_params or not task_required_params:
                curr_messages = deepcopy(assets["messages"])
                try:
                    task_result = self.task(**call_params)
                    result_dict[result_name] = task_result
                    if (
                        assets["messages"] != curr_messages
                    ):  # the tool modified the messages
                        if (
                            task_result == assets["messages"]
                        ):  # the tool returned the modified messages
                            result_dict = {result_name: task_result[-1]["content"]}
                        elif (
                            task_result != assets["messages"][-1]["content"]
                        ):  # the tool modified the messages and also returned something else
                            result_dict = {
                                result_name: task_result,
                                f"{result_name}_message": assets["messages"][-1][
                                    "content"
                                ],
                            }
                    elif task_result == assets["messages"]:  # nothing was modified
                        result_dict = {}
                except Exception as e:
                    error_msg = f"ERROR WITH TASK: {task_name}\nERROR: {e}"
                    print(colored(f"\n\n{error_msg}\n\n", "red"))
        else:
            raise TypeError(f"Invalid task type: {type(self.task)}")
        assets.update(result_dict)
        return assets

    def __call__(self, assets: dict | None = None, **kwargs) -> dict:
        assets = default_assets(assets=assets)
        try:
            condition = self.condition(assets=assets, task=self.task)
        except Exception:
            condition = self.condition(assets=assets)
        if condition:
            assets = self.do_task(assets=assets, **kwargs)
        return assets


class Tasks(BaseModel):
    tasks: list[Task] = Field(default_factory=list)
    condition: Callable = Field(default_factory=lambda: lambda x: True)

    def do_tasks(self, assets: dict | None = None, **kwargs) -> dict:
        assets = default_assets(assets=assets)
        if self.condition(assets):
            for task in self.tasks:
                if not isinstance(task, Task):
                    task = Task(task=task)
                assets = task(assets=assets, **kwargs)
        return assets


class Asker(BaseModel):
    assets: dict = Field(default_factory=default_assets)
    tasks: Tasks = Field(default_factory=Tasks)

    def __call__(self, assets: dict | None = None, **kwargs) -> dict:
        assets = default_assets(assets=assets)
        assets = self.tasks.do_tasks(assets=assets, **kwargs)
        return assets
