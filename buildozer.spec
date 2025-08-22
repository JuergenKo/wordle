[app]
title = Wordle Solver
package.name = wordlesolver
package.domain = org.juerg

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 1.0
requirements = python3,kivy,pillow

orientation = portrait

# Android specific
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.arch = arm64-v8a

# Permissions
android.permissions = INTERNET

# Add your words file
source.include_patterns = words_choose.txt,assets/words_choose.txt