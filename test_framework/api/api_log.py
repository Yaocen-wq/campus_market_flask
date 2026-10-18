import requests
from utils.logger import get_logger
import json

log = get_logger("api")
RECORDS = []

def clear_records():
    RECORDS.clear()

def req(method, url, session=None, **kwargs):
    who = session if session is not None else requests
    shown = kwargs.get("data", kwargs.get("params"))
    log.info(f"REQ {method} {url} data={shown}")
    RECORDS.append(f"REQ  {method} {url}\ndata={shown}")
    r = who.request(method, url, **kwargs)
    text = r.text
    try:
        text = json.dumps(r.json(), ensure_ascii=False, indent=2)
    except ValueError:
        pass
    log.info(f"RES {r.status_code} {text} 耗时：{r.elapsed.total_seconds():.3f}s")
    RECORDS.append(f"RES  {r.status_code}\n{text}\n耗时：{r.elapsed.total_seconds():.3f}s")
    return r