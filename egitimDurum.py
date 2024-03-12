import pypyodbc

# egitimDurum DATABASE'ne bağlanılır.
database = pypyodbc.connect(
    "DRIVER={SQL Server};"
    "Server=DESKTOPNAME;"   # Bilgisayarınızın server adını yazmanız gerekmektedir.
    "Database=egitimDurum;"  # Oluşturduğunuz Database ismini girmeniz gerekmektedir.
    "Trusted_Connection=True;"
)
cursor = database.cursor()


# Tabloları olusturduğumuz sorguları yazarız
def tabloOlustur():
    # Kişilerin tutulacağı bir tablo oluştur
    cursor.execute('Create Table kisiler (ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),'
                   ' AdSoyad VARCHAR(35) NOT NULL)')

    # Okul bilgilerinin tutulacağı tablo oluşturulur.
    cursor.execute("Create Table okullar (ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   " okulAdi VARCHAR(50) UNIQUE)")

    # Bölümlerin olacağı tabloyu oluştur
    cursor.execute("Create Table bolumler (ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   " bolumAdi VARCHAR(35) UNIQUE)")

    # okul tiplerini tutmak için tablo oluştur
    cursor.execute("Create Table okulTipi (ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   " okulTipi VARCHAR(20) UNIQUE)")

    # Asli eğitim bilgileri için tablo olustur.
    cursor.execute("Create Table egitim ( ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   "kisiID INT UNIQUE,"
                   "okulID INT,"
                   "bolumID INT,"
                   "tipID INT,"
                   "FOREIGN KEY (kisiID) REFERENCES kisiler (ID), "
                   "FOREIGN KEY (okulID) REFERENCES okullar (ID), "
                   "FOREIGN KEY (bolumID) REFERENCES bolumler (ID),"
                   "FOREIGN KEY (tipID) REFERENCES okulTipi (ID) )")

    # Diğer tüm eğitim bilgileri için tablo oluştur
    cursor.execute("Create Table digerEgitimler ( ID INT NOT NULL PRIMARY KEY IDENTITY(1,1),"
                   "kisiID INT ,"
                   "okulID INT,"
                   "bolumID INT,"
                   "tipID INT,"
                   "FOREIGN KEY (kisiID) REFERENCES kisiler (ID), "
                   "FOREIGN KEY (okulID) REFERENCES okullar (ID), "
                   "FOREIGN KEY (bolumID) REFERENCES bolumler (ID),"
                   "FOREIGN KEY (tipID) REFERENCES okulTipi (ID) )")

    # egitim ve digerEgitimler tablolarında olan tek fark sicilID' nin egitim tablosunda UNİQUE olmasıdır.
    # Bunun sebebi egitim tablosunda kişinin çalıştığı kurumda ki unvanının verisini tutmaktadır.
    # digerEgitimler tablosunda ise kişilerin eğer okuduysa, okuduğu diğer okul verileri tutulmaktadır.
    # Veritabanı işlemlerini kaydet
    cursor.commit()


# Tablolara veri ekleme işlemlerini yapmak için sorguları fonksiyonlar yardımıyla oluştururuz

# Kişiler tablosuna veri girişi için
def kisilerEkle(x):
    cursor.execute("INSERT INTO kisiler (AdSoyad) VALUES ('" + x + "')")
    cursor.commit()


# okullar tablosuna veri girişi için
def okulEkle(x):
    cursor.execute("INSERT INTO okullar (okulAdi) VALUES ('" + x + "')")
    cursor.commit()


# bolumler tablosuna veri girişi için
def bolumEkle(x):
    cursor.execute("INSERT INTO bolumler (bolumAdi) VALUES ('" + x + "')")
    cursor.commit()


# okulTipi tablosuna veri girişi için
def okulTipiEkle(x):
    cursor.execute("INSERT INTO okulTipi (okulTipi) VALUES ('" + x + "')")
    cursor.commit()


# x = hangi kolona, y = hangi ID' yi ,z = hangi sicildeki kişiye veri eklemek istediğimizin verisini tutar.
# okulID, bolumID, tipID kolonlarının verilerini girerken UPDATE methodunu kullanıyoruz
# çünkü veri girişi sağlamak istediğimiz bir sicilID' de kişi vardır. Bu sebeple WHERE ile sicilID' yi belirtmeliyiz.
# egitim tablosuna veri girişi için
def egitimEkle(x, y, z):
    if x == "kisiID":
        cursor.execute("INSERT INTO egitim (kisiID) VALUES ('" + y + "')")
    elif x == "okulID":
        cursor.execute("UPDATE egitim SET okulID = '" + y + "' WHERE kisiID = '" + z + "' ")
    elif x == "bolumID":
        cursor.execute("UPDATE egitim SET bolumID = '" + y + "' WHERE kisiID = '" + z + "' ")
    elif x == "tipID":
        cursor.execute("UPDATE egitim SET tipID = '" + y + "' WHERE kisiID = '" + z + "' ")
    cursor.commit()


# okulID, bolumID, tipID kolonlarının verilerini girerken WHERE methoduyla bir koşul daha belirtmek zorunda kalırız
# çünkü tabloda aynı sicilI' de birden çok satır olabilir.
# Bu nedenle tablodaki en büyük ID' yi seçeriz ki en son eklenen satır üstünde veri girişi yapabilelim.
# digerEgitimler tablosuna veri girişi için
def digerEgitimEkle(x, y, z):
    if x == "kisiID":
        cursor.execute("INSERT INTO digerEgitimler (kisiID) VALUES ('" + y + "')")
    elif x == "okulID":
        cursor.execute("UPDATE digerEgitimler SET okulID = '" + y + "' "
                                                                    "WHERE kisiID = '" + z + "' AND "
                                                                                             "ID = (SELECT MAX(ID) "
                                                                                             "FROM digerEgitimler) ")
    elif x == "bolumID":
        cursor.execute("UPDATE digerEgitimler SET bolumID = '" + y + "' "
                                                                     "WHERE kisiID = '" + z + "' AND "
                                                                                              "ID = (SELECT MAX(ID) "
                                                                                              "FROM digerEgitimler) ")
    elif x == "tipID":
        cursor.execute("UPDATE digerEgitimler SET tipID = '" + y + "' "
                                                                   "WHERE kisiID = '" + z + "' AND "
                                                                                            "ID = (SELECT MAX(ID) "
                                                                                            "FROM digerEgitimler) ")
    cursor.commit()


# digerEgitimEkle("okulID", "4", "8")
# tüm tablo bilgilerini almak için kullanırız
a = cursor.execute("SELECT * FROM digerEgitimler ORDER BY ID")

# Birden fazla üniversite okuyan kişilerin isimlerini döndürür.
b = cursor.execute("SELECT DISTINCT(k.AdSoyad) FROM digerEgitimler AS d INNER JOIN kisiler AS k ON d.kisiID = k.ID")

# diger egitim tablosunda bir' den fazla okul okuyan kişilerin bilgileri
# ya da toplamda iki' den fazla okul okuyan kişilerin bilgileri
c = cursor.execute("SELECT COUNT(d.kisiID), k.AdSoyad FROM digerEgitimler AS d "
                   "INNER JOIN kisiler AS k ON d.kisiID = k.ID "
                   "GROUP BY kisiID, k.AdSoyad HAVING COUNT(d.kisiID) > 1")

# toplamda birden' den fazla okul okuyan kişilerin okul,bolum,kişilik bilgileri
d = cursor.execute("SELECT k.AdSoyad, o.okulAdi, b.bolumAdi FROM digerEgitimler AS d "
                   "INNER JOIN kisiler AS k ON d.kisiID = k.ID "
                   "INNER JOIN okullar AS o ON d.okulID = o.ID "
                   "INNER JOIN bolumler AS b ON d.bolumID = b.ID "
                   "ORDER BY d.kisiID")

# Çalışılacak sorguyu döndürür
for e in d:
    print(e)

database.close()
