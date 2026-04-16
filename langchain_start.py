from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
llm = ChatGroq(api_key="api_key", model="llama-3.3-70b-versatile")
messages = [SystemMessage (content="you are brutal mentor")]
while True:
    user_input = input("you : ")
    if user_input.lower() == "quit":
        break
    messages.append(HumanMessage(content= user_input))
    response = llm.invoke(messages)
    messages.append(response)
    print(response.content)