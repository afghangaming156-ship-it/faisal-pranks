[app]

# App name shown on the phone
title = Faisal Pranks

# Internal package name (letters/numbers only)
package.name = faisalpranks
package.domain = org.faisal

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0

# Python libraries the app needs
requirements = python3,kivy

# App icon (your Faisal logo)
icon.filename = %(source.dir)s/icon.png

# Portrait only
orientation = portrait
fullscreen = 0

# The app needs internet to talk to Resend
android.permissions = INTERNET

# Android versions
android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a

# Accept SDK licenses automatically (needed for CI builds)
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
