from langchain_google_genai import ChatGoogleGenerativeAI


class UnsupportedModelError(Exception):
    pass


def create_llm_client(api_key, model, verbose=True, temperature=0.1):
    if model == "gemini-pro":
        return ChatGoogleGenerativeAI(
            model=model,
            verbose=verbose,
            temperature=temperature,
            google_api_key=api_key,
        )

    raise UnsupportedModelError(f"Unsupported model: {model}")


class LLMClient:
    def __init__(self, api_key, model, verbose=True, temperature=0.1):
        self.llm = self.__create_llm_client(api_key, model, verbose, temperature)

    def __create_llm_client(self, api_key, model, verbose, temperature):
        if model == "gemini-pro":
            return ChatGoogleGenerativeAI(
                model=model,
                verbose=verbose,
                temperature=temperature,
                google_api_key=api_key,
            )

        raise UnsupportedModelError(f"Unsupported model: {model}")

    def get_response(self, input_text):
        return self.llm.generate_response(input_text)
