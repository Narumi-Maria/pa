import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Cookie": '_zap=2626e2af-e6c2-44d7-821e-195ed025e731; d_c0="ADAZql7efRGPTpw1Gg2HLCSkh-1MBaOe_Sw=|1593284677"; _ga=GA1.2.1903820707.1593284678; _xsrf=71d5b321-8ccf-43b2-826e-a0becbea69fb; tst=r; _gid=GA1.2.860756019.1597981819; q_c1=ad05fdf5c0594b519ab609ec0f6bebb6|1597982232000|1594834782000; SESSIONID=DMmCb1zYFRBimlCNz981uInVRuunbVffg7GYEebYilt; JOID=UVASC0qKZaEdBVvwdoHc_uXUOGtjxSfDV2VhhSDOPOx7YTW4N3CFmEkMX_BwFnb9j193JMXdvxQXQfAtyL8r91w=; osd=WlkSBE-BbKESAFD5do7Z9ezUN25ozCfMUm5ohS_LN-V7bjCzPnCKnUIFX_91HX_9gFp8LcXSuh8eQf8ow7Yr-Fk=; capsion_ticket="2|1:0|10:1598021893|14:capsion_ticket|44:NzhiMWQxYzk5YWFkNDg5NGE1MjRiNWRlZGQ5YTRmMjE=|c47c098bf4d1edbb6ad8e40f817eeb1be8fdf5aaa9eb4f4575b98e168ffe16f9"; z_c0="2|1:0|10:1598021903|4:z_c0|92:Mi4xczV2Y0JnQUFBQUFBTUJtcVh0NTlFU1lBQUFCZ0FsVk5EeTh0WUFBejFWWlNJU1ZiaUxHbXl1cGREZTl1SmstODNR|19d1f82c11e1f2b81547e6289d277782d8f048921c6e12954efb8f49d9ba00e6"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1598021010,1598021885,1598022664,1598022682; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1598022795; _gat_gtag_UA_149949619_1=1; KLBRSID=57358d62405ef24305120316801fd92a|1598022801|1598016515'
}


def anaz(datas):
    dicList = []
    for i in datas:
        # 作者名
        author = i["author"]["name"]
        # 内容
        soup = BeautifulSoup(i["content"])
        p = soup.findAll("p")
        s = ''
        for j in p:
            s += f"{j.text}\n"
        dic = {
            "author":author,
            "content":s
        }
        dicList.append(dic)
    return dicList


def add(url, datas):
    time.sleep(0.5)
    print("重复一次")
    r = requests.get(url, headers=headers)
    r = r.json()
    datas.extend(r["data"])
    if r["paging"]["is_end"] == False:
        add(r["paging"]["next"], datas)


def main():
    datas = []
    url = 'https://www.zhihu.com/api/v4/questions/371179069/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=20&offset=0&sort_by=updated'
    add(url, datas)
    dicList = anaz(datas)
    exc = pd.DataFrame(dicList, columns=["author", "content"])
    exc.to_excel("所有答案.xlsx", index=False)


if __name__ == "__main__":
    main()
