[app]
title = SMS Service
package.name = sms_service
package.domain = com.example
source.dir = .
version = 1.0
requirements = 
    python3==3.8.5,
    kivy==2.3.0,
    watchdog==3.0.0,
    jnius==1.4.2,
    android==0.2
android.api = 34
android.minapi = 21
android.ndk = 26.1.10909125
android.build_tools = 34.0.0
android.archs = arm64-v8a
android.permissions = 
    SEND_SMS,
    READ_EXTERNAL_STORAGE,
    WRITE_EXTERNAL_STORAGE
p4a.branch = develop
