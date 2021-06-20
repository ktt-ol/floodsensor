import logging
import conf
import http.client, urllib, ssl

# Send a message thru Pushover
def pushover_send(message):
    logging.info("Pushover notification")
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
        "token":    conf.pushover_token,
        "user":     conf.pushover_user,
        "priority": conf.pushover_priority,
        "retry":    conf.pushover_retry,
        "expire":   conf.pushover_expire,
        "message":  message,
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()