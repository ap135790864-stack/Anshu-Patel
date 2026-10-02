[app]
title = JARVIS
package.name = jarvis
package.domain = com.indore.jarvis
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.0,pyjnius,requests,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,RECORD_AUDIO
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreements = True

[buildozer]
log_level = 2
