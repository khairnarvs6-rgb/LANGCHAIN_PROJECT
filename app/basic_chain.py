from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.llm import get_llm


prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms with one practical example."
)

# Prompt -> Groq model -> plain text output.
chain = prompt | get_llm() | StrOutputParser()


if __name__ == "__main__":
    result = chain.invoke({"topic": "LangChain"})
    print(result)