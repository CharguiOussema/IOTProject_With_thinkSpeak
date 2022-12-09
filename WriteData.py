#**************************************
# importation du bibliothèque
import machine
import network 
import urequests 
import dht 
import time

# **************************************
led = machine.Pin(2,machine.Pin.OUT) 
d = dht.DHT11(machine.Pin(0)) 

# **************************************
# Configuration ESP32 wifi 
sta = network.WLAN(network.STA_IF)
if not sta.isconnected(): 
  print('connecting to network...') 
  sta.active(True) 
  sta.connect("dlink","1234Data") 
  while not sta.isconnected(): 
    pass 
print('network config:', sta.ifconfig()) 

# ************************************************************
# déclaration des variables:
HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = 'GPU45WTIM4LRWYDM' 
UPDATE_TIME_INTERVAL = 1000  # in ms 
last_update = time.ticks_ms() 

#***************************************************
while True: 
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL: 
        d.measure() 
        t = d.temperature() 
        h = d.humidity() 
         
        dht_readings = {'field1':t, 'field2':h} 
        request = urequests.post( 
          'http://api.thingspeak.com/update?api_key=' +
          THINGSPEAK_WRITE_API_KEY, 
          json = dht_readings, 
          headers = HTTP_HEADERS )  
        request.close()  
        print("Temperateur ="+str(t)+"C°"+" Humidity ="+str(h)+"%")
        led.value(not led.value()) 
        last_update = time.ticks_ms()
