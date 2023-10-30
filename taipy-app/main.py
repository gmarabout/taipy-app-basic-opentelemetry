from taipy import Config, Status
import taipy as tp
import time
from pathlib import Path
from taipy.gui import get_state_id, invoke_callback

from metrics import init_metrics, tracer


# Telemetry
rec_svc_metrics = init_metrics()


@tracer.start_as_current_span("function_double")
def double(nb):
    time.sleep(1)
    return int(nb) * 2


Config.load(Path(__file__).parent / "config.toml")
scenario = Config.scenarios["my_scenario"]


value = 21
result = double(value)

content = """
* You can double this number: <|{value}|input|propagate=True|>
* by clicking on this button: <|Double it!|button|on_action=on_button_click|>
* and here is the result: <|{result}|>
"""
gui = tp.Gui(page=content)
core = tp.Core()


def job_updated(state_id, scenario, job):
    """Callback called when a job has been updated."""
    if job.status == Status.COMPLETED:

        def _update_result(state, output):
            state.result = output.read()

        # invoke_callback allows to run a function with a GUI _state_.
        invoke_callback(gui, state_id, _update_result, args=[scenario.output])

        # Telemetry
        rec_svc_metrics["scenario_execution_counter"].add(
            1, {"execution_type": "manual", "scenario_name": scenario.config_id}
        )


def on_button_click(state):
    state_id = get_state_id(state)
    my_scenario = tp.create_scenario(scenario)
    my_scenario.input.write(state.value)
    tp.subscribe_scenario(scenario=my_scenario, callback=job_updated, params=[state_id])
    tp.submit(my_scenario)


if __name__ == "__main__":
    tp.run(
        gui,
        core,
        host="0.0.0.0",
        title="Basic Taipy App",
    )
