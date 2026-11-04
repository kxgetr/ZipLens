# ZipLens

ZIP dosyalarındaki içerik farklarını ve değişen görsellerin yan yana önizlemelerini üretir.

## Kullanım

Python 3.11 veya üzeri.

```sh
python -m pip install -r requirements.txt
python ziplens.py old.zip new.zip --previews images
```

JSON raporu stdout üzerinden gelir. PNG önizleme için Pillow gerekir. ZIP girdileri diske çıkarılmaz.

## Doğrulama

```sh
python verify.py
```

MIT lisansı.
