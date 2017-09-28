# lambda-thumbnailer
My edited lambda thumbnailer. To create the zip file required by Lambda, do the following:

```
cd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -r9 ~/CreateThumbnail.zip *
zip -g ~/CreateThumbnail.zip $VIRTUAL_ENV/CreateThumbnail.py
```

