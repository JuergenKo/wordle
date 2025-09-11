[app]

# (str) Title of your application
title = Wordle

# (str) Package name
package.name = wordle

# (str) Package domain (needed for android/ios packaging)
package.domain = org.juergenko

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
# CRITICAL: This lists all file types your app uses. I've added txt, json, and kv.
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt,json,ttf

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
# Exclude the buildozer spec file itself to avoid packaging it
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
# Exclude directories that are not needed in the final app
source.exclude_dirs = bin, .buildozer, .git, __pycache__

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# Your app needs kivy. If you use any other libraries (like random, json, etc.),
# they are part of the standard library and don't need to be listed.
requirements = python3, kivy

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Supported orientation (one of landscape, sensorLandscape, portrait or all)
# orientation = portrait

# (list) Permissions
# Your app doesn't need internet, but if it did, you would uncomment the next line.
# android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
# Setting this to 31 (Android 12) is a good modern target.
android.api = 31

# (int) Minimum API your APK will support.
# This ensures your app runs on most devices. Android 5.0 (API 21) is a safe minimum.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 23b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or create reproducible builds
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# CRITICAL: Set this to True for automated builds on GitHub Actions!
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = @android:style/Theme.NoTitleBar

# (str) Android app theme, default is ok for Kivy-based app
android.theme = "@android:style/Theme.NoTitleBar.Fullscreen"

# (str) Android logcat filters (default)
#android.logcat_filters = *:S python:D

# (str) Android additional directories to package
# This is where you tell Buildozer to include your data and kv folders!
android.add_dirs = data/, kv/

# (str) Android overwrite manifest (default is False)
#android.manifest = False

# (list) Android additional manifest placeholders
#android.manifest_placeholders = {}

# (list) Android additional manifest XML elements
#android.manifest_xml = []

# (list) Android additional intent filters elements
#android.intent_filters = []

# (str) Android jar dependency, default is False
#android.add_jars = foo.jar,bar.jar

# (str) Android add source files
#android.add_src =

# (str) Android add aar dependencies
#android.add_aars =

# (str) Android add assets
#android.add_assets =

# (str) Android add libs
#android.add_libs = libs/android/*.so

# (str) Android add jni libs
#android.add_jni_libs = libs/android/*.so

# (str) Android add activities
#android.add_activities =

# (str) Android add services
#android.add_services =

# (str) Android add providers
#android.add_providers =

# (bool) Android prebuild (default is False)
#android.prebuild = False

# (bool) Android prebuild recovery (default is False)
#android.prebuild_recovery =

# (str) Android copy libraries (default is True)
#android.copy_libs = 1

#
# Python for android (p4a) specific
#

# (str) python-for-android URL to use for checkout
#p4a.url =

# (str) python-for-android fork to use in case if p4a.url is not specified, defaults to upstream (kivy)
#p4a.fork =

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) python-for-android additional arguments
#p4a.extra_args =

#
# iOS specific
#

#
# Authorize the application to be loaded by the apple store
#ios.authorize = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display the warning if the application is not in the root of the repo
# allow_repo_root_warning = 0

# (int) How long to wait for an app to launch before timing out (in seconds)
# app_timeout = 300
