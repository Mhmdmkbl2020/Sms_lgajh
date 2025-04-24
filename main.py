import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from jnius import autoclass
from kivy.app import App
from kivy.uix.label import Label

# Android classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Environment = autoclass('android.os.Environment')
SmsManager = autoclass('android.telephony.SmsManager')

class SMSHandler(FileSystemEventHandler):
    def __init__(self):
        self.target_dir = os.path.join(
            Environment.getExternalStorageDirectory().getAbsolutePath(),
            "SMS_Files"
        )
        os.makedirs(self.target_dir, exist_ok=True)
        
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.txt'):
            self.process_sms(event.src_path)

    def process_sms(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().splitlines()
                if len(content) >= 2:
                    number = content[0].strip()
                    message = '\n'.join(content[1:]).strip()
                    if number.isdigit() and len(number) == 9:
                        SmsManager.getDefault().sendTextMessage(
                            number, None, message, None, None
                        )
                        os.remove(path)
        except Exception as e:
            print(f"Error: {str(e)}")

class SMSApp(App):
    def build(self):
        self.request_permissions()
        self.init_service()
        return Label(text='Service is running...')

    def request_permissions(self):
        activity = PythonActivity.mActivity
        permissions = [
            "android.permission.SEND_SMS",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.WRITE_EXTERNAL_STORAGE"
        ]
        for perm in permissions:
            if activity.checkSelfPermission(perm) != 0:
                activity.requestPermissions([perm], 0)

    def init_service(self):
        observer = Observer()
        handler = SMSHandler()
        observer.schedule(handler, handler.target_dir, recursive=True)
        observer.start()

if __name__ == '__main__':
    SMSApp().run()
