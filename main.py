from sys import argv

import alert
import requests
import os
import FlaskApp.database
from checkdefaced import check
from screenshot import screenshot

script, url, receiver = argv


def main(url, receiver):
    al = alert.Alert()
    print(url)
    db = FlaskApp.database.Database("site")
    data = db.get_single_data({"url": url})
    if data is None:
        print("URL ko co trong csdl")
        return None
    id_map = str(data["_id"])
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
    defaced_result = "false"
    if defaced:
        #al.sendBot(url, img_path)
        subject = "Website Defacement"
        message = f"You website was defaced!\nURL: {url}"
        #al.sendMessage(receiver, subject, message, img_path)
        defaced_result = "true"
        message = (
            f"You website was defaced!\nURL: {url}"
        )
        al.sendMessageToEndpoint(url, receiver, defaced_result, message, img_path, id_map)
        
        print("Website was defaced!")
        return None
    
    al.sendMessageToEndpoint(url, receiver, defaced_result, "Everything oke!", img_path, id_map)
    print("Everything oke!")
    

main(url, receiver)
