import argparse                         # 인자값을 쉽게 옵션으로 만들 수 있는 라이브러리
import requests                         # HTTP요청을 할 수 있는 라이브러리
from bs4 import BeautifulSoup as bs     # html 코드를 Python이 이해하는 객체 구조로 변환하는 Parsing


def print_introduce():
    print("********************************************************")
    print("* Web_fuzzer_BoB 4조 (진영훈, 박찬솔, 석지원, 안평주)  *")
    print("********************************************************\n")

    print("Target :", args.url)
    print("Total requests : ", len(Payloads), "\n")
    
    print("===================================================================")
    print("ID         Response   Lines    Word     Chars       Payload")
    print("===================================================================\n")


def print_main():
    print("{0:04d}:{1:9}{2:11} L{3:7} W{4:8} Ch     {5}".format(ID,Response,Lines,Word,Chars,Payload), end='')
    
    #print("ID :", ID)                  
    #print("Response :", Response)      
    #print("Lines :", Lines)            
    #print("Word :", Word)              
    #print("Chars :", Chars)            
    #print("Payload : ", Payload[ID])   


# 입력받은 쿠키값 저장
bob_cookies = {}

# 입력받은 POST data값 저장
bob_data = {}

# Payload의 개수 세는 변수
ID=1

if __name__ == "__main__":

    # 인자값을 받을 수 있는 인스턴스 생성
    parser = argparse.ArgumentParser(description='사용법')

    # 입력받을 인자값 등록
    parser.add_argument('-seed', required=True, help='퍼징할 시드파일 경로')     # True  : 필수 입력 O
    parser.add_argument('-cookie1', required=False, help='쿠키값1')             # False : 필수 입력 X
    parser.add_argument('-cookie2', required=False, help='쿠키값2')             
    parser.add_argument('-post', required=False, help='POST방식으로 넘길 값')             
    parser.add_argument('-url', required=True, help='퍼징할 대상 주소 URL')

    # 입력받은 인자값을 args에 저장 (type: namespace)
    args = parser.parse_args()

    # 입력받은 인자값 출력
    #print(args.seed)
    #print(args.cookie1)
    #print(args.cookie2)
    #print(args.post)
    #print(args.url)


    # 입력받은 쿠키값 파싱하여 저장    
    if str(args.cookie1) != "None":                         # 쿠키값이 비어있지 않을 경우(입력 받았을 경우)
        div = str(args.cookie1).split("=",maxsplit=1)       # "="을 기준으로 쿠키를 쪼갬
        bob_cookies[div[0]] = div[1]                        # 쪼갠 쿠키를 dictionary형태로 저장
    
    if str(args.cookie2) != "None":
        div = str(args.cookie2).split("=",maxsplit=1)       
        bob_cookies[div[0]] = div[1]                           

    # 입력받은 POST data값 파싱하여 저장
    if str(args.post) != "None":                            # post data가 비어있지 않을 경우(입력 받았을 경우)
        div1 = str(args.post).split("&")                    # "&"을 기준으로 post를 쪼갬
        for i in range(len(div1)):                          # 입력받은 data만큼 반복
            div2 = str(div1[i]).split("=")                  # "="을 기준으로 data를 쪼갬
            bob_data[div2[0]] = div2[1]                     # 쪼갠 data를 dictionary형태로 저장
            if str(div2[1]) == "BOB" : key_BOB = div2[0]       # 만약 value가 BOB라면 key를 저장

    # 인자값으로 입력받은 시드파일에 있는 모든 시드 읽어오기
    f = open(args.seed, 'r')                        
    Payloads = f.readlines()                         

    # 소개 출력
    print_introduce()

    # Session 생성, with 구문 안에서 유지
    with requests.Session() as s:
        
        for Payload in Payloads:                            # 한줄씩 출력하여 시드파일이 끝날 때 까지 반복     

            # post 방식
            if str(args.post) != "None":                    # post data가 비어있지 않을 경우(입력 받았을 경우)
                if str(args.post).find("BOB") == -1 :        # BOB문자가 안들어 있다면 프로그램 종료 
                    print("I don't search BOB")
                    quit()   
                
                bob_data[key_BOB] = Payload.replace("\n", "")   # value가 BOB인 key를 찾아서 Payload로 치환
                bob_url = args.url


            # get 방식
            else :               
                if str(args.url).find("BOB") == -1 :        # BOB문자가 안들어 있다면 프로그램 종료 
                    print("I don't search BOB")
                    quit()  

                bob_url = args.url.replace("BOB", Payload, 1)   # BOB문자 injection으로 치환, \n 까지 같이 저장됨
                bob_url = bob_url.replace("\n", "")                 # \n 문자 빼주기 


            # post, get 공용
            req = s.post(bob_url,data=bob_data, cookies=bob_cookies, allow_redirects=False)    # 전송, allow_redirects 설정 안하면 Response 200,404 만 뜸, get도 post로 넘겨도 상관없는듯
            html = req.text                                 # HTML 소스 가져오기
                
            # 출력할 것들 파싱해주기
            Response = req.status_code                      # HTTP Status 가져오기 (200: 정상)
            Lines = len(html.split("\n"))-1
            Word = len(html.split())
            Chars = len(html)
            
            print_main()                                
        
            ID+=1

        f.close()