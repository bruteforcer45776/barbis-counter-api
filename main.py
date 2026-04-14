from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, os, threading

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

COUNTER_FILE = "/tmp/counter.json"
lock = threading.Lock()

def get_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE) as f:
            return json.load(f).get("counter", 0)
    return 0

def set_counter(val):
    with open(COUNTER_FILE, "w") as f:
        json.dump({"counter": val}, f)

@app.get("/increment")
def increment():
    with lock:
        val = get_counter() + 1
        set_counter(val)
        code = f"BB-{val:04d}"
        return {"counter": val, "code": code}

@app.get("/health")
def health():
    return {"status": "ok", "counter": get_counter()}
