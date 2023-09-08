import logging
import time
import openai

logger = logging.getLogger(__name__)


class OpenAICompletionProvider:
    """A class to provide zero-shot completions from the OpenAI API."""

    def __init__(
        self,
        model: str = "gpt-3-0613",
        temperature: float = 1,
        stream: bool = False,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.stream = stream

    def get_completion(self, prompt: str, slept: int = 3) -> str:
        """Get a completion from the OpenAI API based on the provided prompt."""
        logger.info(f"Getting completion from OpenAI API for model={self.model}")
        logger.info(f"User prompt is {prompt}")
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                stream=self.stream,
            )
        except:

            logger.info(f"Openai API failed, retrying in {slept} seconds!")
            time.sleep(slept * 2)
            return self.get_completion(prompt, slept * 2)
        logger.info(f"Openai response is  {response.choices[0].message['content']}")
        return response.choices[0].message["content"]
