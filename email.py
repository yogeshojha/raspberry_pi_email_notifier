#import

import RPi.GPIO as GPIO
import time
import feedparser
import string

#Edit the details

USERNAME = "kyampus.project@gmail.com"
PASSWORD = "kyampusproject"

#edit this parameter to change the speed of scrolling effect
scroll_time = 0.5


LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def main():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(LCD_E, GPIO.OUT)
  GPIO.setup(LCD_RS, GPIO.OUT)
  GPIO.setup(LCD_D4, GPIO.OUT)
  GPIO.setup(LCD_D5, GPIO.OUT)
  GPIO.setup(LCD_D6, GPIO.OUT)
  GPIO.setup(LCD_D7, GPIO.OUT)
  # Initialise display
  lcd_init()
  time.sleep(0.3)
  temp = uc = 0
  while True:
	lcd_string("    [Inbox]",LCD_LINE_1)
	lcd_string("Checking...",LCD_LINE_2)
	response = feedparser.parse("https://" + USERNAME + ":" + PASSWORD + "@mail.google.com/gmail/feed/atom")
	unread_count = int(response["feed"]["fullcount"])
	uc = str(unread_count)
	lcd_string(uc +" Unread Emails",LCD_LINE_2)
	time.sleep(3)
	lcd_string("Subject:",LCD_LINE_1)
	for count in range(0,unread_count):
		subj = str(response['items'][count].title)
		len_subj = len(subj)
		if(len_subj >= 13):
			m1 = subj[0:13]
			m2 = subj[13:len_subj]
			if(len(m2) >= 13):
				m3 = m2[14:len_subj]
			lcd_string(str(count+1) + ". " + m1,LCD_LINE_2)
			time.sleep(scroll_time)
			lcd_string(m2,LCD_LINE_2)
			if m3:
				time.sleep(scroll_time)
				lcd_string(m3,LCD_LINE_2)
				time.sleep(scroll_time)
		else:
			lcd_string(str(count+1) +". "+subj,LCD_LINE_2)
		time.sleep(2)
		m3 = None

def lcd_init():
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  GPIO.output(LCD_RS, mode)
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
  lcd_toggle_enable()
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
  lcd_toggle_enable()

def lcd_toggle_enable():
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    lcd_string("Have A Nice day", LCD_LINE_2)
    GPIO.cleanup()
