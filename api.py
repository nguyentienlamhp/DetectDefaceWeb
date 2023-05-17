import json
import os
import sys

import requests
from flask import Flask, request, send_file

import bson

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import re
import alert
import FlaskApp.database
from checkdefaced import check
from screenshot import screenshot


def slug(string):
    pattern = "|%[0-9]{1,}|%|--|#|;|/\*|'|\"|\\\*|\[|\]|xp_|\&gt|\&ne|\&lt|&"
    result = re.sub(pattern, "", string)
    return result


app = Flask(__name__)

@app.route("/checkdeface", methods=["GET"])
def checkdomain():
    id_domain = request.args.get('id')
    db = FlaskApp.database.Database("site")
    al = alert.Alert()
    res = {}
    if id_domain is None:
        res = {"code":406,"status": "Id not config !"}
        return res
    #data = db.get_single_data({"_id": ObjectId(id_domain)})
    data = db.get_single_data({"_id": bson.ObjectId(id_domain)})
    if data is None:
        res = {"code":406,"status": " Ko tim thay id!"}
        return res
    url = data["url"] 
    receiver = data["email"]
    try:
        response = requests.get(url)
    except requests.ConnectionError:
        res = {"code":500, "status": "500 Internal Server Error!"}
        return res
    if (response.status_code != 200) and (response.status_code != 302):
        res = {"code":500,"status": "URL Invalid! " + url}
    else:
        img_path = screenshot(url)
        #test
        #al.sendMessageToEndpoint("receiver", "subject", "message", img_path)
        #al.sendMessage("receiver", "subject", "message", img_path)
        #end test
        defaced = check(img_path)
        if defaced:
            subject = "Website Defacement"
            defaced_result = "true"
            message = (
                f"You website was defaced!\nURL: {url}"
            )
            al.sendMessageToEndpoint(url, receiver, defaced_result, message, img_path, id_domain)
            #al.sendBot(url, img_path)
            #al.sendMessage(receiver, subject, message, img_path)
            res = {"code":200,"status": "Website was defaced!", "defaced": "true"}
            print("Website was defaced!")
        else:
            defaced_result = "false"
            message = "Everything oke!"
            al.sendMessageToEndpoint(url, receiver, defaced_result, message, img_path, id_domain)
            res = {"code":200,"status": "Everything oke!"}
            print("Everything oke!")
    return res

@app.route("/checkdeface", methods=["POST"])
def checkdeface():
    db = FlaskApp.database.Database("site")
    al = alert.Alert()
    res = {}
    body = json.loads(request.data)
    if len(body["key"]) == 0 and len(body["path"]) == 0: 
        res = {"status": "400 Bad Request!"}
        return res
    else: 
        key = slug(body["key"])
    
    active_key = {"active_key": key}
    data = db.get_single_data(active_key)
    if data is None:
        res = {"status": "404 Key Invalid!"}
        return res
    url = data["url"] + body["path"]
    receiver = data["email"]
    id_map = str(data["_id"])
    try:
        response = requests.get(url)
    except requests.ConnectionError:
        res = {"status": "500 Internal Server Error!"}
        return res

    if (response.status_code != 200) and (response.status_code != 302):
        res = {"status": "URL Invalid! " + url}
    else:
        #update status
        endpoint = os.environ["API_URL_UPDATE_STATUS"]
        if (endpoint is None):
            endpoint = "https://svc.mitc.vn/data/module4/updateStatusRunning?type=0"
        headers = {'content-type': 'application/json'}
        r = requests.get(endpoint + "&id="+id_map, headers=headers)
        print(r.status_code)
        print(r.reason)
        
        img_path = screenshot(url)
        defaced = check(img_path)
        if defaced:
            
            subject = "Website Defacement"
            defaced_result = "true"
            message ="You website was defaced!"
            al.sendMessageToEndpoint(url,receiver, defaced_result, message, img_path, id_map)
            #al.sendBot(url, img_path)
            #al.sendMessage(receiver, subject, message, img_path)
            res = {"status": "Website was defaced!"}
            print("Website was defaced!")
        else:
            defaced_result = "false"
            message = "Everything oke!"
            al.sendMessageToEndpoint(url,receiver, defaced_result, message, img_path, id_map)
            res = {"status": "Everything oke!"}
            print("Everything oke!")
    return res

@app.route('/download')
def download_file():
    file_path = request.args.get('path')
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8088")
