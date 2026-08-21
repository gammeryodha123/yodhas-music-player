[app]

# (str) Title of your application
title = YODHAS Music Player

# (str) Package name
package.name = yodhasmusicplayer

# (str) Package domain (needed for android/ios packaging)
package.domain = org.yodhas

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (include all required asset extensions)
source.include_exts = py,png,jpg,kv,atlas,mp3,wav,ttf

# (list) Application requirements
# Note: Pin cython and ensure ffmpeg, openssl, and libffi are included for yt-dlp & media support
requirements = python3,kivy,yt-dlp,ffmpeg,libffi,openssl

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (str) Android NDK version to use (MUST match r25b used in build.yml)[span_0](start_span)[span_0](end_span)
android.ndk = 25b[span_1](start_span)[span_1](end_span)

# (int) Target Android API level (33 matches build.yml setup)[span_2](start_span)[span_2](end_span)
android.api = 33[span_3](start_span)[span_3](end_span)

# (int) Minimum API required (API 21 supports Android 5.0 and above)
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK directory (leave commented out so environment variables handle it)
# android.ndk_path =

# (str) Android SDK directory (leave commented out so environment variables handle it)
# android.sdk_path =

# (list) Permissions required by your music player
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, RECORD_AUDIO, FOREGROUND_SERVICE

# (list) List of service to declare
# android.services = 

# (bool) Accept SDK licenses automatically
android.accept_sdk_license = True

# (str) The Android arch to build for (arm64-v8a is modern standard; add armeabi-v7a if targeting older devices)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (bool) Copy library dependencies instead of using symlinks
android.copy_libs = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable)
warn_on_root = 1
