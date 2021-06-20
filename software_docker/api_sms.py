import logging
import conf
import http.client, urllib, ssl

# Send a message thru SMS
def sms_send(message):
    logging.info("SMS notification")
    conn    = http.client.HTTPSConnection("gateway.sms77.io")
    headers = {'Content-type': 'application/json'}
    with open('numbers.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            foo         = {"p": conf.sms_key, "to": row['phonenumber'], "text": message, "from": "Mainframe"}
            json_foo    = json.dumps(foo)
            conn.request('POST', '/api/sms', json_foo, headers)
            response    = conn.getresponse()
