"""
=============================================================
  FİTNESS TAKİP SİSTEMİ - Proje 7
  Nesne Tabanlı Programlama (OOP) ile geliştirilmiştir.
=============================================================
  Özellikler:
    - Sporcu kaydı ve profil yönetimi
    - BMI (Vücut Kitle İndeksi) hesaplama
    - Antrenman ekleme ve listeleme
    - Kalori & süre takibi
    - Hedef belirleme ve ilerleme raporu
    - Günlük takip kaydı
=============================================================
"""

from __future__ import annotations
from datetime import date, datetime
from typing import Optional


# ─────────────────────────────────────────────
#  YARDIMCI FONKSİYON
# ─────────────────────────────────────────────

def baslik_yazdir(metin: str) -> None:
    """Konsola süslü bir başlık yazdırır."""
    print("\n" + "=" * 50)
    print(f"  {metin}")
    print("=" * 50)


# ─────────────────────────────────────────────
#  1. SINIF: Antrenman
# ─────────────────────────────────────────────

class Antrenman:
    """
    Tek bir antrenman seansını temsil eder.

    Özellikler:
        antrenman_id  : Benzersiz kimlik numarası
        tur           : Antrenman türü (ör. Koşu, Yüzme)
        sure          : Dakika cinsinden süre
        yogunluk      : Düşük / Orta / Yüksek
        aciklama      : Kullanıcının ek notları
    """

    # Her yeni antrenman için otomatik artan ID sayacı
    _id_sayaci: int = 1

    # Her antrenman türü için kg başına yakılan kalori katsayısı (kcal/dk/kg)
    KALORI_KATSAYISI: dict = {
        "koşu":          0.133,
        "yürüyüş":       0.067,
        "bisiklet":      0.100,
        "yüzme":         0.117,
        "ağırlık":       0.083,
        "yoga":          0.050,
        "hiit":          0.150,
        "pilates":       0.058,
        "dans":          0.092,
        "diğer":         0.075,
    }

    def __init__(self, tur: str, sure: int,
                 yogunluk: str = "Orta", aciklama: str = "") -> None:
        self.antrenman_id: int  = Antrenman._id_sayaci
        self.tur: str           = tur.lower()
        # HATA KORUMASI: Negatif veya sıfır süre girilirse 1 dakikaya sabitlenir
        if sure <= 0:
            print(f"⚠️  Uyarı: Süre {sure} dk geçersiz. 1 dk olarak ayarlandı.")
            sure = 1
        self.sure: int          = sure          # dakika
        # HATA KORUMASI: Geçersiz yoğunluk girilirse varsayılan atanır
        if yogunluk not in {"Düşük", "Orta", "Yüksek"}:
            print(f"⚠️  Uyarı: '{yogunluk}' geçersiz yoğunluk. 'Orta' kullanıldı.")
            yogunluk = "Orta"
        self.yogunluk: str      = yogunluk
        self.aciklama: str      = aciklama
        self.tarih: date        = date.today()  # otomatik bugünün tarihi

        Antrenman._id_sayaci += 1

    # ── Kalori hesaplama ──────────────────────
    def kalori_hesapla(self, kilo: float) -> float:
        """
        Sporcunun kilosuna ve antrenmana göre yakılan kaloriyi döndürür.
        Formül: katsayı × süre(dk) × kilo(kg)
        """
        katsayi = self.KALORI_KATSAYISI.get(self.tur,
                                             self.KALORI_KATSAYISI["diğer"])
        return round(katsayi * self.sure * kilo, 1)

    # ── Bilgi yazdırma ────────────────────────
    def bilgi_yazdir(self, kilo: float = 0.0) -> None:
        print(f"  [{self.antrenman_id}] {self.tarih} | "
              f"Tür: {self.tur.capitalize():<12} | "
              f"Süre: {self.sure:>3} dk | "
              f"Yoğunluk: {self.yogunluk:<8}", end="")
        if kilo > 0:
            print(f" | Kalori: ~{self.kalori_hesapla(kilo)} kcal", end="")
        print()

    def __str__(self) -> str:
        return (f"Antrenman #{self.antrenman_id} | "
                f"{self.tur.capitalize()} | {self.sure} dk")


# ─────────────────────────────────────────────
#  2. SINIF: Takip (günlük kayıt)
# ─────────────────────────────────────────────

class Takip:
    """
    Belirli bir tarihe ait günlük sağlık kaydını temsil eder.

    Özellikler:
        tarih           : Kaydın ait olduğu gün
        kalori_alinan   : O gün alınan toplam kalori (kcal)
        su_miktari      : İçilen su miktarı (litre)
        adim_sayisi     : Atılan adım sayısı
        not_            : Kullanıcının günlük notu
    """

    def __init__(self, tarih: date, kalori_alinan: float,
                 su_miktari: float, adim_sayisi: int,
                 not_: str = "") -> None:
        self.tarih: date          = tarih
        self.kalori_alinan: float = kalori_alinan
        self.su_miktari: float    = su_miktari
        self.adim_sayisi: int     = adim_sayisi
        self.not_: str            = not_

    def bilgi_yazdir(self) -> None:
        print(f"  📅 {self.tarih} | "
              f"Kalori Alınan: {self.kalori_alinan} kcal | "
              f"Su: {self.su_miktari} lt | "
              f"Adım: {self.adim_sayisi}")
        if self.not_:
            print(f"     Not: {self.not_}")

    def __str__(self) -> str:
        return f"Takip | {self.tarih} | {self.kalori_alinan} kcal"


# ─────────────────────────────────────────────
#  3. SINIF: Hedef
# ─────────────────────────────────────────────

class Hedef:
    """
    Sporcunun belirlediği fitness hedefini temsil eder.

    Özellikler:
        hedef_turu      : "kilo_ver" / "kilo_al" / "koru" / "kondisyon"
        hedef_deger     : Hedeflenen kilo (kg) veya haftalık antrenman sayısı
        bitis_tarihi    : Hedefe ulaşılmak istenen son tarih
        tamamlandi_mi   : Hedefe ulaşıldı mı?
    """

    def __init__(self, hedef_turu: str,
                 hedef_deger: float,
                 bitis_tarihi: date) -> None:
        self.hedef_turu: str      = hedef_turu
        self.hedef_deger: float   = hedef_deger
        self.bitis_tarihi: date   = bitis_tarihi
        self.tamamlandi_mi: bool  = False

    def durum_kontrol(self, mevcut_kilo: float) -> str:
        """
        Sporcunun mevcut kilosuna bakarak hedefe ne kadar yaklaşıldığını döndürür.
        """
        if self.hedef_turu in ("kilo_ver", "kilo_al", "koru"):
            fark = round(mevcut_kilo - self.hedef_deger, 1)
            if abs(fark) < 0.5:
                self.tamamlandi_mi = True
                return "✅ Hedefe ulaşıldı!"
            elif fark > 0:
                return f"⚠️  Hedefe ulaşmak için {fark} kg daha verilmeli."
            else:
                return f"⚠️  Hedefe ulaşmak için {abs(fark)} kg daha alınmalı."
        return "ℹ️  Kondisyon hedefi — antrenmanlara devam edin."

    def __str__(self) -> str:
        return (f"Hedef: {self.hedef_turu.replace('_', ' ').title()} | "
                f"Değer: {self.hedef_deger} | "
                f"Bitiş: {self.bitis_tarihi}")


# ─────────────────────────────────────────────
#  4. ANA SINIF: Sporcu
# ─────────────────────────────────────────────

class Sporcu:
    """
    Fitness takip sistemindeki kullanıcıyı temsil eder.

    Özellikler:
        sporcu_id        : Benzersiz kimlik
        ad               : Sporcu adı-soyadı
        yas              : Yaş
        cinsiyet         : "E" / "K"
        kilo             : Kilogram
        boy              : Santimetre
        antrenmanlar     : Bu sporcuya ait Antrenman nesnelerinin listesi
        takip_kayitlari  : Bu sporcuya ait Takip nesnelerinin listesi
        hedefler         : Bu sporcuya ait Hedef nesnelerinin listesi
    """

    _id_sayaci: int = 1

    def __init__(self, ad: str, yas: int,
                 cinsiyet: str, kilo: float, boy: float) -> None:
        self.sporcu_id: int            = Sporcu._id_sayaci
        self.ad: str                   = ad
        self.yas: int                  = max(1, yas)        # HATA KORUMASI: yaş ≥ 1
        self.cinsiyet: str             = cinsiyet.upper()   # "E" veya "K"
        # HATA KORUMASI: kilo ve boy negatif veya sıfır olamaz
        if kilo <= 0:
            raise ValueError(f"Kilo geçersiz: {kilo}. Pozitif bir değer girin.")
        if boy <= 0:
            raise ValueError(f"Boy geçersiz: {boy}. Pozitif bir değer girin.")
        self.kilo: float               = kilo               # kg
        self.boy: float                = boy                # cm
        self.antrenmanlar: list        = []                 # Antrenman nesneleri
        self.takip_kayitlari: list     = []                 # Takip nesneleri
        self.hedefler: list            = []                 # Hedef nesneleri
        self.kayit_tarihi: date        = date.today()

        Sporcu._id_sayaci += 1

    # ─── BMI Hesaplama ────────────────────────
    def bmi_hesapla(self) -> float:
        """
        Vücut Kitle İndeksi = kilo / (boy_metre)²
        HATA KORUMASI: Boy 0 veya negatif girilirse ZeroDivisionError önlenir.
        """
        if self.boy <= 0:
            print("⚠️  Hata: Boy değeri 0 veya negatif olamaz. BMI hesaplanamadı.")
            return 0.0
        boy_m = self.boy / 100
        return round(self.kilo / (boy_m ** 2), 1)

    def bmi_kategori(self) -> str:
        """BMI değerine göre kategori döndürür."""
        bmi = self.bmi_hesapla()
        if bmi < 18.5:
            return "Zayıf"
        elif bmi < 25.0:
            return "Normal"
        elif bmi < 30.0:
            return "Fazla Kilolu"
        else:
            return "Obez"

    # ─── Kalp Atış Hızı Zonu ─────────────────
    def max_kalp_atisi(self) -> int:
        """220 - yaş formülü ile maksimum kalp atış hızını hesaplar."""
        return 220 - self.yas

    def ideal_bmi_kilo_araligi(self) -> tuple:
        """18.5 – 24.9 BMI aralığına karşılık gelen kilo aralığını döndürür."""
        boy_m = self.boy / 100
        alt   = round(18.5 * boy_m ** 2, 1)
        ust   = round(24.9 * boy_m ** 2, 1)
        return (alt, ust)

    # ─── Antrenman İşlemleri ──────────────────
    def antrenman_ekle(self, antrenman: "Antrenman") -> None:
        """Sporcuya yeni bir antrenman seansı ekler."""
        self.antrenmanlar.append(antrenman)
        print(f"✅ Antrenman eklendi: {antrenman}")

    def toplam_sure(self) -> int:
        """Tüm antrenmanların toplam süresini dakika olarak döndürür."""
        return sum(a.sure for a in self.antrenmanlar)

    def toplam_kalori_yakilan(self) -> float:
        """Tüm antrenmanlar için yakılan toplam kaloriyi döndürür."""
        return round(sum(a.kalori_hesapla(self.kilo)
                         for a in self.antrenmanlar), 1)

    def antrenman_listele(self) -> None:
        """Kayıtlı tüm antrenmanları ekrana basar."""
        if not self.antrenmanlar:
            print("  Henüz antrenman kaydı yok.")
            return
        for a in self.antrenmanlar:
            a.bilgi_yazdir(self.kilo)

    # ─── Günlük Takip ─────────────────────────
    def takip_ekle(self, kayit: "Takip") -> None:
        """Günlük sağlık verisi kaydı ekler."""
        self.takip_kayitlari.append(kayit)
        print(f"✅ Günlük takip eklendi: {kayit.tarih}")

    def takip_listele(self) -> None:
        """Tüm günlük takip kayıtlarını ekrana basar."""
        if not self.takip_kayitlari:
            print("  Henüz takip kaydı yok.")
            return
        for t in self.takip_kayitlari:
            t.bilgi_yazdir()

    # ─── Hedef İşlemleri ──────────────────────
    def hedef_ekle(self, hedef: "Hedef") -> None:
        """Sporcuya yeni bir hedef ekler."""
        self.hedefler.append(hedef)
        print(f"✅ Hedef eklendi: {hedef}")

    def hedef_listele(self) -> None:
        """Tüm hedefleri ve durumlarını listeler."""
        if not self.hedefler:
            print("  Henüz hedef belirlenmemiş.")
            return
        for h in self.hedefler:
            durum = "✅ Tamamlandı" if h.tamamlandi_mi else h.durum_kontrol(self.kilo)
            print(f"  🎯 {h}  →  {durum}")

    # ─── İlerleme Kaydı ───────────────────────
    def ilerleme_kaydet(self, yeni_kilo: float) -> None:
        """
        Sporcunun kilosunu günceller ve değişimi ekrana yazdırır.
        Bu metot ödevde istenen temel metoddur.
        """
        eski_kilo  = self.kilo
        self.kilo  = yeni_kilo
        degisim    = round(yeni_kilo - eski_kilo, 1)
        isaret     = "📉" if degisim < 0 else ("📈" if degisim > 0 else "➡️")
        print(f"\n{isaret} Kilo güncellendi: {eski_kilo} kg → {yeni_kilo} kg "
              f"(Değişim: {degisim:+.1f} kg)")
        print(f"   Yeni BMI: {self.bmi_hesapla()} — {self.bmi_kategori()}")

        # Hedefleri otomatik kontrol et
        for h in self.hedefler:
            if not h.tamamlandi_mi:
                print("  ", h.durum_kontrol(self.kilo))

    # ─── Profil & Özet ───────────────────────
    def profil_yazdir(self) -> None:
        """Sporcunun tam profilini yazdırır."""
        alt, ust = self.ideal_bmi_kilo_araligi()
        print(f"""
  👤 Sporcu Profili
  ─────────────────────────────────────
  ID           : {self.sporcu_id}
  Ad Soyad     : {self.ad}
  Yaş          : {self.yas}
  Cinsiyet     : {"Erkek" if self.cinsiyet == "E" else "Kadın"}
  Kilo         : {self.kilo} kg
  Boy          : {self.boy} cm
  BMI          : {self.bmi_hesapla()} ({self.bmi_kategori()})
  İdeal Kilo   : {alt} – {ust} kg
  Max Nabız    : {self.max_kalp_atisi()} bpm
  Kayıt Tarihi : {self.kayit_tarihi}
  ─────────────────────────────────────
  Toplam Antrenman : {len(self.antrenmanlar)} seans
  Toplam Süre      : {self.toplam_sure()} dakika
  Toplam Kalori    : {self.toplam_kalori_yakilan()} kcal yakıldı
  Günlük Kayıt     : {len(self.takip_kayitlari)} gün
  Aktif Hedef      : {sum(1 for h in self.hedefler if not h.tamamlandi_mi)} adet
        """)

    def __str__(self) -> str:
        return (f"Sporcu #{self.sporcu_id} | {self.ad} | "
                f"{self.kilo} kg / {self.boy} cm | BMI: {self.bmi_hesapla()}")


# ─────────────────────────────────────────────
#  5. YÖNETİM SINIFI: FitnessYonetici
# ─────────────────────────────────────────────

class FitnessYonetici:
    """
    Tüm sporcuları merkezi olarak yöneten sistem sınıfı.

    Özellikler:
        sporcular : Kayıtlı Sporcu nesnelerinin sözlüğü  {sporcu_id: Sporcu}
    """

    def __init__(self) -> None:
        self.sporcular: dict = {}   # {sporcu_id (int): Sporcu}

    # ─── Sporcu CRUD ──────────────────────────
    def sporcu_ekle(self, sporcu: Sporcu) -> None:
        """Sisteme yeni sporcu kaydeder."""
        self.sporcular[sporcu.sporcu_id] = sporcu
        print(f"✅ Sporcu eklendi: {sporcu.ad} (ID: {sporcu.sporcu_id})")

    def sporcu_bul(self, sporcu_id: int) -> Optional[Sporcu]:
        """ID ile sporcu arar, bulamazsa None döner."""
        return self.sporcular.get(sporcu_id)

    def sporcu_listele(self) -> None:
        """Sistemdeki tüm sporcuları listeler."""
        if not self.sporcular:
            print("  Kayıtlı sporcu yok.")
            return
        for sp in self.sporcular.values():
            print(f"  {sp}")

    def sporcu_sil(self, sporcu_id: int) -> bool:
        """Sporcuyu sistemden siler."""
        if sporcu_id in self.sporcular:
            silinen = self.sporcular.pop(sporcu_id)
            print(f"🗑️  {silinen.ad} sistemden silindi.")
            return True
        print("❌ Sporcu bulunamadı.")
        return False

    # ─── Genel Rapor ──────────────────────────
    def genel_rapor(self) -> None:
        """Tüm sporcuların özet istatistiklerini gösterir."""
        baslik_yazdir("GENEL RAPOR")
        if not self.sporcular:
            print("  Kayıtlı sporcu yok.")
            return

        toplam_kalori = sum(sp.toplam_kalori_yakilan()
                            for sp in self.sporcular.values())
        toplam_sure   = sum(sp.toplam_sure()
                            for sp in self.sporcular.values())

        print(f"  Toplam Sporcu     : {len(self.sporcular)}")
        print(f"  Toplam Kalori     : {toplam_kalori} kcal yakıldı")
        print(f"  Toplam Antrenman  : {toplam_sure} dakika")

        print("\n  En çok antrenman yapanlar:")
        sirali = sorted(self.sporcular.values(),
                        key=lambda s: s.toplam_sure(), reverse=True)
        for i, sp in enumerate(sirali[:3], 1):
            print(f"  {i}. {sp.ad:<20} {sp.toplam_sure()} dk")

    def bmi_raporu(self) -> None:
        """Tüm sporcuların BMI durumunu raporlar."""
        baslik_yazdir("BMI RAPORU")
        for sp in self.sporcular.values():
            print(f"  {sp.ad:<20} BMI: {sp.bmi_hesapla():<6} → {sp.bmi_kategori()}")


# ─────────────────────────────────────────────
#  KONSOL MENÜSÜ
# ─────────────────────────────────────────────

def menu_sporcu_sec(yonetici: FitnessYonetici) -> Optional[Sporcu]:
    """Kullanıcıdan sporcu ID alır ve nesneyi döner."""
    yonetici.sporcu_listele()
    try:
        sid = int(input("\n  Sporcu ID girin: "))
        sp  = yonetici.sporcu_bul(sid)
        if sp is None:
            print("❌ Sporcu bulunamadı.")
        return sp
    except ValueError:
        print("❌ Geçersiz giriş.")
        return None


def menu_antrenman_ekle(yonetici: FitnessYonetici) -> None:
    baslik_yazdir("ANTRENMAN EKLE")
    sp = menu_sporcu_sec(yonetici)
    if sp is None:
        return

    print("\n  Antrenman türleri: koşu, yürüyüş, bisiklet, yüzme,")
    print("                    ağırlık, yoga, hiit, pilates, dans, diğer")
    tur      = input("  Tür       : ").strip() or "diğer"
    try:
        sure = int(input("  Süre (dk) : ") or "30")
    except ValueError:
        print("⚠️  Geçersiz süre, 30 dk kullanıldı.")
        sure = 30
    yogunluk = input("  Yoğunluk (Düşük/Orta/Yüksek): ").strip() or "Orta"
    aciklama = input("  Not (boş bırakılabilir)      : ").strip()

    a = Antrenman(tur, sure, yogunluk, aciklama)
    sp.antrenman_ekle(a)
    print(f"  Yakılan kalori: ~{a.kalori_hesapla(sp.kilo)} kcal")


def menu_takip_ekle(yonetici: FitnessYonetici) -> None:
    baslik_yazdir("GÜNLÜK TAKİP EKLE")
    sp = menu_sporcu_sec(yonetici)
    if sp is None:
        return

    kalori  = float(input("  Alınan kalori (kcal) : ") or "2000")
    su      = float(input("  Su (litre)           : ") or "2.0")
    adim    = int(input("  Adım sayısı          : ") or "5000")
    not_    = input("  Günlük not           : ").strip()

    t = Takip(date.today(), kalori, su, adim, not_)
    sp.takip_ekle(t)


def menu_hedef_ekle(yonetici: FitnessYonetici) -> None:
    baslik_yazdir("HEDEF EKLE")
    sp = menu_sporcu_sec(yonetici)
    if sp is None:
        return

    print("  Hedef türleri: kilo_ver, kilo_al, koru, kondisyon")
    tur    = input("  Tür          : ").strip() or "koru"
    deger  = float(input("  Hedef değer  : ") or "70")
    bitis  = input("  Bitiş tarihi (YYYY-AA-GG): ").strip()
    try:
        bitis_t = datetime.strptime(bitis, "%Y-%m-%d").date()
    except ValueError:
        print("⚠️  Tarih formatı hatalı, bugün kullanıldı.")
        bitis_t = date.today()

    h = Hedef(tur, deger, bitis_t)
    sp.hedef_ekle(h)


def menu_ilerleme_kaydet(yonetici: FitnessYonetici) -> None:
    baslik_yazdir("İLERLEME KAYDET (KİLO GÜNCELLE)")
    sp = menu_sporcu_sec(yonetici)
    if sp is None:
        return
    print(f"  Mevcut kilo: {sp.kilo} kg")
    yeni = float(input("  Yeni kilo   : ") or sp.kilo)
    sp.ilerleme_kaydet(yeni)


def ana_menu() -> None:
    """Ana konsol menüsünü çalıştırır."""
    yonetici = FitnessYonetici()

    # ── Demo verileri yükle ──
    demo_yukle(yonetici)

    while True:
        baslik_yazdir("FITNESS TAKİP SİSTEMİ — ANA MENÜ")
        print("  1. Sporcu Kaydı Ekle")
        print("  2. Sporcu Listele")
        print("  3. Sporcu Profili Görüntüle")
        print("  4. Antrenman Ekle")
        print("  5. Antrenmanları Listele")
        print("  6. Günlük Takip Ekle")
        print("  7. Takip Kayıtlarını Görüntüle")
        print("  8. Hedef Ekle")
        print("  9. Hedefleri Görüntüle")
        print(" 10. İlerleme Kaydet (Kilo Güncelle)")
        print(" 11. Genel Rapor")
        print(" 12. BMI Raporu")
        print("  0. Çıkış")

        secim = input("\n  Seçiminiz: ").strip()

        if secim == "1":
            baslik_yazdir("YENİ SPORCU KAYDI")
            ad       = input("  Ad Soyad  : ")
            yas      = int(input("  Yaş       : ") or "25")
            cinsiyet = input("  Cinsiyet (E/K): ").strip().upper() or "E"
            kilo     = float(input("  Kilo (kg) : ") or "70")
            boy      = float(input("  Boy  (cm) : ") or "170")
            sp = Sporcu(ad, yas, cinsiyet, kilo, boy)
            yonetici.sporcu_ekle(sp)

        elif secim == "2":
            baslik_yazdir("SPORCU LİSTESİ")
            yonetici.sporcu_listele()

        elif secim == "3":
            baslik_yazdir("SPORCU PROFİLİ")
            sp = menu_sporcu_sec(yonetici)
            if sp:
                sp.profil_yazdir()

        elif secim == "4":
            menu_antrenman_ekle(yonetici)

        elif secim == "5":
            baslik_yazdir("ANTRENMAN LİSTESİ")
            sp = menu_sporcu_sec(yonetici)
            if sp:
                sp.antrenman_listele()

        elif secim == "6":
            menu_takip_ekle(yonetici)

        elif secim == "7":
            baslik_yazdir("GÜNLÜK TAKİP KAYITLARI")
            sp = menu_sporcu_sec(yonetici)
            if sp:
                sp.takip_listele()

        elif secim == "8":
            menu_hedef_ekle(yonetici)

        elif secim == "9":
            baslik_yazdir("HEDEFLER")
            sp = menu_sporcu_sec(yonetici)
            if sp:
                sp.hedef_listele()

        elif secim == "10":
            menu_ilerleme_kaydet(yonetici)

        elif secim == "11":
            yonetici.genel_rapor()

        elif secim == "12":
            yonetici.bmi_raporu()

        elif secim == "0":
            print("\n  👋 Görüşürüz! Sağlıklı kalın.\n")
            break

        else:
            print("  ❌ Geçersiz seçim, tekrar deneyin.")

        input("\n  [Enter ile devam edin]")


# ─────────────────────────────────────────────
#  DEMO VERİSİ
# ─────────────────────────────────────────────

def demo_yukle(yonetici: FitnessYonetici) -> None:
    """
    Programı ilk açtığınızda test edebilmek için
    örnek sporcu, antrenman, takip ve hedef verileri oluşturur.
    """
    # Sporcu 1
    s1 = Sporcu("Ali Yılmaz", 28, "E", 85.0, 178.0)
    a1 = Antrenman("koşu",    30, "Orta",   "Sabah koşusu")
    a2 = Antrenman("ağırlık", 45, "Yüksek", "Göğüs günü")
    s1.antrenman_ekle(a1)
    s1.antrenman_ekle(a2)
    t1 = Takip(date.today(), 2200, 2.5, 8000, "İyi hissettim")
    s1.takip_ekle(t1)
    h1 = Hedef("kilo_ver", 78.0, date(2025, 12, 31))
    s1.hedef_ekle(h1)
    yonetici.sporcu_ekle(s1)

    # Sporcu 2
    s2 = Sporcu("Ayşe Kara", 24, "K", 62.0, 165.0)
    a3 = Antrenman("yoga",   60, "Düşük", "Sabah seansı")
    a4 = Antrenman("yüzme",  40, "Orta",  "Havuz antrenmanı")
    s2.antrenman_ekle(a3)
    s2.antrenman_ekle(a4)
    t2 = Takip(date.today(), 1800, 3.0, 10000, "Harika gün!")
    s2.takip_ekle(t2)
    h2 = Hedef("kondisyon", 5, date(2025, 9, 1))
    s2.hedef_ekle(h2)
    yonetici.sporcu_ekle(s2)

    # Sporcu 3
    s3 = Sporcu("Mehmet Demir", 35, "E", 95.0, 182.0)
    a5 = Antrenman("koşu",     25, "Yüksek", "Yoğun seans")
    a6 = Antrenman("bisiklet", 50, "Orta",   "Dış mekân")
    s3.antrenman_ekle(a5)
    s3.antrenman_ekle(a6)
    h3 = Hedef("kilo_ver", 85.0, date(2025, 11, 15))
    s3.hedef_ekle(h3)
    yonetici.sporcu_ekle(s3)

    print("\n  ℹ️  Demo verileri yüklendi (3 sporcu, 6 antrenman, 3 takip kaydı).\n")


# ─────────────────────────────────────────────
#  PROGRAMIN GİRİŞ NOKTASI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    ana_menu()