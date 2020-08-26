#导入模块
import requests
import json
import time
import csv

def get_rank(first):
    #设置cookie,header,url,以及两个空列表用于存数据
    cookie = 'XID=0b1361e1dadcb0b84b394da2d160b5db; s_fid=4C051019B60F60D9-29E4C9BDDB4E31F3; s_vnum_n2_us=4%7C1; s_vi=[CS]v1|2F53E2F20515DB0B-40000836B0A6EEAB[CE]; geo=CN; ccl=Ni0b/ZipSwSG62Y+7mPCHA=='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        'Authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNTg2Mjk4MDU2LCJleHAiOjE2MDE4NTAwNTZ9.X4xjIG5bMpcOuL7uVXsz8jdjs77Z-y01lYxUUInScdclOOsDukzav03dl5xVf9cmERONjAGNJpcEyfRXumAPXQ',
        'Accept-Language': 'zh-Hans-CN',
        'cookie': cookie
    }

    url = 'https://amp-api.apps.apple.com/v1/catalog/cn/apps/930368978/reviews'
    summary = []
    summaryYear = []
    
    #每次循环2000个评论,然后休息30s以防被禁掉ip
    for num in range(first,first+2000,10):
        print(num)
        try:
            #设置get的参数
            payload = {
                'l':'zh-Hans-CN',
                'offset':str(num),
                'platform':'web',
                'additionalPlatforms':'appletv,ipad,iphone,mac'
            }
            
            #请求
            response = requests.get(url, headers=headers, params = payload)
            
            #数据处理
            text = response.json()
            print(text)
            dataList = text['data']
            for dataDic in dataList:
                data={}
                data['date'] = dataDic['attributes']['date']
                date = time.mktime(time.strptime(dataDic['attributes']['date'],"%Y-%m-%dT%H:%M:%SZ"))
                data['title'] = dataDic['attributes']['title']
                data['review'] = dataDic['attributes']['review']
                summary.append(data)
                #单独保存一年内的数据
                if (time.time() - date)<= 15768000*2:
                    summaryYear.append(data)
        except Exception as e:
            print(e)  #期间报错则直接返回然后休息30s(可能被禁掉了ip)
            return num,summary,summaryYear
    return num+10,summary,summaryYear

#将字典列表保存到csv
def write_csv_from_list_dict(filename, table, fieldnames, separator, quote):
    with open(filename, 'a', newline='', encoding = 'utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fieldnames,delimiter=separator,quoting=quote,quotechar='"')
        writer.writeheader()
        for row in table:  
            writer.writerow(row)
    
    #主程序
if __name__ == '__main__':
    num = 0
    while num <= 2200000:
        num,summary,summaryYear = get_rank(num)
        write_csv_from_list_dict('summary.csv', summary, ['date','title', 'review'], ',', csv.QUOTE_ALL)
        write_csv_from_list_dict('summaryYear.csv', summaryYear, ['date','title', 'review'], ',', csv.QUOTE_ALL)
        print('ok')
        time.sleep(30)
    
