# lambda-thumbnailer
My edited lambda thumbnailer. To create the zip file required by Lambda, do the following:

```
$ source lambda-thumbnailer/bin/activate
$ zip -r9 ~/CreateThumbnail.zip *
$ zip -g CreateThumbnail.zip CreateThumbnail.zip
```

