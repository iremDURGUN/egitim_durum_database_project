### Eğitim verilerinin tutulduğu veri tabanı için 6 tablo oluşturulmuştur. 
#### Bu tablolar arasındaki bağlantılar;
```
kisiler --> digerEgitimler (bire – çok ilişki)
bolumler --> digerEgitimler (bire – çok ilişki)
okulTipi --> digerEgitimler (bire – çok ilişki)
okullar --> digerEgitimler (bire – çok ilişki)
```
```
kisiler --> egitim (bire – bir ilişki)
bolumler --> egitim (bire – çok ilişki)
okulTipi --> egitim (bire – çok ilişki)
okullar --> egitim (bire – çok ilişki)
```

* Tablolar arasında en çok bire çoklu ilişki kullanılmıştır. Bire çoklu ilişkiyi örnek üzerinden anlatmak gerekirse kisiler tablosunda bulunan ID numarası 3 olan kişi digerEgitimler tablosunda birden çok kez bulunabilir.
ID numarası 3 olan kişinin bilgileri digerEgitimler tablosunda hiç bulunmaya da bilir, bir kez bulunabilir ya da 4 veya daha fazla da bulunabilir. Bu kişinin sonradan okuduğu eğitimlerin bilgisine bağlıdır. 
Kısacası ID bilgisinin bir tabloda bir kez diğer tabloda birden çok bulunabildiği durumlar tablolarda bire – çoklu ilişki bağlantısı görülür.

* Veri tabanındaki bağlantılar arasında bire – çoklu ilişki haricinde bir tane daha bağlantı türümüz vardır, bire – bir ilişki.
Bire – Bir ilişki’ yi örnek üzerinden anlatırsak eğer; kisiler tablosunda bulunan ID bilgisindeki kişinin eğitimler tablosunda sadece bir kez eğitim bilgisinin bulunması durumudur.
Kişi çalıştığı kuruma sadece mezun olduğu bir eğitim bilgisi ile atanabilir. Yani egitim tablosunda kişinin bir mezuniyet bilgisi bulunur ve birden fazla eğitim bilgisi girilmesine izin verilmez.
Bu da iki tablo arasında bire – bir ilişki olmasını sağlar.

* Eğer tablolar arasındaki bağlantıların diagramını incelemek isterseniz [egitimDurumDiagram](https://github.com/iremDURGUN/egitim_durum_database_project/blob/main/egitimDurumDiagram%20-%20Microsoft%20SQL%20Server%20Management%20Studio%2013.03.2024%2010_23_16.png) dosyasına giderek inceleyebilirsiniz..







