[app]

# App info
title = FitTracker
package.name = fittracker
package.domain = org.fittracker

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json,db

version = 1.0.0

# Requirements
requirements = python3,kivy==2.3.1,kivymd==1.2.0,plyer,sqlite3

# Android
android.api = 34
android.minapi = 21
android.ndk = 26b
android.ndk_path =
android.sdk_path =
android.ant_path =
android.gradle_dependencies = androidx.core:core:1.12.0
android.gradle_api_version = 8
android.archs = arm64-v8a

# Permissions
android.permissions = CAMERA, INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACTIVITY_RECOGNITION, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# App icon (optional)
# icon = icon.png

# Orientation
orientation = portrait

# Fullscreen
fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1
