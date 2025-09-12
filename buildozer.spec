[app]

# App info
title = Wordle
package.name = wordle
package.domain = org.juergenko

# Where your main.py lives
source.dir = .

# Make sure both code and data are included
source.include_exts = py,kv,txt,json,ttf,png,jpg,jpeg,atlas
source.include_dirs = data, kv

# Exclude build clutter
source.exclude_exts = spec
source.exclude_dirs = bin, .buildozer, .git, __pycache__

# Version
version = 1.0

# Requirements
requirements = python3, kivy

# Orientation
orientation = portrait

# Run fullscreen = 0 (false)
fullscreen = 0

# Target Android API (31 = Android 12, safe modern target)
android.api = 31
android.minapi = 21
android.ndk_api = 21

# Private storage ensures files are packaged inside the APK
android.private_storage = True

# Accept licenses automatically
android.accept_sdk_license = True

# Activity/Theme
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = @android:style/Theme.NoTitleBar
android.theme = "@android:style/Theme.NoTitleBar.Fullscreen"


[buildozer]

# Logging level
log_level = 2
