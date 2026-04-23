🏋️‍♂️ Fitness Takip Sistemi
📌 Proje Hakkında
Fitness Takip Sistemi, bireylerin fiziksel aktivitelerini, sağlık verilerini ve kişisel hedeflerini sistematik bir şekilde yönetmelerini sağlamak amacıyla geliştirilmiş bir yazılım uygulamasıdır. Proje, Python programlama dili kullanılarak Nesne Tabanlı Programlama (OOP) yaklaşımı ile tasarlanmıştır.
Sistem; sporcu yönetimi, antrenman takibi, günlük veri kaydı, hedef belirleme ve raporlama gibi temel işlevleri kapsamaktadır.
🎯 Amaç
Bu projenin temel amacı:
Kullanıcıların fitness süreçlerini dijital ortamda takip edebilmesini sağlamak
Sağlık verilerini düzenli ve anlamlı şekilde analiz etmek
Hedef odaklı ilerleme takibi sunmak
⚙️ Özellikler
👤 Sporcu kaydı ve profil yönetimi
🏃‍♂️ Antrenman ekleme ve listeleme
🔥 Kalori hesaplama
📊 BMI (Vücut Kitle İndeksi) hesaplama
📝 Günlük takip (kalori, su, adım)
🎯 Hedef belirleme ve ilerleme analizi
📈 Genel raporlama sistemi
🧱 Sistem Mimarisi
Proje, aşağıdaki temel sınıflardan oluşmaktadır:
Sporcu → Kullanıcı bilgileri ve ana işlemler
Antrenman → Egzersiz kayıtları
Takip → Günlük sağlık verileri
Hedef → Kullanıcı hedefleri
FitnessYonetici → Sistem yönetimi
Bu yapı sayesinde sistem:
Modüler
Genişletilebilir
Bakımı kolay
bir hale getirilmiştir.
💻 Gereksinimler
Python 3.x
Terminal / Komut satırı
Herhangi bir ek kütüphane gerektirmez.
🚀 Kurulum ve Çalıştırma
Projeyi çalıştırmak için:
git clone https://github.com/kullaniciadi/fitness-takip.git
cd fitness-takip
python fitness.py
Program başlatıldığında:
Demo veriler otomatik yüklenir
Ana menü ekrana gelir
🖥️ Kullanım
Program çalıştırıldığında aşağıdaki ana menü görüntülenir:
1. Sporcu Kaydı Ekle
2. Sporcu Listele
3. Sporcu Profili Görüntüle
4. Antrenman Ekle
5. Antrenmanları Listele
6. Günlük Takip Ekle
7. Takip Kayıtlarını Görüntüle
8. Hedef Ekle
9. Hedefleri Görüntüle
10. İlerleme Kaydet
11. Genel Rapor
12. BMI Raporu
0. Çıkış
Kullanıcı, ilgili numarayı girerek işlem yapabilir.
🧮 Hesaplamalar
📊 BMI (Vücut Kitle İndeksi)
BMI= 
boy 
2
 
kilo
​	
 
Boy metre cinsine çevrilerek hesaplanır.
🔥 Kalori Hesaplama
Kalori=katsayı×s 
u
¨
 re×kilo
Her antrenman türü için farklı katsayılar kullanılmaktadır.
📊 Raporlama
Genel Rapor
Toplam sporcu sayısı
Toplam antrenman süresi
Yakılan toplam kalori
BMI Raporu
Tüm sporcuların BMI değerleri
Kategori bilgileri
🛡️ Hata Kontrolleri
Sistem aşağıdaki durumlara karşı koruma sağlar:
Geçersiz girişler kontrol edilir
Negatif değerler engellenir
Varsayılan değerler atanır
Kullanıcıya uyarı mesajları verilir
🧪 Demo Veriler
Program başlangıcında:
3 sporcu
Antrenman kayıtları
Günlük takip verileri
otomatik olarak yüklenir.
🔮 Geliştirme Önerileri
Grafiksel kullanıcı arayüzü (GUI)
Veritabanı entegrasyonu
Mobil uygulama desteği
Yapay zekâ destekli analiz
