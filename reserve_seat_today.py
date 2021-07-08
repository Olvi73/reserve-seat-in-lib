# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 15:14:25 2021

@author: Oliver
"""
import requests
import re
import time
import execjs
from bs4 import BeautifulSoup

# content=""

lib_dic={"1141":"建筑工程阅览室（一）C801","1143":"建筑工程阅览室（二）C803"}

mheaders =  {
'Host':        'wechat.v2.traceint.com',
'User-Agent':        'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000731) NetType/WIFI Language/zh_CN',
'Accept':        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8',
'Accept-Encoding':        'gzip, deflate',
'Accept-Language':        'zh-CN,en-US;q=0.8'
}
mcookies = dict(FROM_TYPE="weixin" ,wechatSESS_ID="",
        Hm_lvt_7ecd21a13263a714793f376c18038a87="",
        Hm_lpvt_7ecd21a13263a714793f376c18038a87="",
    SERVERID=""
)

def parse_trace(content):
        try:
            cookie=[]
            content += ' ;'
            
            pattern = re.compile(r'SERVERID\=\w+\|\d{10}\|\d{10}')
            SERVERID = pattern.search(content).group(0)
            cookie.append(SERVERID.replace("SERVERID=", ""))
            
            pattern = re.compile(r'wechatSESS_ID\=\w+(?=[\s;])')
            wechatSESS_ID = pattern.search(content).group(0)
            cookie.append(wechatSESS_ID.replace("wechatSESS_ID=", ""))
            
            pattern = re.compile(r'(?<=Hm_lvt_\w{32}\=)(\d{10}|,)+(?=[\s;])')
            Hm_lvt_time = pattern.search(content).group(0)
            cookie.append(str(Hm_lvt_time))
            
            pattern = re.compile(r'(?<=Hm_lpvt_\w{32}\=)\d{10}(?=[\s;])')
            Hm_lpvt_time = pattern.search(content).group(0)
            cookie.append(str(Hm_lpvt_time))
            #
            # SERVERID_time_2 = re.compile(r'(?<=SERVERID\=\w{32}\|\d{10}\|)\d{10}(?=[\s;])')
            # SERVERID_time_2 = pattern.search(content).group(0)

            #return '\n' + wechatSESS_ID + '\n'  +SERVERID +'\n' + "Hm_lvt_7ecd21a13263a714793f376c18038a87="+Hm_lvt_time +'\n'+"Hm_lpvt_7ecd21a13263a714793f376c18038a87="+Hm_lpvt_time
            return cookie
        except Exception as e:
            print(str(e))
            return []

def reserve_a_seat(content):
    cookie=parse_trace(content)
    roomValue ="1143" #教室编号
    seatValue="7,12"  #座位编号
    SERVERID=cookie[0]
    wechatSESS_ID=cookie[1]
    Hm_lvt_time=cookie[2]
    Hm_lpvt_time=cookie[3]
    mcookies['SERVERID']=SERVERID
    mcookies['wechatSESS_ID']=wechatSESS_ID
    mcookies['Hm_lvt_7ecd21a13263a714793f376c18038a87']=Hm_lvt_time
    mcookies['Hm_lpvt_7ecd21a13263a714793f376c18038a87']=Hm_lpvt_time
    rs = requests.Session()
    #hex 
    today_seatmap_page="https://wechat.v2.traceint.com/index.php/reserve/layout/libid=%s.html&%s"%(roomValue,int(time.time()))
    today_reserve_prefix="http://wechat.v2.traceint.com/index.php/reserve/get/"
    response = rs.get(url=today_seatmap_page,
                         timeout=3,
                         headers=mheaders,
                         cookies=mcookies,
                         verify=False)
    response.encoding = 'utf8'
    html_seatmap=response.text
    soup = BeautifulSoup(html_seatmap, 'html.parser')
    hexch_js_url = soup.find('script', src=re.compile(r'https://static\.wechat\.v2\.traceint\.com/template/theme2/cache/layout/.+?')).get('src', '')
    hexch_js_code = requests.get(hexch_js_url, verify=False)
    hexch_js_code.encoding = 'utf8'
    hexch_js_code = hexch_js_code.text
    pattern = re.compile(r'(?<=T\.ajax_get\().*?(?=,)')
    temp_ajax_url = pattern.search(hexch_js_code).group(0)
    ajax_url = temp_ajax_url.replace("AJAX_URL", "\""+today_reserve_prefix+"\"")
    # temp=hexch_js_code
    # pattern = re.compile(r'e\.dec\(\"\w+\"\)')
    # target = pattern.search(ajax_url).group(0)
    # hexch_js_code = re.sub(r'[A-Z]\.ajax_get', 'return %s ; T.ajax_get' % ajax_url, hexch_js_code)
    hexch_js_code = re.sub(r'T\.ajax_get', 'var final=%s; return final; T.ajax_get' % ajax_url, hexch_js_code)
    
    tmp = execjs.compile(hexch_js_code)
    http_hexch_seatinfo = tmp.call('reserve_seat', roomValue, seatValue)
    
    url_querenxuanzuo = "http://wechat.v2.traceint.com/index.php/reserve/get/libid=%s&%s=%s&yzm="%(roomValue,http_hexch_seatinfo,seatValue)
    respone=rs.get(url_querenxuanzuo,timeout=1,headers=mheaders,cookies=mcookies)
    if(respone.status_code==200):
        print("预约成功！教室：%s，座位号%s"%(lib_dic[roomValue],seatValue))

if __name__=="__main__":
    content=input("输入cookie:\n")
    reserve_a_seat(content)