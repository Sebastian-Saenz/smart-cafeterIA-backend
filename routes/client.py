import os
from flask import Blueprint, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from psycopg_pool import PoolTimeout

from config import Config
from extensions import checkpointer
from utils import get_prompt
from tool_services import (
    check_schedule,
    get_order,
    search_stock,
    get_recommendation,
    get_client_data,
)

client_bp = Blueprint("client", __name__)
config = Config()


@client_bp.route("/agent", methods=["GET"])
def client_agent():
    id_agente = request.args.get("idagente")
    msg = request.args.get("msg", "")

    model = ChatOpenAI(model="gpt-4.1-2025-04-14")
    prompt = ChatPromptTemplate.from_messages(
        [("system", get_prompt("virtual_assistent.txt")), ("human", "{messages}")]
    )

    agent = create_react_agent(
        model,
        tools=[
            check_schedule,
            get_order,
            search_stock,
            get_recommendation,
            get_client_data,
        ],
        checkpointer=checkpointer,
        prompt=prompt,
    )

    try:
        print(f"[Client Service]")
        print(f"\t↳ Mensaje: {msg}")
        print("\t↳ Invocando agente...")
        res = agent.invoke(
            {"messages": [HumanMessage(content=msg)]},
            config={"configurable": {"thread_id": id_agente}},
        )
        reply = res["messages"][-1].content
        print(f"[Client Service]")
        print(f"\t↳ Reply final: {reply}")
    except PoolTimeout:
        reply = "Ups, hubo un problema 😕"

    return jsonify({"reply": reply})