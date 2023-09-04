import json
from typing import Any, Dict, List, Tuple

from pipeline.base import SynthStage
from templates.description_templates import (
    MESSAGE_TEMPLATE_1 as TEMPLATE,
    SNIPPET_EXAMPLE_2 as SNIPPET_EX,
    DESCRIPTION_EXAMPLE_2 as DESCRIPTION_EX,
)


class DescriptionBuilder(SynthStage):
    def __init__(
        self,
        input_path_template: str = "snippets/{ID}_snippets",
        output_path_template: str = "descriptions/{ID}_description",
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
            snippet = entry.get("snippet")
            prompt, meta = self.get_prompt(snippet)
            completion = self.llm_provider.get_completion(prompt)

            entry["description_metadata"] = meta

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
            FUNCTION_SNIPPET=str(input),
            # SNIPPET_EXAMPLE=SNIPPET_EX,
            DESCRIPTION_EXAMPLE=DESCRIPTION_EX,
        )

        meta = {
            "TEMPLATE": TEMPLATE,
            "FUNCTION_SNIPPET": str(input),
            # "SNIPPET_EXAMPLE": SNIPPET_EX,
            "DESCRIPTION_EXAMPLE": DESCRIPTION_EX,
        }

        return prompt, meta
