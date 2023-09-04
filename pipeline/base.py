from abc import ABC, abstractmethod
import os
from typing import List, Dict

from helpers.json_utils import load_jsonl_into, write_jsonl
from helpers.openai import OpenAICompletionProvider


class SynthStage(ABC):
    llm_provider: OpenAICompletionProvider

    def __init__(
        self,
        input_path_template: str,
        output_path_template: str,
    ):
        base_dir = "outputs/"
        self.input_path_template = base_dir + input_path_template
        self.output_path_template = base_dir + output_path_template

    def read_inputs(self, run_id: str) -> List[Dict]:
        """Read inputs and return a list of dictionaries."""
        data = []
        input_path = self.input_path_template.format(ID=run_id) + ".jsonl"
        if os.path.exists(input_path):
            load_jsonl_into(input_path, data)
        else:
            raise FileNotFoundError(f"File with name {input_path} does not exist!")
        return data

    @abstractmethod
    def clean_inputs(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Clean the input data."""
        pass

    @abstractmethod
    def call_llm(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Call the model."""
        pass

    @abstractmethod
    def clean_outputs(self, data: List[Dict], run_id: str) -> List[Dict]:
        """Clean the output data."""
        pass

    def save_outputs(self, data: List[Dict], run_id: str) -> None:
        """Save the outputs."""
        results = []
        out_path = self.output_path_template.format(ID=run_id) + ".jsonl"
        if os.path.exists(out_path):
            load_jsonl_into(out_path, results)
        for entry in data:
            results.append(entry)
        write_jsonl(out_path, results)
        return

    def run(self, run_id: str) -> None:
        """Run the entire stage pipeline."""
        data = self.read_inputs(run_id)
        data = self.clean_inputs(data, run_id)
        data = self.call_llm(data, run_id)
        data = self.clean_outputs(data, run_id)
        self.save_outputs(data, run_id)


class SynthPipeline:
    def __init__(
        self, model: str = "gpt-3.5-turbo-0613", temperature: float = 1.0
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.stages = []

    def add_stage(self, stage: SynthStage) -> "SynthPipeline":
        """Add a stage to the pipeline."""
        stage.llm_provider = OpenAICompletionProvider(self.model, self.temperature)
        self.stages.append(stage)
        return self

    def run(self, id) -> None:
        """Run all stages in the pipeline."""
        for stage in self.stages:
            stage.run(id)
