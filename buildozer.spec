[app]

# (str) Title of your application
title = Weekly Scheduler

# (str) Package name
package.name = weeklyscheduler

# (str) Package domain (needed for android/ios packaging)
package.domain = org.primetech

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,json

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
requirements = python3,kivy==2.3.0,requests,plyer,android

# (str) Custom source folders for requirements
# requirements.source =

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/logo.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/logo.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PYTHON_FILE

# (str) OSX Specific: The user you'll use to log in into your account
#osx.username = user

# (str) OSX Specific: The path to the certificate you'll use to sign the app
#osx.certificate = /path/to/cert.p12

# (str) OSX Specific: The password to the certificate
#osx.certificate_password = password

# (bool) Android specific: allow backup
android.allow_backup = True

# (str) Android specific: presplash color (new android theme)
# android.presplash_color = #FFFFFF

# (str) Android specific: the theme color (new android theme)
# android.theme_color = #FFFFFF

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to use
#android.api = 30

# (int) Minimum API required
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 21

# (str) Android NDK version to use
#android.ndk = 23b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
# android.accept_sdk_license = False

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.renpy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) List of arguments to be passed to javac. For example:
# android.add_javacargs = -Xlint:all;-Werror
#android.add_javacargs =

# (list) List of directory where to find .so libs
#android.add_libs_armeabi = libs/armeabi
#android.add_libs_armeabi_v7a = libs/armeabi-v7a
#android.add_libs_arm64_v8a = libs/arm64-v8a
#android.add_libs_x86 = libs/x86
#android.add_libs_x86_64 = libs/x86_64

# (list) List of shared libraries (.so) to add to the APK
#android.add_libs = libs/android.so

# (list) Custom Java classes to add as activities to the manifest.
#android.add_activites = com.example.ExampleActivity

# (str) python-for-android branch to use, defaults to stable
#p4a.branch = stable

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (list) Copy these files to src/main/res/xml/ (used for example with intent-filters)
#android.res_xml = PATH_TO_FILE.xml

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android.so

# (list) Android additional libraries to copy into libs/armeabi-v7a
#android.add_libs_armeabi_v7a = libs/android-v7.so

# (list) Android additional libraries to copy into libs/arm64-v8a
#android.add_libs_arm64_v8a = libs/android-v8.so

# (list) Android additional libraries to copy into libs/x86
#android.add_libs_x86 = libs/android-x86.so

# (list) Android additional libraries to copy into libs/x86_64
#android.add_libs_x86_64 = libs/android-x864.so

# (list) Android additional libraries to copy into libs/mips
#android.add_libs_mips = libs/android-mips.so

# (list) Android additional libraries to copy into libs/mips64
#android.add_libs_mips64 = libs/android-mips64.so

# (list) Android additional libraries to copy into libs/all
#android.add_libs_all = libs/android-all.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a

# (bool) Sign the release version
# android.release_artifact = .apk
# Clean build artifacts after successful build
android.clean_build_after_install = True

# Limit build cache size
android.build_cache_size = 1G