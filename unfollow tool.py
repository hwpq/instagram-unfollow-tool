try:
    import requests,uuid,os,ctypes,uuid,time,threading
except Exception as ex:
    print(ex)
    input()
    exit(0)


id = None
req = requests.session()

class Login():
    def __init__(self):
        self.username = input("Username : ")
        self.password = input("Password : ")
        self.login()

    def login(self):
        global id
        head = {"User-Agent":"Instagram 152.0.0.1.60 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
        
        data = "signed_body=SIGNATURE.{\"jazoest\":\"22283\",\"country_codes\":\"[{\\\"country_code\\\":\\\"1\\\",\\\"source\\\":[\\\"default\\\"]},{\\\"country_code\\\":\\\"966\\\",\\\"source\\\":[\\\"sim\\\"]}]\",\"phone_id\":\"" + str(uuid.uuid4()) + "\",\"enc_password\":\"#PWD_INSTAGRAM:0:0:" + self.password + "\",\"username\":\"" + self.username + "\",\"adid\":\"" + str(uuid.uuid4()) + "\",\"guid\":\"" + str(uuid.uuid4()) + "\",\"device_id\":\"" + str(uuid.uuid4()) + "\",\"google_tokens\":\"[]\",\"login_attempt_count\":\"3\"}"
        
        res = req.post("https://i.instagram.com/api/v1/accounts/login/",data=data,headers=head)
        if "logged_in_user" in res.text:
            id = res.json()['logged_in_user']['pk']
            print("sucssfully login")
            #input("sessionid : "+ res.cookies['sessionid'])
            Del_following()
        elif "bad_password" in res.text:
            input("bad password")
            exit(0)

        elif "challenge_required" in res.text:
            api_path = res.json()['challenge']['api_path']
            self.api_challenge(api_path)
        else:
            input(res.text)
            exit(0)
    
    def api_challenge(self,api_path):
        try:
            head = {"User-Agent":"Instagram 152.0.0.1.60 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
                
            res = req.get("https://i.instagram.com/api/v1"+api_path,headers=head)
            if "phone_number" in res.text:
                print("0 - "+res.json()['step_data']['phone_number'])
            if 'email' in res.text:
                print("1 - "+res.json()['step_data']['email'])
            if res.text.__contains__("phone_number") and res.text.__contains__("email") == False:
                input("unknown verification method !!")
                exit(0)
            self.api_send_choice(api_path)
        except Exception as ex:pass
    
    def api_send_choice(self,path):
        try:
            head = {"User-Agent":"Instagram 152.0.0.1.60 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
            
            choice = input("Choice : ")
            data = "choice="+choice    
            res = req.post("https://i.instagram.com/api/v1"+path,data=data,headers=head)
            if (res.text.__contains__("contact_point")) or (res.text.__contains__("\"resend_delay\":60")):
                print("code Sent To "+res.json()['step_data']['contact_point'])
                self.api_send_code(path)
            else:
                input(res.text)
                exit(0)
        except:pass
    
    def api_send_code(self,path):
        try:
            global id
            head = {"User-Agent":"Instagram 152.0.0.1.60 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
            
            code = input("code : ")
            data = "security_code="+code
            res = req.post("https://i.instagram.com/api/v1"+path,data=data,headers=head)
            if "logged_in_user" in res.text:
                id = res.json()['logged_in_user']['pk']
                print("sucssfully login")
                #input("sessionid : "+ res.cookies['sessionid'])
                Del_following()
            else:
                input(res.text)
                exit(0)
        except:pass


class Del_following():
    def __init__(self):
        self.done = 0
        self.bad = 0
        self.ran = True
        self.slp = input("sleep : ")
        threading.Thread(target=self.work).start()
        self.grabe_id()
    
    def grabe_id(self):
        try:
            url = "https://i.instagram.com/api/v1/friendships/"+str(id)+"/following/?includes_hashtags=true&search_surface=follow_list_page&query=&enable_groups=true&rank_token=883e139a-e642-4257-b04f-4342afc642b4"
            head = {
                "User-Agent":"Instagram 152.0.0.1.60 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
            res = req.get(url,headers=head)
            if res.text.__contains__("users\":[]") != True:
                self.del_following(res.json()['users'][0]['pk'])   
            elif res.text.__contains__('"users":[],'):
                self.ran = False
                input("\nMission completed successfully :)")
                exit(0)
            else:
                self.ran = False
                input(res.text)
                exit(0)  
        except:pass

    def del_following(self,idd):
        try:
            head = {
                "User-Agent":"Instagram 152.0.0.1.60 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            }       
            data = {"user_id":idd,"radio_type":"wifi-none","_uid":str(uuid.uuid4()),"_uuid":"284dda16-e663-4ab4-8d31-74b200482df5","nav_chain":"9cb:self_profile:2,ProfileMediaTabFragment:self_profile:3,Ac4:self_following:4,Ac4:self_following:7,Ac4:self_following:8","container_module":"self_following"}
            res = req.request('POST',f"https://i.instagram.com/api/v1/friendships/destroy/{idd}/",data=data,headers=head).status_code
            if res == 200:
                self.done +=1
                time.sleep(int(self.slp))   
                self.grabe_id()
            else:
                self.bad +=1
        except:pass
    
    def work(self):
        while self.ran:
            print("unfollow : {} / Errors : {}".format(self.done,self.bad),end='\r',flush=True)




def main():
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW("unfollow tool By RiOS")
        os.system("mode con:cols=74 lines=17")

    Login()

if __name__ == "__main__":
    main()