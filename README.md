# Flettest app

```
install pixi (https://pixi.sh/latest/#installation)
pixi install
pixi shell
```

## Build the app

### Android

```
export PIP_FIND_LINKS=echo $(readlink -f dist)
flet build apk -v
connect your device
adb install build/apk/app-release.apk
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

**Step By Step Build Process**

If you don have necessary python packages (mobile-forge recipes (whl)), then you can build everything from scratch.

1. Install pixi - curl -fsSL https://pixi.sh/install.sh | sh
2. git clone https://github.com/flet-dev/mobile-forge.git
3. git clone https://github.com/ssppkenny/python-android.git
4. Enter mobile-forge
5. Run pixi init .
6. Enter python-android
7. Run build-all.sh 3.12.9
8. Enter mobile-forge
9. Export MOBILE_FORGE_ANDROID_SUPPORT_PATH=python-android-path
10. git clone https://github.com/ssppkenny/mobile-forge-recipes.git
11. Copy recipes to mobile-forge
12. Run pixi install, pixi shell
13. In mobile-forge src/forge/cross.py add "packaging=24.0" after "install" in the method pip_install, to prevent newer version of packaging
14. Build recipes (forge android djvulib, readpdfutils, fastrlsa, flet-libpdfium)
15. git clone https://github.com/ssppkenny/flet-reflow.git
16. Enter flet-reflow
17. Run pixi install, pixi shell
18. export PIP_PDF_LINKS=echo $(readlink -f dist)
19. flet build apk

