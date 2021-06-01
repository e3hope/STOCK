from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Stock

import sys
from PyQt5.QtWidgets import *
import win32com.client
import pythoncom
import pandas as pd
import os
import json

# 메인
def main(request):
    return HttpResponse('main')

#국내차트 데이터 전송
def domestic(request):
    if request.method == 'GET':
        pythoncom.CoInitialize()
        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            exit()
        else : print("Plus 연결 성공")
  
        # 일자별 object 구하기
        objDomeindex = win32com.client.Dispatch("DsCbo1.StockWeek")
        code = {'KOSPI':'U001','KOSDAQ':'U201'}
        data = {'KOSPI':[],'KOSDAQ':[]}
        for k,v in code.items() :
            objDomeindex.SetInputValue(0,v) # 나스닥
            objDomeindex.SetInputValue(1,ord("D")) # 일자별
            objDomeindex.SetInputValue(3,9999) # 일자별
            objDomeindex.BlockRequest()
            for i in range(0,6) :
                temp = {}
                temp['date'] = objDomeindex.GetDataValue(0,i)
                temp['index'] = objDomeindex.GetDataValue(1,i)
                data[k].append(temp)
        pythoncom.CoUninitialize()
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, status=200)
        # data = {KOSPI:[{date:20210531,index:3232},{date:20210531,index:3232}],KOSDAQ:[{date:20210531,index:3232},{date:20210531,index:3232}]}

# 해외차트 데이터 전송
def foreign(request):
    if request.method == 'GET':
        pythoncom.CoInitialize()
        objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')

        bConnect = objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            exit()
        else : print("Plus 연결 성공")
        
        objForeindex = win32com.client.Dispatch('Dscbo1.CpSvr8300')
        # code = {'DOW':'.DJI','NASDAQ':'COMP'}
        # data = {'DOW':{},'NASDAQ':{}}
        code = {'DOW':'.DJI','NASDAQ':'COMP','SP500':'SPX','SH':'SHANG'}
        data = {'DOW':[],'NASDAQ':[],'SP500':[],'SH':[]}
        for k,v in code.items() :
            objForeindex.SetInputValue(0,v) # 나스닥
            objForeindex.SetInputValue(1,ord("D")) # 일자별
            objForeindex.SetInputValue(3,9999) # 일자별
            objForeindex.BlockRequest()
            for i in range(0,6) :
                temp = {}
                temp['date'] = objForeindex.GetDataValue(0,i)
                temp['index'] = objForeindex.GetDataValue(1,i)
                data[k].append(temp)
        pythoncom.CoUninitialize()
        return JsonResponse(data,json_dumps_params={'ensure_ascii': False}, status=200)
        # data = {DOW:[{date:20210531,index:3232},{date:20210531,index:3232}],NASDAQ:[{date:20210531,index:3232},{date:20210531,index:3232}],
        #         SP500:[{date:20210531,index:3232},{date:20210531,index:3232}],SH:[{date:20210531,index:3232},{date:20210531,index:3232}]}


# 종목 정보 전송
def getstock(request, stock_code):
    if request.method == 'GET':
        # stock_code = request.GET['stock_code']
        pythoncom.CoInitialize()
        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            exit()
        
        # 현재가 객체 구하기
        objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
        objStockMst.SetInputValue(0,'A'+stock_code)   #종목 코드 - 삼성전자
        objStockMst.BlockRequest()
        
        # 현재가 통신 및 통신 에러 처리 
        rqStatus = objStockMst.GetDibStatus()
        rqRet = objStockMst.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            exit()

        # 현재가 정보 조회
        data = {
            'code':objStockMst.GetHeaderValue(0),  #종목코드
            'name':objStockMst.GetHeaderValue(1),  # 종목명
            'time':objStockMst.GetHeaderValue(4),  # 시간
            'closing':objStockMst.GetHeaderValue(11), # 종가
            #'beforeafter':objStockMst.GetHeaderValue(12),  # 대비
            'opening':objStockMst.GetHeaderValue(13),  # 시가
            'high':objStockMst.GetHeaderValue(14),  # 고가
            'low':objStockMst.GetHeaderValue(15),  # 저가
            'calling':objStockMst.GetHeaderValue(16),  #매도호가
            'offer':objStockMst.GetHeaderValue(17),   #매수호가
            'trading_volume':objStockMst.GetHeaderValue(18),   #거래량
            'transaction_amount':objStockMst.GetHeaderValue(19)  #거래대금
        }
        pythoncom.CoUninitialize()
        return JsonResponse(data,json_dumps_params={'ensure_ascii': False}, status=200)
        # data = {code:23,name:넷,time:~,closing:종가,beforeafter:대비,opening:시가 ,high:고가,low:저가,
        #         calling:매도호가,offer:매수호가,trading volume:거래량,transaction_amount:거래대금}

        
        # 예상 체결관련 정보
        # exFlag = objStockMst.GetHeaderValue(58) #예상체결가 구분 플래그
        # exPrice = objStockMst.GetHeaderValue(55) #예상체결가
        # exDiff = objStockMst.GetHeaderValue(56) #예상체결가 전일대비
        # exVol = objStockMst.GetHeaderValue(57) #예상체결수량
        # if (exFlag == ord('0')):
        #     print("장 구분값: 동시호가와 장중 이외의 시간")
        # elif (exFlag == ord('1')) :
        #     print("장 구분값: 동시호가 시간")
        # elif (exFlag == ord('2')):
        #     print("장 구분값: 장중 또는 장종료")
        
        # print("예상체결가 대비 수량")
        # print("예상체결가", exPrice)
        # print("예상체결가 대비", exDiff)
        # print("예상체결수량", exVol)

# 종목 정보 전송
def searchstock(request,stock_name):
    if request.method == 'GET':
        queryset = Stock.objects.filter(name__contains=stock_name)
        serialize = serializers.serialize('json', queryset)
        data = []
        
        # 데이터 가공
        for s in json.loads(serialize):
            temp = {}
            for k,v in s.items() :
                if k == 'pk' :
                    temp['code'] = v
                elif k == "fields" :
                    temp.update(v)
            data.append(temp)
        return JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii': False},status=200)
        # data = [{code:23,name:넷},{code:344,name:넷떡상}]