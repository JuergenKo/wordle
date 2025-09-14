[app]

# App info
title = Wordle
package.name = wordle
package.domain = org.juergenko
source.dir = .
version = 1.0
requirements = python3,kivy,kivmob
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713


orientation = portrait


# (list) Java .jar files to add
android.add_jars = 



# Include source and data files
source.include_exts = py,kv,txt,json,png,jpg,jpeg,atlas,ttf
source.include_dirs = data, kv
# Explicit patterns for safety
source.include_patterns = data/*.txt, data/*.json


# Android specific

android.minapi = 21
android.ndk_api = 21

# Force modern SDK versions
android.compile_sdk = 34
android.api = 34
android.ndk = 25b   
# (safe choice, works with python-for-android)

# Google Mobile Ads (AdMob) SDK
android.gradle_dependencies = com.google.android.gms:play-services-ads:23.0.0


# (list) Gradle dependencies
# android.gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0

android.private_storage = True
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = @android:style/Theme.NoTitleBar
android.theme = "@android:style/Theme.NoTitleBar.Fullscreen"
android.build_tools_version = 36.0.3
android.accept_sdk_license = True

# Ensure data directories are packaged
android.add_dirs = data/, kv/
android.add_assets = data/

# Optional: set app icon and presplash if you have them
# icon.filename = %(source.dir)s/data/icon.png
# presplash.filename = %(source.dir)s/data/presplash.png

[buildozer]

log_level = 2
