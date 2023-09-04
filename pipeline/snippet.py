from typing import Any, Dict, List, Tuple
from pipeline.base import SynthStage
from templates.snippet_templates import MESSAGE_TEMPLATE_1 as TEMPLATE


class CodeSnippetBuilder(SynthStage):
    def __init__(
        self,
        input_path_template: str = "tasks/{ID}",
        output_path_template: str = "snippets/{ID}_snippets",
    ):
        super().__init__(input_path_template, output_path_template)
        self.required_inputs = ["task"]

    def clean_inputs(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Clean the input data."""
        cleaned_data = [
            entry
            for entry in data
            for required_input in self.required_inputs
            if required_input in entry
        ]
        return cleaned_data

    def call_llm(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Call the model."""
        for entry in data:
            task = entry.get("task")
            prompt, meta = self.get_prompt(task)
            completion = self.llm_provider.get_completion(prompt)

            entry["snippet_metadata"] = meta
            entry["snippet"] = completion

        return data

    def clean_outputs(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Clean the output data."""
        return [entry for entry in data if "example_function" not in entry["snippet"]]

    def get_prompt(self, input: Any) -> Tuple[str, Dict[str, str]]:
        """Get prompt and metadata."""
        prompt = TEMPLATE.format(FUNCTION_TASK=str(input))
        meta = {
            "TEMPLATE": TEMPLATE,
            "FUNCTION_TASK": str(input),
        }

        return prompt, meta
