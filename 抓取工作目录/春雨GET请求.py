#coding=utf-8
import urllib
import urllib2
import re
import json, thread, threading,time,random

# -----------代理列表-----------
IPANDPORT = []

# 地区列表

Province = [
    'province%22%3A%22%E5%8C%97%E4%BA%AC%E5%B8%82%22%2C%22',
    'province%22%3A%22%E6%B9%96%E5%8C%97%E7%9C%81%22%2C%22',
    'province%22%3A%22%E5%A4%A9%E6%B4%A5%E5%B8%82%22%2C%22',
    'province%22%3A%22%E6%B2%B3%E5%8C%97%E7%9C%81%22%2C%22',
    'province%22%3A%22%E5%B1%B1%E8%A5%BF%E7%9C%81%22%2C%22',
    'province%22%3A%22%E8%BE%BD%E5%AE%81%E7%9C%81%22%2C%22',
'province%22%3A%22%E9%BB%91%E9%BE%99%E6%B1%9F%E7%9C%81%22%2C%22',
'province%22%3A%22%E4%B8%8A%E6%B5%B7%E5%B8%82%22%2C%22',
'province%22%3A%22%E6%B1%9F%E8%8B%8F%E7%9C%81%22%2C%22',
'province%22%3A%22%E6%B5%99%E6%B1%9F%E7%9C%81%22%2C%22',
'province%22%3A%22%E5%AE%89%E5%BE%BD%E7%9C%81%22%2C%22',
'province%22%3A%22%E7%A6%8F%E5%BB%BA%E7%9C%81%22%2C%22',
'province%22%3A%22%E6%B1%9F%E8%A5%BF%E7%9C%81%22%2C%22',
'province%22%3A%22%E5%B1%B1%E4%B8%9C%E7%9C%81%22%2C%22',
'province%22%3A%22%E6%B2%B3%E5%8D%97%E7%9C%81%22%2C%22',
'province%22%3A%22%E6%B9%96%E5%8D%97%E7%9C%81%22%2C%22',
'province%22%3A%22%E5%B9%BF%E4%B8%9C%E7%9C%81%22%2C%22',
'province%22%3A%22%E5%B9%BF%E8%A5%BF%E5%A3%AE%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8C%BA%22%2C%22',
'province%22%3A%22%E6%B5%B7%E5%8D%97%E7%9C%81%22%2C%22',
'province%22%3A%22%E9%87%8D%E5%BA%86%E7%9C%81%22%2C%22',
'province%22%3A%22%E5%9B%9B%E5%B7%9D%E7%9C%81%22%2C%22',
'province%22%3A%22%E8%B4%B5%E5%B7%9E%E7%9C%81%22%2C%22',
'province%22%3A%22%E4%BA%91%E5%8D%97%E7%9C%81%22%2C%22',
'province%22%3A%22%E8%A5%BF%E8%97%8F%E7%9C%81%22%2C%22',
'province%22%3A%22%E9%99%95%E8%A5%BF%E7%9C%81%22%2C%22',
'province%22%3A%22%E7%94%98%E8%82%83%E7%9C%81%22%2C%22',
'province%22%3A%22%E9%9D%92%E6%B5%B7%E7%9C%81%22%2C%22',
'province%22%3A%22%E5%AE%81%E5%A4%8F%E5%9B%9E%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8C%BA%22%2C%22',
'province%22%3A%22%E6%96%B0%E7%96%86%E7%BB%B4%E5%90%BE%E5%B0%94%E8%87%AA%E6%B2%BB%E5%8C%BA%22%2C%22',
'province%22%3A%22%E5%8F%B0%E6%B9%BE%E7%9C%81%22%2C%22',
'province%22%3A%22%E5%86%85%E8%92%99%E5%8F%A4%E8%87%AA%E6%B2%BB%E5%8C%BA%22%2C%22',
'province%22%3A%22%E9%A6%99%E6%B8%AF%E7%89%B9%E5%88%AB%E8%A1%8C%E6%94%BF%E5%8C%BA%22%2C%22',
'province%22%3A%22%E6%BE%B3%E9%97%A8%E7%89%B9%E5%88%AB%E8%A1%8C%E6%94%BF%E5%8C%BA%22%2C%22',
]
# -----------函数块-----------
def getTheRemoteAgent():
    f = open("proxy_list.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

# 拼接第一级页面字符串
def combolFirstUrl(url, index, province):
    # 匹配页码
    pattern = re.compile(r'page=\d+&')
    match = re.findall(pattern, url)
    result, number = re.subn(pattern, 'page=%d&' % index, url)
    print result
    # 匹配省
    pattern = re.compile(r'provinceMD')
    match = re.findall(pattern, result)
    result_1, number = re.subn(pattern, province, result)
    print result_1
    return result_1
# 根据doc_id拼接第二季页面字符串
def combolSecondUrl(url, string):
    pattern = re.compile(r'doctor/.*?/homepage')
    match = re.findall(pattern, url)
    result, number = re.subn(pattern, 'doctor/%s/homepage' % string, url)
    print result
    return result

# 发起请求
def setUpGet(url):
    # 设置代理
    index = random.randint(0, len(IPANDPORT)-2)
    print IPANDPORT[index]
    proxy = {'http':IPANDPORT[index]}
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    headers = {'User-Agent': 'Chunyuyisheng/7.5.2 (iPhone; iOS 9.1; Scale/2.00)',
                'Connection': 'Keep-Alive'}
    req = urllib2.Request(url)

    res_data = urllib2.urlopen(req)
    res = res_data.read()
    print res
    return res

# 输出到文件
def loadToFile(*rags):
    f = open("产科.txt", "a")
    if f:
        for rag in rags:
            if isinstance(rag, int):
                f.write(str(rag)+',')
            else:
                f.write(rag.encode('UTF-8')+',')
        f.write('\n')
        f.close()
    else:
        print "open file failed"

# 解析json获得doc_id
def getDoctorsId(response):
    result = json.loads(response)
    print len(result)
    arr = []
    for docs in result:
        print docs['doc_id']
        arr.append(docs['doc_id'])
    return arr


# 获取页面第二级数据
def getDataByDocID(url, docIDArr):
    for docId in docIDArr:
        attempts = 0
        print docId
        url = combolSecondUrl(baseUrl_2, docId)
        try:
            response = setUpGet(url)
        except Exception, e:
            try:
                response = setUpGet(url)
            except Exception, e:
                try:
                    response = setUpGet(url)
                except Exception, e:
                    pass

        # 解析数据并录入txt
        result = json.loads(response)
        #需要获得的参数
        # 姓名
        name = result['doctor_detail']['doc_name']
        print name
        # 科室
        clinic_name = result['doctor_detail']['clinic_name']
        # 职称
        title = result['doctor_detail']['title']
        # 医院
        hospital = result['doctor_detail']['hospital']
        # 图文咨询费
        graph = result['doctor_detail']['graph']['price']
        # 图文咨询数
        graph_num = result['doctor_detail']['graph']['purchase_num']
        # 电话咨询费
        telephonePrice = result['doctor_detail']['telephone']['tel_price_4_minute']
        # 电话咨询数
        telephone_num = result['doctor_detail']['telephone']['purchase_num']
        # 院后指导费用
        hospitalGuidePrice = result['doctor_detail']['hospital_guide']['price']
        # 院后指导数
        hospitalGuide_num = result['doctor_detail']['hospital_guide']['purchase_num']
        # 咨询套餐费
        familyDoc_price = result['doctor_detail']['family_doc']['price']['fweek_price']
        # 咨询套餐数
        familyDoc_num = result['doctor_detail']['family_doc']['purchase_num']
        # 视频咨询费
        videoPrice = result['doctor_detail']['video']['price']
        # 视频咨询数
        video_num = result['doctor_detail']['video']['purchase_num']
        # 预约挂号费
        add_hsp_tag_price = result['doctor_detail']['add_hsp_reg']['price']
        # 预约挂号数
        add_hsp_tag_num = result['doctor_detail']['add_hsp_reg']['purchase_num']
        # 粉丝数
        fans_count = result['doctor_detail']['fans_count']
        # 服务人数
        reply_num = result['doctor_detail']['reply_num']
        # 收到心意数
        thank_num = result['doctor_detail']['thank_num']
        loadToFile(name,clinic_name,title,hospital,graph,graph_num,telephonePrice,telephone_num,
                   hospitalGuidePrice,hospitalGuide_num,
                   familyDoc_price,familyDoc_num,
                   videoPrice,video_num,
                   add_hsp_tag_price,add_hsp_tag_num,
                   fans_count,reply_num,thank_num)

def start(baseUrl_1, baseUrl_2, tmpIndex, province):
    reqUrl = combolFirstUrl(baseUrl_1, tmpIndex, province)
    response = setUpGet(reqUrl)
    docIDArr = getDoctorsId(response)
    getDataByDocID(baseUrl_2, docIDArr)
# -----------函数块-----------
# 多线程
class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
    def run(self):
        apply(self.func, self.args)


# 拼接Url
baseUrl_1_1 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%221%22%7D&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&mac=e4%3a6b%3ab7%3af3%3a24%3a1b&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_2 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%222%22%7D&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&mac=e4%3a6b%3ab7%3af3%3a24%3a1b&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_4 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%224%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_3 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%223%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_8 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%228%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_21 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%2221%22%7D&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&mac=e4%3a6b%3ab7%3af3%3a24%3a1b&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_9 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%229%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_12 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%2212%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_7 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%227%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_17 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%2217%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_13 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%2213%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_15 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%2215%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_14 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%2214%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_11 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%2211%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_16 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%2216%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_22 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%2222%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_6 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%226%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1_19 = "https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&filter=%7B%22provinceMDclinic_no%22%3A%2219%22%7D&&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"


baseUrl_2 = "https://api.chunyuyisheng.com/api/v6/doctor/clinic_web_eeb65e65132f41a5/homepage/?app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&mac=c4%3A6a%3Ab7%3A53%3A24%3A1a&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"

keshiArr = [baseUrl_1_1, baseUrl_1_2, baseUrl_1_4, baseUrl_1_3,
            baseUrl_1_8, baseUrl_1_21 ,baseUrl_1_9 ,baseUrl_1_12,
            baseUrl_1_7, baseUrl_1_17, baseUrl_1_13, baseUrl_1_15,
            baseUrl_1_14, baseUrl_1_11,baseUrl_1_16, baseUrl_1_22,
            baseUrl_1_6 ,baseUrl_1_19
            ]
rang = range(1, 6)

# for keshi in keshiArr:
# for province in Province:
#     for ra in rang:
#         print ra
#         start(baseUrl_1_1, baseUrl_2, ra, province)

# 读取代理
getTheRemoteAgent()
# 多线程
threads = []
for province in Province:
    for ra in rang:
        t1 = MyThread(start, (baseUrl_1_21, baseUrl_2, ra, province))
        # threads.append(t1)
        t1.setDaemon(True)
        t1.start()
        t1.join()
        # start(baseUrl_1, baseUrl_2, ra)
# for t in threads:
#     t.setDaemon(True)
#     t.start()
#
# for t in threads:
#     t.join()
print "Exiting Main Thread"





