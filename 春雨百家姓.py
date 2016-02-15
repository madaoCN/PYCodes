#coding=utf-8
import urllib
import urllib2
import re
import json, thread, threading,time,random
import os

# -----------代理列表-----------
IPANDPORT = []
NAME = []
# 地区列表

officeTemp = ''

Province = ['北京市','天津市','河北省','山西省','内蒙古自治区','辽宁省',
            '吉林省','黑龙江省','上海市','江苏省','浙江省','安徽省',
            '福建省','江西省','山东省','河南省','湖北省','湖南省',
            '广东省','广西壮族自治区','海南省','重庆市','四川省',
            '贵州省','云南省','西藏省','陕西省','甘肃省','青海省',
            '宁夏回族自治区','新疆维吾尔族自治区','台湾省',
            '香港特别行政区','澳门特别行政区'
]

Clinic_no = [1,2,4,3,
             8,21,9,12,
             7,17,13,15,
             14,11,16,22,
             6,19]
# -----------函数块-----------
# 获取代理列表
def getTheRemoteAgent():
    f = open("proxy_list.txt", "r")
    for line in f:
        IPANDPORT.append(line)
    f.close()

# 获取百家姓
def getTheName():
    f = open('name.txt', "r")
    for name in  f:
        NAME.append(name)
    f.close()

# 拼接第一级页面字符串
def combolFirstUrl(url, pageNo, name, province, clinic_no):
    # 匹配页码
    pattern = re.compile(r'page=\d+&')
    match = re.findall(pattern, url)
    result_1, number = re.subn(pattern, 'page=%d&' % pageNo, url)

    #匹配Name
    nameStr = 'query=%s' % (urllib.quote(name.strip()))
    pattern = re.compile(r'query=@QUERY@')
    match = re.findall(pattern, result_1)
    result_2, number = re.subn(pattern, nameStr, result_1)

    # 匹配filter
    # filterStr = '{"province":"%s","clinic_no":"%s"}' % (province, clinic_no)
    filterStr = '{"clinic_no":"%s"}' % (clinic_no)
    filterStr_final = 'filter=%s' %  urllib.quote(filterStr)
    pattern = re.compile(r"filter=@FILTER@")
    match = re.findall(pattern, result_2)
    result_3, number = re.subn(pattern, filterStr_final, result_2)
    print result_3
    
    return result_3

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
    index = random.randint(0, len(IPANDPORT)-1)
    print IPANDPORT[index]
    proxy = {'http':IPANDPORT[index]}
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    headers = {'User-Agent': 'Chunyuyisheng/7.5.2 (Android 4.1.2;MI 1S_by_Xiaomi)'}
    req = urllib2.Request(url, headers=headers)

    try:
        res_data = urllib2.urlopen(req, timeout=20)
    except Exception, e:
        try:
           res_data = urllib2.urlopen(req, timeout=20)
        except Exception, e:
            try:
                res_data = urllib2.urlopen(req, timeout=20)
            except Exception, e:
                pass
    res = res_data.read()
    print res
    return res

# 输出到文件
def loadToFile(*rags):
    path = os.path.expanduser(r'~/Desktop/data/%s.txt' % (officeTemp))
    print path
    f = open(path, "a")
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
    # 如果医生id数组没有值
    if len(docIDArr) == 0:
        print '没有值'
        return 0
    for docId in docIDArr:
        attempts = 0
        print docId
        url = combolSecondUrl(baseUrl_2, docId)
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
        loadToFile(
                name,clinic_name,title,hospital,graph,graph_num,telephonePrice,telephone_num,
                   hospitalGuidePrice,hospitalGuide_num,
                   familyDoc_price,familyDoc_num,
                   videoPrice,video_num,
                   add_hsp_tag_price,add_hsp_tag_num,
                   fans_count,reply_num,thank_num)

def start(baseUrl_1, baseUrl_2, tmpIndex, name, province, clinic_no):
    reqUrl = combolFirstUrl(baseUrl_1, tmpIndex, name, province, clinic_no)
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
# https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&query=@QUERY@&filter=@FILTER@&sort_type=default&app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi
# baseUrl_1 = '''
# https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&query=@QUERY@&filter=@FILTER@&sort_type=default&app=0&platform=android&systemVer=4.1.2&version=7.5.2&app_ver=7.5.2&imei=867746015013717&device_id=867746015013717&mac=c4%3A6a%3Ab7%3A53%3A24%3A1a&secureId=96a94c7b3102faac&installId=1454148004339&phoneType=MI+1S_by_Xiaomi&vendor=anzhihd
# '''
baseUrl_2 = "https://api.chunyuyisheng.com/api/v6/doctor/clinic_web_eeb65e65132f41a5/homepage/?app=0&platform=android&systemVer=4.1.2&version=7.6.0&app_ver=7.6.0&imei=867746015013717&device_id=867746015013717&mac=c4%3A6a%3Ab7%3A53%3A24%3A1a&secureId=96a94c7b3102faac&installId=1451808746751&phoneType=MI+1S_by_Xiaomi&vendor=xiaomi"
baseUrl_1 = '''
https://api.chunyuyisheng.com/api/v4/doctor_search?page=1&query=@QUERY@&filter=@FILTER@&sort_type=default&app=0&platform=android&systemVer=4.1.2&version=7.5.2&app_ver=7.5.2&secureId=96a94c7b3102faac&phoneType=MI+1S_by_Xiaomi&vendor=anzhihd
'''

rang = range(1, 6)
# 读取代理
getTheRemoteAgent()
getTheName()
# 多线程
# for province in Province:
#     for no in Clinic_no:
# Thread = []
province = '测试'

for name in NAME:
    for pageIndex in rang:
        officeTemp = "产科"
        t1 = MyThread(start, (baseUrl_1, baseUrl_2, pageIndex, name, province, '21'))
            # Threads.append(t1)
            # 把线程分为三分
        t1.setDaemon(True)
        t1.start()
        t1.join()




