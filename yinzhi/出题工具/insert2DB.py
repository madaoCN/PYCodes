#!/usr/bin/env python
#coding=utf8

import xlrd
import pymysql
import chardet
import sys
import json

FILE = '/Users/lixiaorong/Desktop/data.xlsx'
reload(sys)
sys.setdefaultencoding("utf-8")
#获取游标
conn = pymysql.Connect(host='roadshow.4i-test.com', port=43306, db='onlineclass',user='onlineclass',password='onlineclass.yinzhi' ,charset='utf8')
cur = conn.cursor()


def openExcel(file=FILE):
    '''
    获取excel表格的实例
    :param file: 文件路径
    :return: excel操作实例
    '''
    try:
        file = xlrd.open_workbook(file)
        return file
    except Exception, e:
        print e


def excel_table_byIndex(file=FILE, colIndex=0, tableIndex = 0):
    '''
    #根据索引获取Excel表格中的数据
     参数:file：Excel文件路径
     colnameindex：表头列名所在行的索引
     ，by_index：表的索引
    '''
    data = openExcel(file)
    table = data.sheets()[tableIndex]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    print nrows, ncols
    colnames = table.row_values(colIndex)  # 某一行数据
    list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
        for i in range(len(colnames)):
            colValue = colnames[i]
            rowValue = row[i]
         #判断类型
            if isinstance(colValue, float):
                colValue = unicode(int(colValue))
            if isinstance(rowValue, float):
                rowValue = unicode(int(rowValue))
            app[unicode(colValue)] = rowValue
            # app[colnames[i]] = str(row[i])
        list.append(app)
    return list

def insertOneRowToDB(oneRowData, index):
    tableName = "onlineclass_vehicle_info"

    nameDic = {u'车种车号':'f_carid',
               u'车船吨位': 'f_tonnage',
               u'发动机号码': 'f_motorid',
               u'车辆识别代码':'f_identifyid'
               }

    myKey = ""
    myValue = ""

    for key in oneRowData:
        try:
            if nameDic[key]:
                myKey = myKey + ',' + nameDic[key]
                myValue = myValue + ',' + "'" + oneRowData[key] + "\'"
        except Exception, e:
            pass

    SQL = '''INSERT INTO %s(f_id, f_create_time, f_modify_time,
    f_version_id%s) VALUES(%s, '2016-07-20 13:11:35', '2016-07-20 13:11:35',
    '0'%s)''' %(tableName,myKey,index,myValue)
    print SQL
    try:
        cur.execute(SQL)
        if not conn.commit():
            print "导入成功!"
    except Exception, e:
        print e
        print "+++++++++++导入以下数据失败 "
        print index

if __name__ == '__main__':
    tables = excel_table_byIndex(tableIndex=18)
    index = 1000
    for row in tables:
        insertOneRowToDB(row, index)
        # break
        index += 1
    cur.close()
    conn.close()

'''///表0
u'a':'f_industry', u'b':'f_department',
               u'c': 'f_assetid', u'd': 'f_year',
               u'e': 'f_month', u'f': 'f_hour',
               u'g': 'f_minute', u'h': 'f_asset_source',
               u'i': 'f_province', u'j': 'f_city',
               u'k': 'f_storage',u'l': 'f_work_shop',
               u'm': 'f_currency', u'n': 'f_clear_style',
               u'o': 'f_bill_discount_category',
               u'p': 'f_four_sqr_random_num',
               u'q': 'f_asset_level', u'r': 'f_pay_style',
               u's': 'f_reimbursed_style', u't': 'f_date',
               u'u': 'f_account_sub_type', u'v': 'f_plateid',
               u'w': 'f_account_category', u'x': 'f_audit_advice',

//表1
u'a':'f_industry', u'b':'f_company',
               u'c': 'f_address', u'd': 'f_telephone',
               u'e': 'f_account_bank', u'f': 'f_account_bank_addr', u'g':'f_account_number',
               u'h': 'f_texid', u'i': 'f_credit_code',
               u'j': 'f_economic_type', u'k': 'f_gm',
               u'l': 'f_company_prov',u'm': 'f_company_city',
               u'n': 'f_market_company_code', u'o': 'f_staff_number',
               u'p': 'f_registered_capital',u'q': 'f_paid_capital',
               u'r': 'f_operate_range', u's': 'f_found_date',
               u't': 'f_legal_person_name', u'u': 'f_company_intro',
               u'v': 'f_main_product_name',

//表2
u'a':'f_company', u'b':'f_department',
               u'c': 'f_staff_name', u'd': 'f_staff_code',
               u'e': 'f_base_salary', u'f': 'f_creditid',
               u'g':'f_issuing_authority',u'h': 'f_address',


//表3
u'a':'f_company', u'b':'f_department',
               u'c': 'f_manager',


//表7
u'原材料名称':'f_material_name', u'原材料规格型号':'f_material_model',
               u'原材料单位': 'f_material_unit', u'原材料类别': 'f_material_category',
               u'原材料材质': 'f_material_quality', u'年': 'f_year',
               u'月':'f_month',u'日': 'f_day',
               u'原材料购入单价':'f_material_purchase_price'


//表8
u'公司':'f_company', u'固定资产名称':'f_fixed_asset_name',
               u'固定资产类别': 'f_fixed_asset_category',


//表9
u'固定资产名称':'f_fixed_asset_name',
               u'固定资产单位': 'f_fixed_asset_unit',
               u'固定资产总造价': 'f_fixed_asset_build_tol_price',
               u'预计使用年限':'f_except_use_year',u'预计残值': 'f_expected_residual_value',
               u'预计清理费':'f_expect_clean_price',
               u'固定资产价格':'f_fixed_asset_price'

//表11
u'地市':'f_city',
               u'出租车发票查询电话': 'f_taxi_bill_req_tel',
               u'出租车发票监督电话': 'f_taxi_bill_control_tel',
               u'出租车起步价':'f_taxi_start_price',u'出租车计费单价': 'f_taxi_fee_unit',
               u'工业用电电费单价':'f_electric_fee_unit',
               u'车牌号':'f_license_plate_number'


//表13
u'银行':'f_bank',
               u'年': 'f_year',
               u'月': 'f_month',
               u'日':'f_day',u'利率': 'f_draft_rate',

//表14
{u'会计科目类型':'f_subject_type',
               u'会计科目借贷': 'f_subject_borrow_or_lend',
               u'一级科目': 'f_first_grade_subject',
               }

//表15
              '''