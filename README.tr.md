# ateschh-kit

> Claude Code ve Antigravity için yapılandırılmış bir AI geliştirme sistemi.  
> Fikirden dağıtıma kadar, bağlam kaybı ve proje terk etme olmadan çalışır.

---

## Kurulum

```bash
npx ateschh-kit
```

Hepsi bu. Sistem bulunduğunuz dizine kurulur.

---

## Bu Nedir?

AI ajanlarını yazılım geliştirme sürecinin tamamında yönlendiren yapılandırılmış bir iş akışı sistemi:

```
/brainstorm → /requirements → /design → /build → /test → /deploy
```

Her aşama geçiş gerektiriyor. Brainstorm'dan direkt kodlamaya geçemezsiniz.

## Neden İşe Yarıyor?

| Sorun | Çözüm |
|-------|-------|
| AI oturumlar arasında bağlamı unutuyor | `/save` + `/resume` — Claude Code ve Antigravity arasında çalışır |
| Proje ortasında "gelin framework değiştirelim" | REQUIREMENTS.md onay sonrası kilitlenir |
| Kapsam kayması | Yeni fikirler BACKLOG.md'ye gider — şimdi değil |
| Proje terk etme | STATE.md her zaman sıradakini bilir |
| "Şunu hızlıca düzelt" tuzakları | `/quick` tek seferlik görevler için, `/next` otomatik pilot için |

---

## Komutlar

| Komut | Ne Yapar |
|-------|---------|
| `/new-project` | Yeni proje başlat |
| `/brainstorm` | Fikir analizi + pazar araştırması |
| `/requirements` | Teknoloji yığınını seç ve kilitle |
| `/design` | Sayfalar, özellikler ve versal sistem |
| `/build` | Plandan bir görevi uygula |
| `/test` | L1–L4 kalite kontrolleri |
| `/deploy` | Üretim ortamına dağıt |
| `/status` | Nerede olduğunu gör |
| `/save` | Bağlamı kaydet (çapraz platform) |
| `/resume` | Son oturumdan devam et |
| `/next` | Doğru sonraki adımı otomatik tespit et ve çalıştır |
| `/quick` | Tam pipeline olmadan tek seferlik görev |
| `/map-codebase` | Mevcut projeyi analiz et |
| `/settings` | Yapılandırmayı görüntüle/düzenle |

---

## Nasıl Kullanılır

**Yeni proje başlatmak:**
```
/new-project
/brainstorm  ← fikrinizi anlatın
/requirements
/design
/build  ← tamamlanana kadar tekrarlayın
/test
/deploy
```

**Bir projeye dönmek:**
```
/resume
# veya
/next  ← kaldığınız yeri otomatik tespit eder
```

**Mevcut bir proje üzerinde çalışmak:**
```
/map-codebase
```

---

## İçerik

```
ateschh-kit/
├── CLAUDE.md              ← Ana orkestrasyon dosyası
├── .claude/rules/         ← 7 otomatik yüklenen davranış kuralı
├── agents/                ← 9 uzman ajan
├── skills/                ← 9 yeniden kullanılabilir atomik yetenek
├── workflows/             ← 15 slash-komut iş akışı
├── templates/             ← Proje dosyası şablonları
└── context-agent/         ← Bağlam yönetim sistemi
```

---

## Desteklenen Platformlar

| Platform | Durum |
|----------|-------|
| Claude Code | ✅ Tam destek |
| Antigravity | ✅ Tam destek |
| Cursor | ✅ Çalışır (agents klasörü) |
| Windsurf | ✅ Çalışır (agents klasörü) |

---

## Desteklenen Teknoloji Yığınları

| Tür | Varsayılan Yığın |
|-----|----------------|
| Web Uygulaması | Next.js + Supabase + Vercel |
| Mobil | Expo + Supabase |
| Tarayıcı Uzantısı | Plasmo + TypeScript |
| Backend API | Hono + Cloudflare Workers |
| Masaüstü | Electron / Tauri |

---

## Çapraz Platform Bağlamı

Aynı proje üzerinde Claude Code ve Antigravity'den dönüşümlü çalışın:

```
Platform A → /save
Platform B → /resume   ← tam kaldığınız yerden devam eder
```

---

## Lisans

MIT — Özgürce kullanın, özgürce değiştirin, atıf zorunluluğu yok.

---

## Katkı Sağlamak

[CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın.
