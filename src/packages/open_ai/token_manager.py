from re import search
from time import time, sleep
from openai import OpenAI, RateLimitError
from openai.types.responses import Response
from json import load

from packages.open_ai.case_size_error import CaseSizeError


def _extract_limit_requested(error_message, hadm_id: str):
    match = search(r"Limit (\d+)(?:, Used (\d+))?, Requested (\d+)", error_message)
    if not match:
        return None, None, None
    elif not match.group(2):
        raise CaseSizeError(hadm_id)
    else:
        limit = int(match.group(1))
        used = int(match.group(2)) if match.group(2) else limit
        requested = int(match.group(3))
        return limit, used, requested


class TokenManager:
    def __init__(self, model='gpt-4.1-nano', tpm=30_000):
        self.__tokens = tpm
        self.__tpm_limit = tpm
        self.__last_check = time()
        self.__client = OpenAI()
        with open('./assets/schema.json', 'r') as file:
            self.__schema = load(file)
        self.__model = model

    def send_request(self, model_input: str, hadm_id: str) -> Response:
        while True:
            try:
                return self.__client.responses.create(
                    model=self.__model,
                    input=model_input,
                    text=self.__schema,
                    temperature=0.1
                    # reasoning = {"effort": "high"}
                )
            except RateLimitError as e:
                self.__handle_rate_limit(str(e), hadm_id)

    def __handle_rate_limit(self, error_message, hadm_id: str):
        limit, used, requested = _extract_limit_requested(error_message, hadm_id)
        if not limit or not requested:
            print("Could not parse limit/requested from error. Waiting 15 seconds fallback.")
            sleep(15)
        else:
            tokens_remaining = limit - used
            tokens_missing = requested - tokens_remaining
            tokens_per_second = limit / 60
            wait_seconds = (tokens_missing / tokens_per_second)
            wait_seconds = max(wait_seconds, 5)
            print(f"Rate limit: waiting {wait_seconds:.3f} seconds based on server info...")
            sleep(wait_seconds)
        self.__refill_tokens()

    def __refill_tokens(self):
        now = time()
        elapsed = now - self.__last_check
        regenerated = (self.__tpm_limit / 60) * elapsed
        self.tokens = min(self.__tokens + regenerated, self.__tpm_limit)
        self.last_check = now
