[app]

# (str) Title of your application
title = YODHAS Music Player

# (str) Package name
package.name = yodhasmusic

# (str) Package domain
package.domain = org.yodhas.musicplayer

# (str) Source code where main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 0.1

# (list) Application requirements (Fixed dependencies for yt-dlp/HTTPS)
requirequirements = python3,kivy,cython,yt_dlp,urllib3,certifi,openssl,requests


# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 0

# (list) Permissions required for network streaming & saving files
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (list) Architectures to build
android.archs = arm64-v8a, armeabi-v7a

# (bool) Auto backup
android.allow_backup = True

[buildozer]

# (int) Log level
log_level = 2

# (int) Warning on root execution
warn_on_root = 1
