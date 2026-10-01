[app]

title = Faisal Pranks

package.name = faisalpranks
package.domain = org.faisal

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0

requirements = python3,kivy

icon.filename = %(source.dir)s/icon.png

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 34
android.minapi = 24

# Single arch only — fast and stable (covers all modern phones)
android.archs = arm64-v8a

android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
