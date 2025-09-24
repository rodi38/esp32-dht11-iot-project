import machine
import dht
import time
import network
import urequests
import gc


#-------------------------------------
# Configurações
THINGSPEAK_API_KEY = 'API_KEY'
THINGSPEAK_WRITE_BASE_URL = 'https://api.thingspeak.com/update' #rota get
WIFI_SSID = 'SSID DA REDE' #nome da rede do wifi
WIFI_PASSWORD = 'SENHA DA REDE'
TEMP_THRESHOLD = 31 #limite da temperatura, para o relé ligar após isso
HUMIDITY_THRESHOLD = 70 #limite da umidade, para o relé ligar após isso
SENSOR_INTERVAL = 15 #intervalo de leitura
#-------------------------------------


#-------------------------------------
#hardware
rele = machine.Pin(2, machine.Pin.OUT)
sensor_dht = dht.DHT11(machine.Pin(4))
wlan = network.WLAN(network.STA_IF)
#-------------------------------------

def conectar_wifi():
    print("Status WiFi:", wlan.status())
    wlan.active(True)
    wlan.scan()
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)


    print("Conectando à rede WiFi...")
    while not wlan.isconnected():
        print('tentando conexão')
        time.sleep(1)
        print(wlan.status())

    print("Conectado à rede WiFi!")
    print(wlan.ifconfig())



def leitura_dht():
    try:
        sensor_dht.measure()
        temperatura = sensor_dht.temperature()
        umidade = sensor_dht.humidity()
        
        return temperatura, umidade
    except Exception as e:
        print(f"Erro ao ler o sensor: {e}")
        return None, None
    
def enviar_dados_thingspeak(temperatura, umidade):  
    try:
        url = f"{THINGSPEAK_WRITE_BASE_URL}?api_key={THINGSPEAK_API_KEY}&field1={temperatura}&field2={umidade}"
        
        print(f"Enviando: Temp={temperatura}°C, Umid={umidade}%")
        response = urequests.get(url)
        
        if response.status_code == 200:
            entry_id = response.text
            print(f"Dados enviados com sucesso! Entry ID: {entry_id}")
            response.close()
            return True
        else:
            print(f"Erro HTTP: {response.status_code}")
            response.close()
            return False
            
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")
        return False


def validacao_rele(temperatura, umidade):
    if temperatura > TEMP_THRESHOLD or umidade > HUMIDITY_THRESHOLD:
        if rele.value() == 0:  # Se estava desligado
            rele.value(1)
            print(f"Relê LIGADO - Temp: {temperatura}°C, Umid: {umidade}%")
        return True
    else:
        if rele.value() == 1:  # Se estava ligado
            rele.value(0)
            print(f"Relê DESLIGADO - Temp: {temperatura}°C, Umid: {umidade}%")
        return False


def main():
    rele.value(0)
    conectar_wifi()
    
    ultima_leitura = 0
    
    while True:
        try:
            tempo_atual = time.ticks_ms()
            
            # Lê sensor apenas no intervalo definido
            if time.ticks_diff(tempo_atual, ultima_leitura) >= SENSOR_INTERVAL * 1000:
                temperatura, umidade = leitura_dht()
                
                if temperatura is not None and umidade is not None:
                    print(f"Leitura: Temp={temperatura}°C, Umid={umidade}%")
                    
                    # Controla relê
                    validacao_rele(temperatura, umidade)
                    
                    # Envia dados para ThingSpeak
                    if enviar_dados_thingspeak(temperatura, umidade):
                        ultima_leitura = tempo_atual
                    else:
                        print("Falha no envio, tentando novamente em 5s...")
                        time.sleep(5)
                else:
                    print("Falha na leitura do sensor, tentando novamente...")
            
            # Pequena pausa para não sobrecarregar
            time.sleep(1)
            
            # Limpeza de memória ocasional, anteriormente o programa dava erro por falta de memoria.
            if time.ticks_ms() % 30000 < 1000:  # A cada ~30 segundos
                gc.collect()
                
        except KeyboardInterrupt:
            print("\nSistema interrompido pelo usuário")
            rele.value(0)
            break
        except Exception as e:
            print(f"Erro no loop principal: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()



        
        
