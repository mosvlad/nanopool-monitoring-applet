import os
import signal
import json
import configparser

import requests

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

APPINDICATOR_ID = 'NANOPOOL'
WALLET = ""
UPDATE_DELAY = 0

def main():    
    icon_image = os.path.dirname(__file__) + "/eth.png"
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, icon_image, appindicator.IndicatorCategory.OTHER)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    get_info = gtk.MenuItem(label = 'Get info')
    get_info.connect('activate', result)
    menu.append(get_info)
    item_quit = gtk.MenuItem(label = 'Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def get_info():

    url = 'https://api.nanopool.org/v1/eth/user/' + WALLET
    account_response = requests.get(url)
    price_response = requests.get('https://api.nanopool.org/v1/eth/prices')
    json_result = json.loads(account_response.text)
    json_price = json.loads(price_response.text)
    
    if json_result['status'] == True:
        result =  "<i><font size = 1>" + json_result['data']['account'] + "</font></i><br><br>"

        result += "<b>Balance:</b> " + "<b><font color = '#00FF00'>" + json_result['data']['balance'] + " ETH</font></b><br>"
        result += "<b>Balance:</b> " + "<b><font color = '#00FF00'>" + str(round(float(json_result['data']['balance']) * float(json_price['data']['price_usd']), 2)) + " USD</font></b><br>"
        result += "<b>Hash Rate:</b> " + "<b><font color = '#00FF00'>" + json_result['data']['hashrate'] + "Mh/s </font></b><br><br>"
        result += "<b>Avg 1 hour :</b><i>" + json_result['data']['avgHashrate']['h1'] + "Mh/s </i> <br>"
        result += "<b>Avg 3 hour :</b><i>" + json_result['data']['avgHashrate']['h3'] + "Mh/s </i><br>"
        result += "<b>Avg 6 hour :</b><i>" + json_result['data']['avgHashrate']['h6'] + "Mh/s </i><br>"
        result += "<b>Avg 12 hour :</b><i>" + json_result['data']['avgHashrate']['h12'] + "Mh/s </i><br>"
        result += "<b>Avg 24 hour :</b><i>" + json_result['data']['avgHashrate']['h24'] + " Mh/s </i><br>"
    else:
        result = "<b><font color = '#FF0000'>" + json_result['error'] + "</font></b>"
    
    return result
        

def result(_):
    wdir=os.getcwd()
    notify.Notification.new("<b><i>STATUS</i></b>", get_info(), icon=os.path.join(wdir,"eth.png")).show()
    
def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    
    config = configparser.ConfigParser()
    config.read('options.ini')
    WALLET       = config.get('options', 'wallet')
    UPDATE_DELAY = config.get('options', 'delay')
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
