from ..common import conf, dataProc, code
import pandas as pd
import math


def FinInfoNaver(srchItem='', rptGb='연간'):
    columns = ['종류', '종목코드', '종목명', '기준년월', '매출액', '영업이익', '영업이익발표기준', '세전계속사업이익', '당기순이익', 
               '당기순이익지배', '당기순이익비지배', '자산총계', '부채총계', '자본총계', '자본총계지배', '자본총계비지배', '자본금', 
               '영업활동현금흐름', '투자활동현금흐름', '재무활동현금흐름', 'CAPEX', 'FCF', '이자발생부채','영업이익률', '순이익률',
               'ROE', 'ROA', '부채비율', '자본유보율', 'EPS', 'PER', 'BPS', 'PBR', '현금DPS', '현금배당수익률', '현금배당성향', '보통주식수']    
    data = []
    shCodeList = []

    filePathNm = conf.companyInfoPath + "/재무정보(네이버).pkl"
    acntInfo = dataProc.ReadPickleFile(filePathNm)        

    if srchItem == '':
        shCodeList = list(acntInfo[rptGb].keys())
    else:
        stockItem = code.StockItem(srchItem)
        if len(stockItem) == 1:
            shCodeList = [ stockItem.iloc[0]['종목코드'] ]

    shCodeList.sort()
    for shCode in shCodeList:
        shName = acntInfo[rptGb][shCode]['종목명']
        data += [ [ rptGb, shCode, shName] +  
                    info for info in acntInfo[rptGb][shCode]['info'] ]

    return pd.DataFrame(data, columns = columns).astype({ '매출액':'float', '영업이익':'float', '영업이익발표기준':'float', 
            '세전계속사업이익':'float', '당기순이익':'float',  '당기순이익지배':'float', '당기순이익비지배':'float', '자산총계':'float',
            '부채총계':'float', '자본총계':'float', '자본총계지배':'float', '자본총계비지배':'float', '자본금':'float', '영업활동현금흐름':'float',
            '투자활동현금흐름':'float', '재무활동현금흐름':'float', 'CAPEX':'float', 'FCF':'float', '이자발생부채':'float', '영업이익률':'float',
            '순이익률':'float', 'ROE':'float', 'ROA':'float', '부채비율':'float', '자본유보율':'float', 'EPS':'float', 'PER':'float',
            'BPS':'float', 'PBR':'float', '현금DPS':'float', '현금배당수익률':'float', '현금배당성향':'float', '보통주식수':'int64' })
# acntInfo['columns'])


def FinInfoDart(srchItem='', unit="억"):
    #acct_list = ['매출액','영업이익','당기순이익','총포괄손익']
    unit_list = {'천' : 1000, '만' : 10000, '백만' : 1000000, '천만' : 10000000, '억' : 100000000, '십억' : 1000000000, '조' : 1000000000000 }
    data = []
    shCodeList = []

    if not unit_list.get(unit):
        print('유효하지 않은 금액단위 > ', unit)
        print('선택가능한 금액단위 > ', unit_list.keys())        
        unit = "억"

    filePathNm = conf.companyInfoPath + "/재무정보(금감원).pkl"
    acntInfo = dataProc.ReadPickleFile(filePathNm)        

    if srchItem == '':
        shCodeList = list(acntInfo['data'].keys())
    else:
        stockItem = code.StockItem(srchItem)
        if len(stockItem) == 1:
            shCodeList = [ stockItem.iloc[0]['종목코드'] ]

    shCodeList.sort()
    for shCode in shCodeList:
        data += [ [ shCode, acntInfo['data'][shCode]['종목명'], acntInfo['data'][shCode]['결산월']] +  
                    info[0:4] + [  0 if type(val) == str else int(round(val / unit_list[unit], 0)) for val in info[4:] ]             
                 for info in acntInfo['data'][shCode]['info'] ]

    return pd.DataFrame(data, columns = ['종목코드','종목명','결산월'] + acntInfo['columns'])


def DividendInfo(srchItem):
    data = []
  
    x = code.StockItem(srchItem)[['종목코드','종목명']].values.tolist()
    [shCode, shName] = x[0] if len(x) == 1 else ['','']        

    filePathNm = conf.companyInfoPath + "/주식배당정보(한국거래소).pkl"
    acntInfo = dataProc.ReadPickleFile(filePathNm)        
    
    if acntInfo['data'].get(shCode) and acntInfo['data'][shCode].get('info'):
        for x in acntInfo['data'][shCode]['info']:
            data.append( [shCode, shName] + x )
    
    return pd.DataFrame(data, columns = ['종목코드','종목명']+acntInfo['columns'])


def CashFlowInfo(srchItem='', unit="억"):   
    unit_list = {'일' : 1, '천' : 1000, '만' : 10000, '백만' : 1000000, '천만' : 10000000, '억' : 100000000, '십억' : 1000000000, '조' : 1000000000000 }

    data = []
    shCodeList = []

    filePathNm = conf.companyInfoPath + "/현금흐름표(금감원).pkl"

    if not unit_list.get(unit):
        print('유효하지 않은 금액단위 > ', unit)
        print('선택가능한 금액단위 > ', unit_list.keys())        
        unit = "억"

    acntInfo = dataProc.ReadPickleFile(filePathNm)

    if srchItem == '':
        shCodeList = list(acntInfo['data'].keys())
    else:
        stockItem = code.StockItem(srchItem)
        if len(stockItem) == 1:
            shCodeList = [ stockItem.iloc[0]['종목코드'] ]

    shCodeList.sort()
    for shCode in shCodeList:
        data += [ [ shCode, acntInfo['data'][shCode]['종목명']] + info[0:4] + 
                  [ None if (math.isnan(val) or type(val) == str) else int(round(val / unit_list[unit], 0)) for val in info[4:] ]             
                  for info in acntInfo['data'][shCode]['info'] 
                ]

    return pd.DataFrame(data, columns = ['종목코드','종목명'] + acntInfo['columns'])