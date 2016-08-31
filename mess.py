from flask import Flask
from flask import render_template, jsonify
import requests
import urllib

try:
    import simplejson
except ImportError:
    import json as simplejson

SPARKURL = 'https://api.ciscospark.com/v1/'
SPARKID = 'PubHub@sparkbot.io'
SPARKKEY = 'Bearer NGU5ZjM3MWMtYWYyOS00ODZjLWEwY2YtODY0ZGM3N2E1YjdiYWJlNDkwMmQtMGI3'
SPARKROOMID = 'Y2lzY29zcGFyazovL3VzL1JPT00vMDRkYWVlNzAtNjYzNy0xMWU2LTg5MjctNzNmNDA1ZmYxOTkw'


def make_request(url_ext, method, post_data=""):
    #url = SPARKURL + url_ext
    url = url_ext
    #print url
    headers = {
        "Authorization": SPARKKEY,
        "Content-Type": "application/json; charset=utf-8"
    }
    # headers = json.dumps(headers_obj)
    if method == "POST":
        resp = requests.post(url, data=post_data, headers=headers)
        if int(resp.status_code / 100) == 2:
            return resp.json()
        return False
    if method == "GET":
        if post_data:
            parameters = urllib.urlencode(post_data)
            url = url + "?" + parameters
        resp = requests.get(url, headers=headers)
    #if resp.links:
            #print resp.links
        #print resp.links['next']['url']
        if (resp.status_code / 100 == 2):
            if resp.links:
            	#print "NEXT url now.."
                return resp.json(), resp.links['next']['url']
            else:
                #print "no NEXT url now.."
                return resp.json(), "";

    if method == "PUT":
        resp = requests.put(url, data=post_data, headers=headers)
        if resp.status_code / 100 == 2:
            return True
        return False
    if method == "DELETE":
        resp = requests.delete(url, data=post_data, headers=headers)
        if resp.status_code / 100 == 2:
            # print("DELETE", url, resp)
            return True
    return False


def sent_msg(msg, file=None):
    if not msg:
        return
    data = {
        "roomId": SPARKROOMID,
        "text": msg
    }
    if file:
        data["file"] = file

    rep = make_request("messages", "POST", simplejson.dumps(data))
    #print rep
    return rep


def getmessages(roomid):
    if not roomid:
        return False

    data = {
        "roomId": roomid,
        "max": 1000
    }
    rep, nexurl = make_request(SPARKURL + "memberships", "GET", data)
    data = simplejson.loads(simplejson.dumps(rep).encode('UTF-8'))
    count =  len(data["items"]);
    #print "----------First : "
    #print count

    #print nexurl
    while nexurl:
        rep1, nexurl = make_request(nexurl, "GET", "")
    #print rep1
        data1 = simplejson.loads(simplejson.dumps(rep1).encode('UTF-8'))
        #print len(data1["items"]);
        count =  count + len(data1["items"]);
    #data = data + data1


    #print "Out"


    return count


app = Flask(__name__)


@app.route("/count")
def count():
    # spark.sent_msg("Helllo")

    return str(getmemberships(SPARKROOMID))


@app.route("/")
def index():
    return render_template("graphic.html")


@app.route("/dark")
def dark():
    return render_template("graphic.dark.html")

@app.route("/bg")
def bg():
    return render_template("graphic.bg.html")


if __name__ == "__main__":
    app.run()
