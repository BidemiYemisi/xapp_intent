import json
from threading import Thread
from flask import Flask, request, jsonify
from ricxappframe.xapp_frame import Xapp

RMR_MT_INTENT = 30001

app = Flask(__name__)
the_xapp = None

def send_intent_via_rmr(payload: dict):
    data = json.dumps(payload).encode("utf-8")
    sbuf = the_xapp.rmr_alloc_msg(len(data))
    sbuf.contents.mtype = RMR_MT_INTENT
    sbuf.contents.sub_id = 0
    sbuf.contents.payload = data
    sbuf.contents.len = len(data)
    ok = the_xapp.rmr_send_msg(sbuf)
    return ok

@app.get("/health")
def health():
    return jsonify(ok=True)

@app.post("/intent")
def intent():
    try:
        payload = request.get_json(force=True)
    except Exception as e:
        return jsonify(ok=False, error=f"bad json: {e}"), 400
    # wrap & forward into RIC fabric
    sent = send_intent_via_rmr({"kind":"dt_intent","payload":payload})
    return jsonify(ok=True, rmr_sent=bool(sent))

def run_rest():
    app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)

def default_handler(self, sbuf):
    # Not used here; this xApp only originates mtype 30001
    pass

def run():
    global the_xapp
    the_xapp = Xapp(default_handler=default_handler, use_fake_sdl=True)
    Thread(target=run_rest, daemon=True).start()
    the_xapp.run()

if __name__ == "__main__":
    run()
