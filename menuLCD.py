#import
import RPi.GPIO as GPIO 
import time
import socket
import datetime
# Define GPIO to LCD mapping 
LCD_RS = 23
LCD_E = 27
LCD_D4 = 18 
LCD_D5 = 17
LCD_D6 = 14
LCD_D7 = 3
LED_ON = 2
#Define some device constants
LCD_WIDTH = 16 # Max char
LCD_CHR = True
LCD_CMD= False
LCD_LINE_1 = 0x80 # 1 LCD RAM address
LCD_LINE_2 = 0xC0 # 2 LCD RAM address

#Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005 
# define giá trị các nút bấm
BT1 = 21
BT2 = 26
BT3 = 20
BT4 = 19
def lcd_init():
    GPIO.setmode(GPIO.BCM) 
    GPIO.setwarnings(False)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT) 
    GPIO.setup(LCD_D7, GPIO.OUT) 
    GPIO.setup(LED_ON, GPIO.OUT) 
    #Initialise display
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD) 
    lcd_byte(0x0C, LCD_CMD) 
    lcd_byte(0x06, LCD_CMD) 
    lcd_byte(0x01, LCD_CMD) 
    
def lcd_string(message, line): 
    message = message.rjust(len(message))
    if line==1:
        lcd_byte(LCD_LINE_1,False) 
    else:
        lcd_byte(LCD_LINE_2,False) 
    for i in range(len(message)):
        lcd_byte(ord(message[i]), LCD_CHR)
        
def lcd_clear():
    lcd_string("                ",1)
    lcd_string("                ",2)
    
def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    #mode = True for character
    #       False for command
    GPIO.output(LCD_RS, mode) # RS
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False) 
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True) 
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True) 
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True) 
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True) 
    # Toggle 'Enable' pin 
    time.sleep(E_DELAY) 
    GPIO.output(LCD_E, True) 
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False) 
    time.sleep(E_DELAY)
    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False) 
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True) 
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True) 
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True) 
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True) 
    # Toggle 'Enable' pin 
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False) 
    time.sleep(E_DELAY)


def updateMenu(): 
    if (countMenu == 0):
        lcd_clear()
        lcd_string(">SHOW IP",1)
        lcd_string(" SHOW TIME",2)
    elif (countMenu == 1):
        lcd_clear()
        lcd_string(" SHOW IP",1)
        lcd_string(">SHOW TIME",2) 
    elif (countMenu == 2):
        lcd_clear()
        lcd_string(">MENU 3",1)
        lcd_string(" MENU 4",2)   
    elif (countMenu == 3): 
        lcd_clear()
        lcd_string(" MENU 3",1)
        lcd_string(">MENU 4",2)    
  

def get_ip_address():
    ip_address = ''
    s = socket.socket(socket.AF_INET, 
                      socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def selectMenu(): 
    if (countMenu == 0):
        lcd_clear()
        lcd_string("DIA CHI IP",1)
        lcd_string(get_ip_address(),2) 
        
    elif (countMenu == 1):
        lcd_clear()
        lcd_string("TIME",1)
        lcd_string(datetime.date.today().strftime("%B %d, %Y"),2)
        
    elif (countMenu == 2):
        lcd_clear()
        lcd_string("MENU 3",1)
        lcd_string("NOI DUNG MENU 3.",2)
        
    elif (countMenu == 3):
        lcd_clear()
        lcd_string("MENU 4",1)
        lcd_string("NOI DUNG MENU 4.",2)
        
  
def main():
    GPIO.setmode(GPIO.BCM) #setup mode
    # đặt các nút bấm là input, pull_up các nút bấm
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    lcd_init() 
    time.sleep(1) 
    lcd_clear()
    GPIO.output(LED_ON, True)
    time.sleep(1)
    global countMenu
    
    countMenu = 0
    updateMenu()
    while True:
        if (GPIO.input(BT1) == GPIO.LOW): 
            countMenu += 1     
            if (countMenu > 3):
                countMenu = 0                 
            updateMenu()
            time.sleep(0.25)
            print("BT1 ",countMenu)
        if (GPIO.input(BT2) == GPIO.LOW):
            countMenu -= 1
            if (countMenu < 0):
                countMenu = 3                
            updateMenu()
            time.sleep(0.25)
            print("BT2 ",countMenu)
        if (GPIO.input(BT3) == GPIO.LOW):
            selectMenu()
            time.sleep(0.25)
            print("BT3 ",countMenu)
        if (GPIO.input(BT4) == GPIO.LOW):
            updateMenu()
            time.sleep(0.25)
            print("BT4 ",countMenu)    
main()