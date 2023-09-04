from json import JSONDecodeError
import json
from typing import Any, Dict, List, Tuple
from pipeline.base import SynthStage
from templates.task_templates import MESSAGE_TEMPLATE_1 as TEMPLATE


class TaskBuilder(SynthStage):
    def __init__(
        self,
        input_path_template: str = "{ID}_",
        output_path_template: str = "{ID}_tasks",
    ):
        super().__init__(input_path_template, output_path_template)
        self.required_inputs = ["function_id"]

    def read_inputs(self, run_id: str) -> List[Dict]:
        return [{"function_base": run_id}]

    def clean_inputs(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Clean the input data."""
        return data

    def call_llm(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Call the model."""
        results = []
        for entry in data:
            input = entry.get("function_base")
            prompt, meta = self.get_prompt(input)
            completion = self.llm_provider.get_completion(prompt)
            try:
                tasks = json.loads(completion)
            except:
                raise Exception(
                    f"LLM did not provide a valid json for category {input}"
                )
            for task in tasks.get("tasks"):
                results.append(task)
        return results

    def clean_outputs(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Clean the output data."""
        return data

    def get_prompt(self, input: Any) -> Tuple[str, Dict[str, str]]:
        """Get prompt and metadata."""
        prompt = TEMPLATE.format(
            INPUT=input,
        )
        meta = {
            "TEMPLATE": TEMPLATE,
            "TASK_CATEGORY": str(input),
        }

        return prompt, meta
