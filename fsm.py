#-*- coding:utf-8 -*-
from transitions.extensions import GraphMachine

import requests
import re
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print ("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print ("Encountered an end tag :", tag)

    def handle_data(self, data):
        print ("Encountered some data  :", data)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
    #condition
    def is_to_error(self, update):
        text = update.message.text.upper()
        if 'ERROR' in text:
            return 1
        return 0
    
    def is_Init_to_Exchangerate(self, update):
        text = update.message.text.upper()
        if text == 'A':
            return 1
        return 0
          
    def is_Exchangerate_to_Init(self, update):
        text = update.message.text.upper()
        return text == 'Q'
    
    def is_Exchangerate_to_Exchangerate_parse(self, update):
        text = update.message.text.upper()        
        if text == 'USD':
            return 1
        if text == 'EUR':
            return 1
        if text == 'GBP':
            return 1
        if text == 'AUD':
            return 1
        if text == 'JPY':
            return 1
        if text == 'CNY':
            return 1
        return 0
        
    def is_Exchangerate_to_Exchangerate_other(self, update):
        text = update.message.text.upper()        
        if text == 'O':
            return 1
        return 0


    def is_Init_to_Avg(self, update):
        text = update.message.text.upper()
        if text == 'B':
            return 1
        return 0

    def is_Avg_to_Init(self, update):
        text = update.message.text.upper()
        return text == 'Q'
        
    def is_Avg_to_Avg_parse(self, update):
        text = update.message.text.upper()
        if text == 'A':
            return 1
        if text == 'B':
            return 1
        if text == 'C':
            return 1
        if text == 'D':
            return 1
        if text == 'E':
            return 1
        if text == 'F':
            return 1
        if text == 'G':
            return 1
        if text == 'H':
            return 1
        return 0
        is_Stock_to_Stock_parse
    def is_Avg_to_Avg_other(self, update):
        text = update.message.text.upper()
        return text == 'O'

    def is_Init_to_Stock(self, update):
        text = update.message.text.upper()
        if text == 'C':
            return 1  
        update.message.reply_text("歡迎使用理財 ChatBot\n\n(1)\t輸入 A 查詢當日匯率\n\n(2)\t輸入 B 查詢國際指數\n\n(3)\t輸入 C 查詢當日行情\n\n(4)\t輸入 error + 狀況 回報錯誤\n\n")
        return 0
    
    def is_Stock_to_Stock_parse(self, update):
        text = update.message.text.upper()
        temp = int(text)
        if temp / 1000 > 0:
            if temp / 1000 < 10:
                return 1    
        update.message.reply_text("股票不存在\n")
        return 0
        
    def is_Stock_to_Init(self, update):
        text = update.message.text.upper()
        return text == 'Q'
        
    #Init
    def on_enter_Init(self, update):
        print('Enter Init')     
        update.message.reply_text("歡迎使用理財 ChatBot\n\n(1)\t輸入 A 查詢當日匯率\n\n(2)\t輸入 B 查詢國際指數\n\n(3)\t輸入 C 查詢當日行情\n\n(4)\t輸入 error + 狀況 回報錯誤\n\n")

    #Exchangerate
    def on_enter_Exchangerate(self, update):
        update.message.reply_text("歡迎查詢當日匯率\n\n(1)\t輸入幣別查詢匯率\n範例 : 輸入 USD 查詢美金\n\n美金 (USD), 歐元 (EUR),\n英鎊 (GBP), 澳幣 (AUD),\n日圓 (JPY),人民幣 (CNY)\n\n(2)\t輸入 O 查詢其他\n\n(3)\t輸入 Q 離開\n\n(4)\t輸入 error + 狀況 回報錯誤\n\n")

    def on_exit_Exchangerate(self, update):
        print('Leaving Exchangerate')   
             
    #Exchangerate_parse
    def on_enter_Exchangerate_parse(self, update):
        data = requests.get('http://rate.bot.com.tw/xrt?Lang=zh-TW')
        temp = data.text.replace(' ', '')
        tar = update.message.text.upper()
        index = temp.find(tar)
        temp = temp[index:index+300]
        temp = re.sub(r'<[^>]*>', '', temp)
        temp = re.sub(r'[^0-9.\n]', '', temp)
        temp = temp[7:]
        temp = re.sub('\n', '  ', temp)
        update.message.reply_text('買入  賣出\n'+temp+'\n\n資料來源台灣銀行 http://rate.bot.com.tw/xrt?Lang=zh-TW')
        self.go_back(update)

    def on_exit_Exchangerate_parse(self, update):
        print('Leaving Exchangerate_parse')

    #Exchangerate_other
    def on_enter_Exchangerate_other(self, update):
        update.message.reply_text('請參考台灣銀行 http://rate.bot.com.tw/xrt?Lang=zh-TW')
        self.go_back(update)

    def on_exit_Exchangerate_other(self, update):
        print('Leaving Exchangerate_other')
       
    #Avg
    def on_enter_Avg(self, update):
        update.message.reply_text("查詢國際指數\n\n(1)\t輸入 A 查詢台灣加權指數\n\n(2)\t輸入 B 查詢日經225指數\n\n(3)\t輸入 C 查詢香港恆生指數\n\n(4)\t輸入 D 查詢上海綜合指數\n\n(5)\t輸入 E 查詢道瓊工業指數\n\n(6)\t輸入 F 查詢那斯達克指數\n\n(7)\t輸入 G 查詢德國XetraDAX指數\n\n(8)\t輸入 H 查詢英國金融時報指數\n\n(9)\t輸入 O 查詢其他\n\n(10)\t輸入 Q 離開\n\n(11)\t輸入 error 回報錯誤\n\n")

    def on_exit_Avg(self, update):
        print('Leaving Avg')
        
    #Avg_parse
    def on_enter_Avg_parse(self, update):
        data = requests.get('https://tw.money.yahoo.com/marketindex')
        temp = data.text.replace(' ', '')
        text = update.message.text.upper()
        tar = 'TWII'
        if text == 'A':
            tar = 'TWII'
        if text == 'B':
            tar = 'N225'
        if text == 'C':
            tar = 'HSI'
        if text == 'D':
            tar = '000001.SS'
        if text == 'E':
            tar = 'DJI'
        if text == 'F':
            tar = 'IXIC'
        if text == 'G':
            tar = 'GDAXI'
        if text == 'H':
            tar = 'FTSE'
        index = temp.find(tar)
        temp = temp[index+72:index+130]
        temp = re.sub(r'<[^>]*>', '', temp)
        temp = re.sub(r'[^0-9.\n]', '', temp)
        temp = re.sub('\n', '', temp)
        if text == 'A':
            temp = '台灣加權指數\n' + temp
        if text == 'B':
            temp = '日經225指數\n' + temp
        if text == 'C':
            temp = '香港恆生指數\n' + temp
        if text == 'D':
            temp = '上海綜合指數\n' + temp
        if text == 'E':
            temp = '道瓊工業指數\n' + temp
        if text == 'F':
            temp = '那斯達克指數\n' + temp
        if text == 'G':
            temp = '德國XetraDAX指數\n' + temp
        if text == 'H':
            temp = '英國金融時報指數\n' + temp
        update.message.reply_text(temp+'\n\n資料來源Yahoo理財 https://tw.money.yahoo.com/marketindex')
        self.go_back(update)
        
    def on_exit_Avg_parse(self, update):
        print('Leaving Avg_parse')
        
    #Avg_other
    def on_enter_Avg_other(self, update):
        update.message.reply_text('請參考Yahoo理財 https://tw.money.yahoo.com/marketindex')
        self.go_back(update)

    def on_exit_Avg_other(self, update):
        print('Leaving Avg_other')    
            
    #Stock
    def on_enter_Stock(self, update):
        print('Enter Stock')     
        update.message.reply_text("查詢當日行情\n\n(1)\t輸入股票代號\n範例 : 輸入 2330 查詢 台積電(2330)\n輸入 2317 查詢 鴻海(2317)\n輸入 2882 查詢 國泰金(2881)\n\n(2)\t輸入 Q 離開\n\n(3)\t輸入 error + 狀況 回報錯誤\n\n")

    def on_exit_Stock(self, update):
        print('Leaving Stock')     
         
    #Stock_parse
    def on_enter_Stock_parse(self, update):
        print('Enter Stock_parse')     
        src = update.message.text.upper()
        print(src)
        data = requests.get('https://www.google.com.tw/search?biw=734&bih=754&q=%E8%82%A1%E5%83%B9+' + src + '&oq=%E8%82%A1%E5%83%B9+' + src + '&gs_l=serp.3..0i8i30k1.760.913.0.1592.2.2.0.0.0.0.159.302.0j2.2.0....0...1.1.64.serp..0.1.158.I_c-Lvh8thk')
        temp = data.text.replace(' ', '')
        
        tar = '搜尋結果'
        index = temp.find(tar)
        nm = temp[index+20:index+75]
        nm = re.sub(r'<[^>]*>', '', nm)
        nm = re.sub(r'[a-zA-Z<>/,.+-_`\"\']', '', nm)
        
        tar = '(TPE)'
        index = temp.find(tar)
        temp = temp[index+420:index+450]
        temp1 = temp
        temp = re.sub(r'157%', '', temp)
        if temp1 == temp :
            update.message.reply_text('無法查詢或股票不存在')
            self.go_back(update)
        else :
            temp = re.sub(r'<[^>]*>', '', temp)
            temp = re.sub(r'[^0-9.\n]', '', temp)
            temp = re.sub('\n', '', temp)
            print(temp)
            update.message.reply_text(nm+'\n'+temp+'\n\n資料來源https://www.google.com.tw/search?biw=734&bih=754&q=%E8%82%A1%E5%83%B9+' + src + '&oq=%E8%82%A1%E5%83%B9+' + src + '&gs_l=serp.3..0i8i30k1.760.913.0.1592.2.2.0.0.0.0.159.302.0j2.2.0....0...1.1.64.serp..0.1.158.I_c-Lvh8thk')
            self.go_back(update)

    def on_exit_Stock_parse(self, update):
        print('Leaving Stock_parse')     
       
    #error 
    def on_enter_error(self, update):
        print('Enter error')
        mess = update.message.text.upper()
        print('\n\n***********\nERROR:' + mess + '\n***********\n\n')
        self.go_back(update)

    def on_exit_error(self, update):
        update.message.reply_text('已收到錯誤回報')
        print('Leaving error')     

