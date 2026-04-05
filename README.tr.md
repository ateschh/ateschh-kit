# ateschh-kit

> Claude Code ve Antigravity için yapılandırılmış bir AI geliştirme sistemi.
> Fikirden dağıtıma kadar, bağlam kaybı ve proje terk etme olmadan çalışır.

---

## Kurulum

```bash
npx ateschh-kit@latest
```

Hepsi bu. Sistem bulunduğunuz dizine kurulur.

> Her zaman `@latest` kullanın — npx paketleri yerel olarak cache'ler, `@latest` olmadan eski sürümü alabilirsiniz.

**Mevcut kurulumu güncellemek** (projelerinize dokunmaz):

```bash
npx ateschh-kit@latest --update
```

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
| `/design` | Sayfalar, özellikler ve tasarım sistemi |
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
/brainstorm  ← fikrinizi anlatın, Claude takip soruları sorar
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

**Claude Code ile Antigravity arasında geçiş:**
```
Claude Code  → /save
Antigravity  → /resume   ← tam kaldığınız yerden devam eder
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
├── .claude/
│   ├── rules/             ← 7 otomatik yüklenen davranış kuralı
│   └── commands/          ← Slash komutları (Claude Code native)
├── .agent/
│   └── workflows/         ← Slash komutları (Antigravity native)
├── agents/                ← 9 uzman ajan
├── skills/                ← 9 yeniden kullanılabilir atomik yetenek
└── templates/             ← Proje dosyası şablonları
```

> `.claude/commands/` ve `.agent/workflows/` birebir aynı dosyaları içerir — her platform için biri.

---

## Desteklenen Platformlar

| Platform | Slash Komutları | Durum |
|----------|----------------|-------|
| Claude Code | `.claude/commands/` | ✅ Tam destek |
| Antigravity | `.agent/workflows/` | ✅ Tam destek |
| Cursor | CLAUDE.md üzerinden | ✅ Çalışır |
| Windsurf | CLAUDE.md üzerinden | ✅ Çalışır |

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

## Kalite Seviyeleri

Her görev devam etmeden önce bu seviyeleri geçmek zorunda:

| Seviye | Ne Kontrol Eder | Ne Zaman |
|--------|----------------|---------|
| L1 | Build/tip/lint hatası yok | Her zaman |
| L2 | Özellik tanımlandığı gibi çalışıyor | Her zaman |
| L3 | Tüm sistem içinde doğru çalışıyor | `/test`'te |
| L4 | Performans, güvenlik, UX | `/deploy` öncesi |

---

## Lisans

MIT — Özgürce kullanın, özgürce değiştirin, atıf zorunluluğu yok.

---

## Katkı Sağlamak

[CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın.
