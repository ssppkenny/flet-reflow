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
adb install build/apk/app-release.apk
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).
