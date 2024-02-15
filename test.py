from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

# streaming determines how open AI responds to langchain
chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

# Using a mixin rather than subclassing LLMChain directly so that we don't have to keep
# redefining the stream method for anything else we want to add streaming support to
class StreamingChain(StreamableChain, LLMChain):
    pass

chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input= {"content": "tell me a joke"}):
    print(output)