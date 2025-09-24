#  Monitoramento de Temperatura e Umidade com ESP8266 + ThingSpeak

Este projeto utiliza MicroPython no ESP32 para monitorar temperatura e umidade com o sensor DHT11, enviando os dados para a nuvem via ThingSpeak.

Também é possivel controlar o relé para acionar dispositivos quando a temperatura ou umidade ultrapassarem limites pré-definidos, atualmente está apenas ligando e desligando o relé caso atenda certas condições.

# Funcionalidades

Conexão automática à rede Wi-Fi.

Leitura periódica de temperatura e umidade com sensor DHT11.

Envio de dados para a plataforma ThingSpeak.

Acionamento automático de relé baseado em limites configuráveis.

Coleta de lixo (gc.collect()) para evitar problemas de memória.

# Hardware Necessário

ESP32

Sensor DHT11

Módulo Relé 5V

Jumpers fêmeas

Acesso Wi-Fi

# Estrutura do Projeto
```
├── main.py       # Código principal em MicroPython
├── README.md     # Documentação do projeto
```
# Instalação e Configuração

Instale o Thonny IDE para gravar o código no ESP32.

Instale o MicroPython firmware no microcontrolador.

Clone ou copie este repositório.

Configure as credenciais de Wi-Fi e API Key do ThingSpeak no código:
```
THINGSPEAK_API_KEY = 'SUA_API_KEY'
WIFI_SSID = 'NOME_DA_REDE'
WIFI_PASSWORD = 'SENHA_DA_REDE'
```

Ajuste os limites, se necessário:

```
TEMP_THRESHOLD = 31   # Temperatura limite em °C
HUMIDITY_THRESHOLD = 70   # Umidade limite em %
SENSOR_INTERVAL = 15  # Intervalo entre leituras (segundos)
```


# ThingSpeak

ThingSpeak é usado no projeto como nossa conexão com a nuvem, é o que torna o projeto IOT.

Crie uma conta no site do ThingSpeak

Crie um novo Channel e habilite dois campos:

Field1 → Temperatura

Field2 → Umidade

Copie a Write API Key e cole no código.

Pronto! Os dados começarão a aparecer no painel.

# Lógica do Relé

Relé liga se:
```
temperatura > TEMP_THRESHOLD
```
ou
```
umidade > HUMIDITY_THRESHOLD
```
O Relé desliga quando os valores ficam abaixo dos limites.

<hr>



# Exemplo de Saída no Terminal<br>
```python
Conectando à rede WiFi...
Conectado à rede WiFi!
('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')
Leitura: Temp=29°C, Umid=65%
Relê DESLIGADO - Temp: 29°C, Umid: 65%
Enviando: Temp=29°C, Umid=65%
Dados enviados com sucesso! Entry ID: 12345
```
