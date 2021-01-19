import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """DROP TABLE IF EXISTS users cascade""",
    """DROP TABLE IF EXISTS routes cascade""",
    """DROP TABLE IF EXISTS activities cascade""",
    """DROP TABLE IF EXISTS route_activities cascade""",
    """DROP TABLE IF EXISTS route_score cascade""",
    """DROP TABLE IF EXISTS activity_image cascade""",


        """CREATE TABLE IF NOT EXISTS users 
    (
        id SERIAL NOT NULL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR (255) NOT NULL,
        name VARCHAR (255) NOT NULL,
        surname VARCHAR (255) NOT NULL,
        email VARCHAR (255) NOT NULL,
        img_url BYTEA

    )""",

    """CREATE TABLE IF NOT EXISTS routes
    (
        id SERIAL NOT NULL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        description VARCHAR (255) NOT NULL,
        img_url BYTEA,
        FOREIGN KEY (user_id) REFERENCES userS(id) ON UPDATE CASCADE ON DELETE CASCADE

    )""",

    """CREATE TABLE IF NOT EXISTS activities
    (
        id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR (255) NOT NULL

    )""",

    """CREATE TABLE IF NOT EXISTS route_activities
    (
        activity_id INT NOT NULL,
        route_id INT NOT NULL,
        FOREIGN KEY (activity_id) REFERENCES activities(id)ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (route_id) REFERENCES routes(id) ON UPDATE CASCADE ON DELETE CASCADE

    )""",

    """CREATE TABLE IF NOT EXISTS activity_image
    (
        activity_id INT NOT NULL,
        image_url VARCHAR NOT NULL,
        FOREIGN KEY (activity_id) REFERENCES activities(id) ON UPDATE CASCADE ON DELETE CASCADE

    )""",


   """INSERT INTO activities(id, name, description) VALUES (0, 'Kadıköy-Beşiktaş Vapuruna Bin', 'Boğaz hattında çalışan vapurlardan birine binmek İstanbul’da yapılacak en güzel, en ucuz ve en keyifli aktivitelerden biri. Eğer Anadolu yakasında iseniz Kadıköy-Beşiktaş vapuruna binip Beşiktaş’a varıncaya kadar, İstanbul’da görülmesi gereken yerlerden Haydarpaşa Garı’nı, Dolmabahçe ve Topkapı Sarayları’nı, Galata Kulesi’ni ve kıyılardaki önemli sarayları İstanbul Boğazı’nın ortasından izleyebilirsiniz.')""",
   """INSERT INTO activity_image(activity_id, image_url) VALUES (0, 'https://gezentianne.com/wp-content/uploads/2019/05/kad%C4%B1koy_vapuru_istanbulda_yapilacak_aktiviteler.jpg')""",
 """INSERT INTO activities(id, name, description) VALUES (1, 'Ortaköy’de Kumpir Ye', 'Istanbul dediğinizde ilk akla gelen manzara, Ortaköy Camisi’ni ve Boğaz Köprüsü’nü de içine alan aşağıdaki fotoğraftaki manzara. Ortaköy girişinde sıra sıra dizilmiş kumpircilerden sevdiğiniz malzemelerle hazırlanmış kumpirinizi alıp bu manzaraya nazır banklarda oturmak ve kumpirinizi kaşıklamak İstanbul’da yapılacak aktivitelerin olmazsa olmazlarından biri.')""",
   """INSERT INTO activity_image(activity_id, image_url) VALUES (1, 'https://gezentianne.com/wp-content/uploads/2019/05/istanbulda_yapilacak_aktiviteler_ortakoy_kumpir.jpg')""",

    """INSERT INTO activities(id, name, description) VALUES (2, 'Kuruçeşme Bebek Arası Yürüyüş', 'İstanbul Boğazı kenarındaki en keyifli yürüyüş rotasına sahip Kuruçeşme-Arnavutköy-Bebek-Rumeli Hisarı hattını yaklaşık 1 saatte yürüyebilir, İstanbul Boğazı’nın keyfini maksimum şekilde çıkarabilirsiniz. Yürüyüş boyunca yine Boğaz’a sıfır olarak konumlandırılmış İstanbul’da görülecek en güzel yerlerden Kuruçeşme Parkı ve Bebek Parkı’nda mola verebilirsiniz.')""",
"""INSERT INTO activity_image(activity_id, image_url) VALUES (2, 'https://gezentianne.com/wp-content/uploads/2017/09/istanbul_gezilecek_tarihi_turistik_yerler_bebek.jpg')""",
"""INSERT INTO activities(id, name, description) VALUES (3, 'Emirgan Korusu Gezintisi', 'Özellikle Lale zamanı olan Nisan ve Mayıs döneminde Emirgan Korusu’nu gezmek İstanbul’da yapılacak görsel anlamda en büyüleyici aktivitelerden biri. Emirgan korusu hafta sonu İstanbul’un kargaşasından kaçıp kendini doğanın kollarını bırakmak isteyen İstanbulluların tercih ettiği yeşillik ve ormanlık yerlerin başında geliyor.')""",
"""INSERT INTO activity_image(activity_id, image_url) VALUES (3, 'https://gezentianne.com/wp-content/uploads/2017/10/emirgan_korusu_nerede_nasil_gidilir_lale_kahvalti.jpg')""",
"""INSERT INTO activities(id, name, description) VALUES (4, 'İstiklal Caddesi’ni Keşfedin', 'Taksim’e geldiğinizde Taksim Meydanı’ndan İstiklal Caddesi boyunca Galatasaray Lisesi’ne doğru yürüyüş yapabilir, sağlı sollu konumlanırılmış kafeleri butikleri görebilirsiniz. Beyoğlu Çikolatacısı’ndan bütün fındıklı Beyoğlu çikolatası almayı ihmal etmeyin derim.')""",
"""INSERT INTO activity_image(activity_id, image_url) VALUES (4, 'https://gezentianne.com/wp-content/uploads/2017/09/istanbul_gezilecek_tarihi_turistik_yerler_taksim-2.jpg')""",
"""INSERT INTO activities(id, name, description) VALUES (5, 'Madame Tussauds Müzesi Gezisi', 'Ünlü balmumu heykel müzesi İstiklal Caddesi’ndeki Madame Tussauds’yu ziyaret etmeli. Madame Tussauds’da Arda Turan’dan Hidayet Türkoğlu’na, Einstein’dan Leonardo de Vinci’ye, Zeki Müren’den Madonna’ya, Justin Bieber’dan Lady Gaga’ya, MFÖ’den Rihanna’ya, Adile Naşit’ten Barış Manço’ya, Shek’ten Hollywood yıldızlarına yerli yabancı pek çok ünlü ismi bir arada ve yakından görme imkanı bulup instagramlık muhteşem fotolar çektirebilirsiniz.')""",
"""INSERT INTO activity_image(activity_id, image_url) VALUES (5, 'https://gezentianne.com/wp-content/uploads/2019/05/istanbulda_yapilacak_aktiviteler_madame_tussauds.jpg')""",

]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    initialize(url)