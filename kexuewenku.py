#获取cookie
import requests
import json
import re
from tqdm import tqdm
import time

def get_name(book_url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Access-Control-Request-Headers': 'accesstoken',
        'Access-Control-Request-Method': 'POST',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
    responsepdf = requests.get(book_url,headers=headers)
    if responsepdf.status_code == 200:
        q='title>'
        h='</title'
        j=q+'(.*?)'+h
  #print(responsepdf.text)
        return re.findall(j, responsepdf.text)[0]

def post_id(id_book):
    url='http://api/file/add'
    params='{"params":{"userName":"Guest","userId":"b31f5c2e52b211eab864005056952de2","file":"http://'+id_book+'.pdf"}}'
    type_biao='http'
    data={
        "params":params,
        "type":type_biao
        }
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Access-Control-Request-Headers': 'accesstoken',
        'Access-Control-Request-Method': 'POST',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
    rep = requests.post(url=url, data=data, headers=headers)
    id_data=json.loads(rep.text)
    return id_data['result']

def get_pdf(result):
    url='http://api/file/'+result+'/getDocumentbuffer'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Access-Control-Request-Headers': 'accesstoken',
        'Access-Control-Request-Method': 'POST',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
    responsepdf = requests.get(url,headers=headers)
    name=name_bo+".pdf"
    if responsepdf.status_code == 200:
        with open(name , "wb") as code:
            code.write(responsepdf.content)

def download(url: str, fname: str):
    # 用流stream的方式获取url的数据
    resp = requests.get(url, stream=True)
    # 拿到文件的长度，并把total初始化为0
    total = int(resp.headers.get('content-length', 0))
    # 打开当前目录的fname文件(名字你来传入)
    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

            
def big_file_pre(id_book):
    url='http://spi/v2/doc/pretreat?r='+str(int(round(time.time() * 1000)))
    params='{"params":{"userName":"Guest","userId":"b31f5c2e52b211eab864005056952de2","file":"http:///'+id_book+'.pdf"}}'
    type_biao='http'
    data={
        "filetype":type_biao,
        "zooms":"-1,100",
        "tileRender":"false",
        "fileuri":params,
        "pdfcache":"true",
        "callback":""
        }
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Access-Control-Request-Headers': 'accesstoken',
        'Access-Control-Request-Method': 'POST',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
    rep = requests.post(url=url, data=data, headers=headers)
    id_data=json.loads(rep.text)
    return id_data['resultBody']['taskid']

def big_file_qu(taskid):
    url='http://api/v2/task/'+taskid+'/query?r='+str(int(round(time.time() * 1000)))
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Access-Control-Request-Headers': 'accesstoken',
        'Access-Control-Request-Method': 'POST',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
    res_qu= requests.get(url,headers=headers)
    return res_qu.text

book_url=str(input("请输入书籍页面网站...")).strip()
id_book=book_url.split("=")[1]
r_e='record'
md='md5'
if id_book=='':
    print("请输入网站...")
else:
    name_bo=get_name(book_url)
    print(name_bo)
    result=post_id(id_book)
    if result=="OutOfFileSizeLimit":
        taskid=big_file_pre(id_book)
        while 2>1:
            qu_text=big_file_qu(taskid)
            print(qu_text)
            if  r_e in qu_text:
                cl_re=json.loads(qu_text)
                result=json.loads(cl_re['resultBody']['record'])['uuid']
                print(result)
                break
            elif md in qu_text:
                cl_re=json.loads(qu_text)
                result=cl_re['resultBody']['uuid']
                print(result)
                break
            else:
                print("获取循环中...")
                time.sleep(2)
    else:
        print(result)
    url='http://api/file/'+result+'/getDocumentbuffer'
    name=name_bo+".pdf"
    print("开始下载...")
    download(url,name)
         #get_pdf(result)
    

