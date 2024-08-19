import sys
sys.path.append("..")

from utils import create_req_session
from resultmemorize import ResultMemorizer

@ResultMemorizer.memorize
def get_country_list(apikey = "VFoCdZK4WjDeArKacB43cE1K0Intx2Vu"):
    url = "https://api.smspool.net/country/retrieve_all"
    try:
        res = create_req_session().post(url, data=f"key={apikey}")
        return res.json()
    except Exception as e:
        return None

@ResultMemorizer.memorize
def get_service_list(apikey = "VFoCdZK4WjDeArKacB43cE1K0Intx2Vu"):
    url = "https://api.smspool.net/service/retrieve_all"
    try:
        res = create_req_session().post(url, data=f"key={apikey}")
        return res.json()
    except Exception as e:
        return None

@ResultMemorizer.memorize
def get_the_min_price(srvid, statuscb = None, reqid = "", apikey = "VFoCdZK4WjDeArKacB43cE1K0Intx2Vu"):
    service_id = srvid  #Chat GPT
    url = "https://api.smspool.net/request/price?country=%s&service=%s&key=%s&pool=&name=%s"
    min_price = 99
    min_country = ""
    success_rate = 100
    clist = get_country_list()
    steprate = 100 / len(clist)
    curprog = 0
    for c in clist:
        url1 = url % (str(c["ID"]), service_id, apikey, c["name"])
        res = create_req_session().get(url1)
        if res.status_code == 200:
            # Request successful
            data = res.json()  # Extract JSON response data
            print(data, c["name"])
            try:
                if float(data["price"]) < min_price:
                    min_price = float(data["price"])
                    min_country = c["name"]
                    success_rate = data["success_rate"]
                elif float(data["price"]) == min_price and data["success_rate"] >= success_rate:
                    min_price = float(data["price"])
                    min_country = c["name"]
                    success_rate = data["success_rate"]
                else:
                    pass
            except:
                pass
            curprog = curprog + steprate
            if curprog > 100:
                curprog = 100
            statuscb(reqid, curprog)
        else:
            # Request failed
            print(f"Request failed with status code: {res.status_code}")

    output = "%s_%s_%s_%s" % (srvid, min_country, str(min_price), str(success_rate))
    statuscb(reqid, 100, output)
    print(output)
    return output


get_country_list()
get_service_list()