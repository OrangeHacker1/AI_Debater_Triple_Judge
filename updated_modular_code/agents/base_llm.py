
from openai import OpenAI
import time

from openai import APIError, RateLimitError, APITimeoutError, AuthenticationError


class LLMInterface:

    def __init__(self, base_url, api_key, model, temperature, max_tokens):
        """
        Creates a reusable interface for querying the LLM.

        Parameters
        ----------
        base_url : str
            URL of hosted model endpoint
        api_key : str
            Authentication key
        model : str
            Model name
        """

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens


    def query(self, prompt, retries=3):
        """
        Sends prompt to model with retry + error handling.
        """

        for attempt in range(retries):

            try:

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )

                return response.choices[0].message.content

            except AuthenticationError:
                raise Exception("Authentication failed. Check API key.")

            except RateLimitError:
                print("Rate limit exceeded. Waiting...")
                time.sleep(3)

            except APITimeoutError:
                print("API timeout. Retrying...")
                time.sleep(2)

            except APIError as e:
                print("General API error:", e)
                time.sleep(2)

        raise Exception("LLM query failed after retries")
