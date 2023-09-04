import json
from typing import Any, Dict, List, Tuple

from pipeline.base import SynthStage
from templates.sample_templates import (
    MESSAGE_TEMPLATE_2 as TEMPLATE,
    CONVERSATION_EXAMPLE_2 as PROMPT_EX,
    FUNCTION_EXAMPLE_2 as FUNCTION_EX,
    CALL_EXAMPLE_2 as CALL_EX,
)


class DataSampleBuilder(SynthStage):
    def __init__(
        self,
        input_path_template: str = "descriptions/{ID}_description",
        output_path_template: str = "data_samples/{ID}_sample",
    ):
        super().__init__(input_path_template, output_path_template)
        self.required_inputs = ["snippet"]

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
            input_description = entry.get("description")
            prompt, meta = self.get_prompt(input_description)
            completion = self.llm_provider.get_completion(prompt)

            entry["sample_metadata"] = meta

            try:
                entry["description"] = json.loads(completion)
            except Exception:
                entry["description"] = None

        return data

    def clean_outputs(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Clean the output data."""
        return [entry for entry in data if "example_function" not in entry["snippet"]]

    def get_prompt(self, input: Any) -> Tuple[str, Dict[str, str]]:
        """Get prompt and metadata."""
        prompt = TEMPLATE.format(
            FUNCTION_DESCRIPTION=str(input),
            PROMPT_EXAMPLE=PROMPT_EX,
            # FUNCTION_EXAMPLE=FUNCTION_EX,
            CALL_EXAMPLE=CALL_EX,
        )

        meta = {
            "TEMPLATE": TEMPLATE,
            "FUNCTION_DESCRIPTION": str(input),
            "PROMPT_EXAMPLE": PROMPT_EX,
            "FUNCTION_EXAMPLE": FUNCTION_EX,
            "CALL_EXAMPLE": CALL_EX,
        }

        return prompt, meta
