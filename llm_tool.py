from openai import OpenAI
import streamlit as st
import os
from typing import Any

from langchain.tools import BaseTool
from langchain.agents import initialize_agent, load_tools
from langchain.callbacks import OpenAICallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import pymysql


class MySqlTool:
    connection = None

    @staticmethod
    def s_connection_db():
        if MySqlTool.connection is None:

            MySqlTool.connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='zh19991111',
                database='employee'
            )

        return MySqlTool.connection


def queryEmployee(query: str):

    connection = MySqlTool.s_connection_db()

    cursor = connection.cursor()

    id = 0
    try:
        id = int(query) or 0
    except ValueError:
        id = 0

    sql = f"SELECT * FROM worker where WORKER_ID = {id} or FIRST_NAME = '{query}' or SALARY = '{query}'"
    print("sql: ", sql)
    cursor.execute(sql)

    results = cursor.fetchall()

    info = ""

    for row in results:
        info += f"id: {row[0]}, 姓名: {row[1]}, 工资: {row[3]}, 入职时间: {row[4]}, 部门: {row[5]} \n"

    cursor.close()
    print(type(info))

    return info


class EmployeeQueryTool(BaseTool):
    name = "employeeQuery"
    description = "If user want to do query about database, use it"

    def _run(self, query: str) -> str:
        print("\nEmployeeQueryTool query: " + query)
        info = queryEmployee(query)
        if (len(info) > 0):
            return info
        else:
            return "未找到员工信息!"


llm = ChatOpenAI(openai_api_key='sk-ZKLYy95Hb6QwvoIaE8A1A6Ce6d3d4172Bf50Fa929a650a87', openai_api_base='https://elderman.top/v1', temperature=0, model_name='gpt-3.5-turbo-1106')
tools = [EmployeeQueryTool()]
agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
    )

)


model_list = ["llama2", "orca-mini", "gemma:2b", "openai_model"]

# Set OpenAI API key from Streamlit secrets
# client = OpenAI(
#     base_url = 'http://localhost:11434/v1',
#     api_key='ollama', # required, but unused
# )


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-1106"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Settings")

    option = st.selectbox(
        'Select a model',
        [model for model in model_list])
    st.write('You selected:', option)
    st.session_state["model_name"] = option

st.title(f"Chat with {st.session_state['model_name']} with Mysql")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            # model= st.session_state['model_name']
            model='gpt-3.5-turbo-1106',
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


while True:
    str = input("请输入您的问题：")
    result = agent.run(str)
    print("执行结果: ", result)
