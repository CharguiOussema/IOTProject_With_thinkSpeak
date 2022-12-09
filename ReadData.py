# Importation des packages
import urequests
import time
import network
import machine
import json

# Déclaration des ports 
ledRouge = machine.Pin(22,machine.Pin.OUT)
ledJaune = machine.Pin(15,machine.Pin.OUT)
buzzer = machine.Pin(14, machine.Pin.OUT)
sta = network.WLAN(network.STA_IF)

#  Connexion réseau internet
if not sta.isconnected(): 
  print('connecting to network...') 
  sta.active(True) 
  sta.connect("dlink","1234Data") 
  while not sta.isconnected(): 
    pass 
print('network config:', sta.ifconfig())
UPDATE_TIME_INTERVAL = 1000  
last_update = time.ticks_ms() 


while True:
    
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        # Lire les données via API RESTFULL 
        request = urequests.get("https://api.thingspeak.com/channels/1968611/feeds.json?results=2") 
        res = json.loads(request.text)
        Temperateur = res['feeds'][0]['field1']
        print(Temperateur)
        request.close()
        if(int(Temperateur) > 20 ):
            buzzer.value(1) 
            time.sleep(2) 
            ledRouge.value(1)
            ledJaune.value(0)
        else:
            ledRouge.value(0)
            ledJaune.value(1)
            buzzer.value(0) 
            time.sleep(2) 
            
        last_update = time.ticks_ms()
        
        
#**********************************************

Temperateur = res['feeds'][0]['field1']
print(Temperateur)