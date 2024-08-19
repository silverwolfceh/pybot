from flask import Flask, render_template, request, redirect, url_for, send_file
from modules.smspool import get_the_min_price, get_service_list
from jsondb import jsondb, CACHE
import time
import threading
import json

app = Flask("YourTiniWorkers")

CID = "SMSPOOL"
CIDIDX = "TEMP"
DID = ""

status_keeper = {}


def update_status(requestid, percent, result=None):
    print(requestid, percent)
    with jsondb(requestid) as obj:
        ret, data = obj.get_cache(requestid)
        if ret == CACHE.CACHEHIT:
            data["status"] = percent
            data["result"] = result
            obj.store_cache(requestid, data)


def thread_wrapper(srvid, update_status, reqid, apikey):
    return get_the_min_price(srvid, update_status, reqid, apikey)


@app.route("/smspool/check")
def check_status():
    reqid = request.args.get('reqid', "")
    with jsondb(reqid) as obj:
        ret, data = obj.get_cache(reqid)
        if ret == CACHE.CACHEMISS:
            return "Invalid reqid"
        else:
            status = f"{data['status']:.2f}"
            result = data['result']
            return {"status": status, "result": result}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/smspool")
def smspool():
    slist = get_service_list()
    return render_template("smspool.html", options=slist)


@app.route("/smspool/run", methods=["POST"])
def runit():
    # Get service type
    srvid = request.form.get('selectedOption')
    ignorecache = int(request.form.get('ignorecache'))
    print(ignorecache)
    
    if srvid == "":
        return "Please input srvid"
    apikey = "VFoCdZK4WjDeArKacB43cE1K0Intx2Vu"
    reqid = "SRV_" + str(int(time.time()))
    # Check if there is same service on-going
    with jsondb(CIDIDX) as obj:
        idxkey = f"{srvid}_{apikey}"
        ret, data = obj.get_cache(idxkey)

        if ret == CACHE.CACHEMISS:
            # New service
            obj.store_cache(idxkey, {"reqid": reqid})
        elif ignorecache == 1:
            obj.delete_cache(idxkey)
            obj.store_cache(idxkey, {"reqid": reqid})
        else:
            reqid = data["reqid"]

    with jsondb(reqid) as obj:
        ret, data = obj.get_cache(reqid)
        if ret == CACHE.CACHEHIT and ignorecache == 0:
            #data["status"] = 100
            pass
        else:
            data = {}
            data["status"] = 0
            data["result"] = ""
            data["reqid"] = reqid
            obj.store_cache(reqid, data)
            t = threading.Thread(target=thread_wrapper,
                                 args=(srvid, update_status, reqid, apikey))
            t.start()
    return {"taskid": reqid}


if __name__ == '__main__':
    import os
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    app.run("0.0.0.0", 8000, debug=True)
