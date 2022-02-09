import requests
import json
import datetime

from sys import argv
uid = argv

def rError(jsonR):

    if ('error' in jsonR):
        print('Ошибка: ' +str(jsonR['error']['error_code']) +' ' +jsonR['error']['error_msg']) 
        return False
    else:
        return True    


def rAgeOld(fage):

    arr = fage.split('.')

    if len(arr) == 3:
    
        day =int(arr[0])
        moutch =int(arr[1])
        year =int(arr[2])

        now = datetime.datetime.now() 
        then = datetime.datetime(year, moutch, day)
    
        # Кол-во времени между датами.
        delta = now - then

        avgyear = 365.2425        
        years = divmod(delta.days, avgyear)
        years = int(years[0])
        return years
    
    return None

def ConvertUid(uid):
    _params ={'access_token': 'access_token',
              'user_ids': uid,
              'fields'  : 'bdate',
               'v'      : '5.71' }
  
    r = requests.get('https://api.vk.com/method/users.get', params=_params)    
    jsonR =r.json()
    
    if rError(jsonR) ==True:
       print('Проверяем пользователя ' + jsonR['response'][0]['first_name'] +' ' +jsonR['response'][0]['last_name'] +' ' +str(jsonR['response'][0]['id']))    #id":52800053,"first_name":"Максим","last_name":"Тишин",
       return jsonR['response'][0]['id'] 
    else:
        return None   

    #try:
    #    print('Проверяем пользователя ' + jsonR['response'][0]['first_name'] +' ' +jsonR['response'][0]['last_name'] +' ' +str(jsonR['response'][0]['id']))    #id":52800053,"first_name":"Максим","last_name":"Тишин",
    #    return jsonR['response'][0]['id']
    #except:
    #    return None

def rAllFriends(uid):

    _params ={'access_token': 'access_token',
              'user_id': uid,
              'fields'  : 'bdate,sex',
               'v'      : '5.71' }
  
    r = requests.get('https://api.vk.com/method/friends.get', params=_params)
    jsonR =r.json()

    if rError(jsonR) ==True:
        return r 
    else:
        return None       
    

if __name__ == '__main__':

    Next =True

    #проверю переданный уид(может быть передан с id, или как denis_l)
    uid = ConvertUid(uid)

    if uid is None:
        print('Неверный id пользователя!')
        Next =False
    
    if Next:        
        friends =rAllFriends(uid)

        if friends is not None:

            jfriends =friends.json()
            
            print('У него ' +str(jfriends['response']['count']) +' друзей')

            if jfriends['response']['count'] >0:                
                for f in jfriends['response']['items']:                             
                    if ('bdate' in f):
                        
                        fage =f['bdate']
                        fOld =rAgeOld(fage)

                        if fOld !=None:
                            #определю пол пользователя
                            if f['sex'] ==1:
                                Sex =' Ей '
                            elif f['sex'] ==2:
                                Sex =' Ему '
                            else:
                                Sex =' (пол не указан) '       

                            sMessage =' ' +str(fage) +'.' +Sex +str(fOld) +' лет.'
                        else:
                            sMessage =' дата рождения установлена не корректна, невозможно рассчитать возраст!'      

                        print('Дата рождения пользователя ' +f['first_name'] +' ' +f['last_name'] +' с id ' +str(f['id']) +sMessage )   
                    else:
                        print('У пользователя ' +f['first_name'] +' ' +f['last_name'] +' с id ' +str(f['id']) +' дата рождения не установлена!')
   
