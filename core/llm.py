from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from config.settings import settings

def get_llm(model_name=None):
    if settings.LLM_PROVIDER == "anthropic":
        return ChatAnthropic(model=model_name or "claude-3-5-sonnet-20241022", temperature=0)
    else:
        # Default to OpenAI
        return ChatOpenAI(model=model_name or "gpt-4o", temperature=0)
