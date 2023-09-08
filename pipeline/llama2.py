import os
import json
from typing import Any, Dict, List, Tuple
from helpers.json_utils import load_jsonl_into, write_jsonl

from pipeline.base import SynthStage
from templates.llama2_chat_templates import (
    CHAT_TEMPLATE as TEMPLATE,
    EXCHANGE_TEMPLATE as EXCHANGE,
    LATEST_USER_TEMPLATE as LATEST,
    SYSTEM_MESSAGE_TEMPLATE,
)


class Llama2SampleBuilder(SynthStage):
    def __init__(
        self,
        input_path_template: str = "data_samples/{ID}_sample",
        output_path_template: str = "llama2/{ID}_train",
    ):
        super().__init__(input_path_template, output_path_template)
        self.required_inputs = ["sample"]

    def clean_inputs(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Clean the input data."""
        cleaned_data = [
            entry
            for entry in data
            for required_input in self.required_inputs
            if required_input in entry
        ]
        cleaned_data = [entry for entry in data if entry.get("sample") is not None]
        return cleaned_data

    def call_llm(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Call the model."""
        results = []
        for entry in data:
            input = entry.get("sample")
            try:
                if type(input) == str:
                    input = json.loads(input)
                conversation = input.get("conversation")
                function_call = input.get("function_call")
                function_description = entry.get("description")
            except:
                continue
            prompts = self.get_prompt(conversation, function_call, function_description)
            for prompt in prompts:
                prompt["id"] = entry.get("function_id")
                results.append(prompt)

        return results

    def clean_outputs(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Clean the output data."""
        return data

    def save_outputs(self, data: List[Dict], run_id: str) -> None:
        """Save the outputs."""
        results = []
        out_path = self.output_path_template.format(ID=run_id) + ".jsonl"
        if os.path.exists(out_path):
            load_jsonl_into(out_path, results)
        for entry in data:
            results.append(entry)
        write_jsonl(out_path, results, indent=0)
        return

    def get_prompt(
        self, conversation: List, function_call: str, function_description: Dict | Any
    ) -> List[Dict]:
        """Get prompt and metadata."""
        prompts = []
        exchange = ""

        function_descriptions = str([function_description])

        system_message = SYSTEM_MESSAGE_TEMPLATE.format(
            FUNCTION_DESCRIPTIONS=function_descriptions,
        )
        for i, chat in enumerate(conversation):
            if chat.get("role") == "user":
                exchange += f"{chat.get('text')} [/INTS]"
            if chat.get("role") == "assistant":
                # do the spaces here matter??
                exchange += f" {chat.get('text')}</s><s>[INST] "
            if i % 2 == 0:
                try:
                    output = conversation[i + 1].get("text")
                    if i == (len(conversation) - 2):
                        output += f" <s>[FUNC] {function_call}[/FUNC]</s>"
                    prompt = TEMPLATE.format(
                        SYSTEM_MESSAGE=system_message, CONVERSATION=exchange
                    )
                    prompts.append(
                        {
                            "input": prompt,
                            "output": output,
                        }
                    )
                except:
                    return prompts

        return prompts
