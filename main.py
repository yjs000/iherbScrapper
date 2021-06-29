import requests
from bs4 import BeautifulSoup
import datetime
import csv
import time
from pathlib import Path
import operator
# from pynput.keyboard import Key, Controller

def getURLs():
  result = []
  f = open("urls.txt", "r", encoding="utf-8-sig")
  lines = f.readlines()
  f.close()
  
  # 제일 뒤 \n빼주기
  for line in lines:
    result.append(line[:-1])
  return result
  
def checkStock(url):
  #html가져오도록 request
  response = requests.get(url) 
  result = [response.status_code]

  if response.status_code == 200:
    #response
    html = response.text
    #객체로 만들어줌
    soup = BeautifulSoup(html, 'html.parser') 
    
    #날짜, 시간
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M')
    #제품명
    title = soup.find("h1", attrs={"id":"name"}).get_text()
    
    #재고확인
    button = soup.select_one("button.btn-secondary") 
    if button is None:
      button = soup.select_one("button.btn-primary > strong")
    
    button_text = button.text.strip()
    if(button_text == "입고 알림"):
      result = [date, time, title, "재고 없음"]
    elif(button_text == "장바구니에 담기"):
      result = [date, time, title, "재고 있음"]
  else:
    return result
  
  return result

def inputURLs():
  #url 입력받음
  urls = []
  while True:
    inputData = input("url을 입력해주세요(완료 x) : ")
    if inputData == "x":
      break
    else :
      urls.append(inputData)
  return urls

def readCSV(filename):
  #read csv
  f = open(filename, "r", encoding="utf-8-sig")
  reader = csv.reader(f)
  result = []
  for line in reader:
    result.append(line)
  f.close()
  print(result)
  return result

def scrap(urls, filename): 
  #read original data from CSV
  originData = readCSV(filename)
  
  # open csv to write
  f = open(filename, "w", encoding="utf-8-sig", newline="")
  writer = csv.writer(f)
  # write originData first
  for data in originData:
    writer.writerow(data)
  
  # wirte newData
  while True:
    print("scrapping...")
    for url in urls:
      data = checkStock(url)
      writer.writerow(data)
    print("sleep for 5 seconds...")
    time.sleep(5)

def initCSV(filename):
  header = ["날짜", "시간", "제품명", "재고유무"]
  f = open(filename, "w", encoding="utf-8-sig", newline="")
  writer = csv.writer(f)
  writer.writerow(header)

def main():
  # url을 가져옴
  urls = getURLs()
  print(urls)

  filename = "재고확인.csv"
  path = Path("./"+filename)
  # 파일이 있는지 없는지 확인해서
  # 파일이 있으면 그냥 이어서 scrap한 데이터 입력
  if path.exists() :
    print("file exists")
    scrap(urls, filename) # write data
  else: # 파일이 없으면 header 달아주고 scrap한 데이터 입력
    print("file not exists")
    initCSV(filename) # write header
    scrap(urls, filename) # write data

main()

# #after
# if path.exists() :
#   reader = csv.reader(open(filename))
#   print(reader)
#   sortedCSV = sorted(reader, key=operator.itemgetter(2))
# else:
#   print("error")
