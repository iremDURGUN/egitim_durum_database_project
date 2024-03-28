import pypyodbc

# Çalışmaya başlamadan önce Server bilgisine kendi Server bilginizi yazmayı unutmayın!
# egitimDurum DATABASE'ne bağlanılır.
database = pypyodbc.connect(
    "DRIVER={SQL Server};"
    "Server=ServerName;"
    "Database=egitimDurum;"
    "Trusted_Connection=True;"
)
cursor = database.cursor()

# Önemli!! 
# egitimDbExportWithData.txt dosyasını direkt olarak MSSQL' de çalıştırırsanız veri tabanını veriler ile birlikte oluşturabilirsiniz.
# Eğer tabloları ve verileri kendiniz oluşturmak isterseniz veritabanını MSSQL' de oluşturup 
# buradan da ilgili fonksiyonları çalıştırarak bu işlemleri yapabilirsiniz. 
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
    cursor.execute(f"INSERT INTO kisiler (AdSoyad) VALUES ({x})")
    cursor.commit()


# okullar tablosuna veri girişi için
def okulEkle(x):
    cursor.execute(f"INSERT INTO okullar (okulAdi) VALUES ({x})")
    cursor.commit()


# bolumler tablosuna veri girişi için
def bolumEkle(x):
    cursor.execute(f"INSERT INTO bolumler (bolumAdi) VALUES ({x})")
    cursor.commit()


# okulTipi tablosuna veri girişi için
def okulTipiEkle(x):
    cursor.execute(f"INSERT INTO okulTipi (okulTipi) VALUES ({x})")
    cursor.commit()


# x = kisiID, y = okulID, z = bolumID, k = tipID verisini tutar.
# egitim tablosuna veri girişi için
def egitimEkle(x, y, z, k):
    cursor.execute(f"INSERT INTO egitim (kisiID, okulID, bolumID, tipID) VALUES ({x}, {y}, {z}, {k})")
    cursor.commit()


# digerEgitimler tablosuna veri girişi için
def digerEgitimEkle(x, y, z, k):
    cursor.execute(f"INSERT INTO digerEgitimler (kisiID, okulID, bolumID, tipID) VALUES ({x}, {y}, {z}, {k})")
    cursor.commit()


# digerEgitimEkle("okulID", "4", "8")
# tüm tablo bilgilerini almak için kullanırız
a = cursor.execute("SELECT * FROM digerEgitimler ORDER BY ID").fetchall()

# Birden fazla üniversite okuyan kişilerin isimlerini döndürür.
b = cursor.execute("SELECT DISTINCT(k.AdSoyad) FROM digerEgitimler AS d INNER JOIN kisiler AS k ON d.kisiID = k.ID").fetchall()

# diger egitim tablosunda bir' den fazla okul okuyan kişilerin bilgileri
# ya da toplamda iki' den fazla okul okuyan kişilerin bilgileri
c = cursor.execute("SELECT COUNT(d.kisiID), k.AdSoyad FROM digerEgitimler AS d "
                   "INNER JOIN kisiler AS k ON d.kisiID = k.ID "
                   "GROUP BY kisiID, k.AdSoyad HAVING COUNT(d.kisiID) > 1").fetchall()

# toplamda birden' den fazla okul okuyan kişilerin okul,bolum,kişilik bilgileri
d = cursor.execute("SELECT k.AdSoyad, o.okulAdi, b.bolumAdi FROM digerEgitimler AS d "
                   "INNER JOIN kisiler AS k ON d.kisiID = k.ID "
                   "INNER JOIN okullar AS o ON d.okulID = o.ID "
                   "INNER JOIN bolumler AS b ON d.bolumID = b.ID "
                   "ORDER BY d.kisiID").fetchall()

# Toplamda üniversite okuyan kişi sayısı??
e = cursor.execute("SELECT COUNT(e.tipID) + COUNT(d.tipID) "
                   "FROM digerEgitimler AS d "
                   "INNER JOIN kisiler AS k ON d.kisiID = k.ID "
                   "INNER JOIN egitim AS e ON k.ID = e.kisiID "
                   "WHERE d.tipID = 2 AND e.tipID = 2 GROUP BY e.tipID, d.tipID ").fetchall()

# Çalışılacak sorguyu döndürür
for p in a:
    print(p)

database.close()
