from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def infer_relationships(data_dict):
    """Uses LLM to describe relationships between datasets."""
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template("""
    Given these dataframes: {tables}, describe how they are related in a financial services context.
    Return in concise sentences.
    """)
    tables = list(data_dict.keys())
    chain = prompt | model
    response = chain.invoke({"tables": tables})
    print("🔗 Inferred Relationships:\n", response.content)
