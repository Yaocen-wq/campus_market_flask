import json
import os

import pandas as pd
import streamlit as st

HERE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(HERE, "logs", "fail_summary.json")

st.title("测试结果看板")

if not os.path.exists(JSON_PATH):
    st.error(f"找不到 {JSON_PATH}，先跑一次 pytest")
    st.stop()

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

st.metric("失败总数", data["total"])

modules = list(data["modules"].keys())
pick = st.multiselect("只看这些模块", modules, default=modules) if modules else []

rows = []
for g in data["groups"]:
    for c in g["cases"]:
        if c["module"] in pick:
            rows.append({
                "异常类型": g["exc"],
                "模块": c["module"],
                "用例": c["func"],
                "条数": c["count"],
            })

if rows:
    st.dataframe(pd.DataFrame(rows))
else:
    st.info("没有失败的用例")