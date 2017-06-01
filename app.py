#-*- coding:utf-8 -*-
import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine

import requests
from bs4 import BeautifulSoup

API_TOKEN = '336280146:AAHy-Gsybx3T6kd8hDKs3S3gKoZ83O5cQdA'
WEBHOOK_URL = ''

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'Init',
        'Exchangerate', #匯率 
                        #http://rate.bot.com.tw/xrt?Lang=zh-TW
        'Exchangerate_parse',
        'Exchangerate_other',
        
        'Avg',      #指數
                    #https://tw.money.yahoo.com/marketindex
        'Avg_parse',
        'Avg_other',
        
        'Stock',    #股票
                    #https://tw.stock.yahoo.com/h/getclass.php
        'Stock_parse',
        'error'

    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': [
                'Init',
                'Exchangerate',
                'Exchangerate_parse',
                'Exchangerate_other',
                'Avg',
                'Avg_parse',
                'Avg_other',
                'Stock',    
                'Stock_parse'
            ],
            'dest': 'error',
            'conditions': 'is_to_error'
        },
        {
            'trigger': 'advance',
            'source': 'Init',
            'dest': 'Exchangerate',
            'conditions': 'is_Init_to_Exchangerate'
        },
        {
            'trigger': 'advance',
            'source': 'Exchangerate',
            'dest': 'Init',
            'conditions': 'is_Exchangerate_to_Init'
        },
        {
            'trigger': 'advance',
            'source': 'Exchangerate',
            'dest': 'Exchangerate_parse',
            'conditions': 'is_Exchangerate_to_Exchangerate_parse'
        },
        {
            'trigger': 'advance',
            'source': 'Exchangerate',
            'dest': 'Exchangerate_other',
            'conditions': 'is_Exchangerate_to_Exchangerate_other'
        },
        {
            'trigger': 'advance',
            'source': 'Init',
            'dest': 'Avg',
            'conditions': 'is_Init_to_Avg'
        },
        {
            'trigger': 'advance',
            'source': 'Avg',
            'dest': 'Init',
            'conditions': 'is_Avg_to_Init'
        },
        {
            'trigger': 'advance',
            'source': 'Avg',
            'dest': 'Avg_parse',
            'conditions': 'is_Avg_to_Avg_parse'
        },
        {
            'trigger': 'advance',
            'source': 'Avg',
            'dest': 'Avg_other',
            'conditions': 'is_Avg_to_Avg_other'
        },
        {
            'trigger': 'advance',
            'source': 'Init',
            'dest': 'Stock',
            'conditions': 'is_Init_to_Stock'
        },
        {
            'trigger': 'advance',
            'source': 'Stock',
            'dest': 'Init',
            'conditions': 'is_Stock_to_Init'
        },
        {
            'trigger': 'advance',
            'source': 'Stock',
            'dest': 'Stock_parse',
            'conditions': 'is_Stock_to_Stock_parse'
        },
        {
            'trigger': 'go_back',
            'source': [
                'Exchangerate',
                'Avg',
                'Stock',
                'error'
            ],
            'dest': 'Init'
        },
        {
            'trigger': 'go_back',
            'source': [
                'Exchangerate_parse',
                'Exchangerate_other',
            ],
            'dest': 'Exchangerate'
        },
        {
            'trigger': 'go_back',
            'source': [
                'Avg_parse',
                'Avg_other',
            ],
            'dest': 'Avg'
        },
        {
            'trigger': 'go_back',
            'source': [
                'Stock_parse',
            ],
            'dest': 'Stock'
        },
    ],
    initial='Init',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():    
    data = requests.get('http://127.0.0.1:4040')
    temp = data.text.replace(' ', '')
    tar = 'command_line(http)'
    index = temp.find(tar)
    temp = temp[index+39:index+56]
    WEBHOOK_URL = 'https://' + temp + '/hook'
    print(WEBHOOK_URL)
    
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
