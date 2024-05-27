[app]
# (str) Title of your application
title = My KivyMD App

# (str) Package name
package.name = mykivymdapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let's include all source files)
source.include_exts = py,png,jpg,kv,atlas,env,txt,json,ttf
source.include_patterns = assets/*,libs/*,kv/*

# (str) Application versioning (must be set)
version = 0.1

# (str) Application requirements
requirements = python3,firebase-admin==6.5.0,google-cloud-firestore==2.15.0,python-dotenv==1.0.1,openai==1.14.3,Kivy==2.0.0,kivy-deps.angle==0.3.3,kivy-deps.glew==0.3.1,kivy-deps.sdl2==0.3.1,Kivy-Garden==0.1.5,kivymd==0.104.2,asynckivy==0.6.2

# (str) Entry point of your application
entrypoint = app_mobile.py

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE
