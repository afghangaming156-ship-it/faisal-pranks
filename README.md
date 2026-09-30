# Faisal Pranks 😄

د Resend په مرسته د ټوکو (prank) ایمیل لیږلو Android اپ.
هر پیغام په پای کې دا جمله لري: **This was a prank by Faisal Pranks**

---

## 📱 اپ څه کوي؟

- **Your Name** (اړین) — ستا نوم چې اخیستونکی یې ویني
- **Your Gmail** (اختیاري) — که څوک ځواب ورکړي، دلته راځي (reply-to)
- **To** — د اخیستونکي ایمیل
- **Subject** — د ایمیل عنوان (اختیاري)
- **Message** — ستا پیغام
- **Send now** یا **Schedule** — همدا اوس ولېږه، یا په ټاکلي وخت (لکه 2:30 PM)
- هر پیغام په پای کې پخپله د **Faisal Pranks** جمله زیاتوي (لوی فونت)

### 🔒 پټ مینو — Main Control
په **To** ساحه کې دا کوډ ولیکه:
```
fainet.org-1290
```
بیا **SEND** کېکاږه → **Main Control** خلاصیږي. په هغه کې:
- د **Resend API key** ساحه
- **From email** (ستا verified ایمیل)
- **ټول لیږل شوي ایمیلونه** او اخیستونکي (تاریخچه)

---

## ✅ ۱ برخه — د Resend تنظیم (اړین)

Resend یو ایمیل خدمت دی. د دې لپاره چې اپ ایمیل ولېږي، لومړی دا کار وکړه:

1. لاړ شه **https://resend.com** → یو حساب جوړ کړه (وړیا دی).
2. **API Keys** → **Create API Key** → کوډ کاپي کړه (لکه `re_xxxxxxxx`).
3. **Domains** → که خپل ډومین لرې، هغه verify کړه. بیا `From email` به وي لکه `prank@yourdomain.com`.
   - **ډومین نه لرې؟** د ازموینې لپاره کولی شې `onboarding@resend.dev` وکاروې، خو دا یوازې **ستا خپل** ایمیل ته لیږلی شي (نورو ته نه). د ملګرو لپاره ډومین اړین دی.

> **یادونه:** API key او From email اپ کې د `fainet.org-1290` پټ مینو کې ولیکه او **SAVE** کړه.

---

## ✅ ۲ برخه — APK جوړول (ستا ۴۹۵ MB انټرنیټ ته سم)

د Termux لومړۍ جوړونه ۲-۳ GB ډاونلوډ غواړي — ستا انټرنیټ نه بسیا کوي.
نو له **GitHub Actions** څخه کار اخلو: ټول درانه کار په انټرنیټ (cloud) کې کیږي، ته یوازې وروستی APK (~۱۵ MB) ډاونلوډ کوې.

### ګامونه:
1. لاړ شه **https://github.com** → حساب جوړ کړه (وړیا).
2. **New repository** → نوم یې ورکړه (لکه `faisal-pranks`) → **Create**.
3. د دې فولډر ټول فایلونه هلته اپلوډ کړه (Add file → Upload files → ټول کش کړه → Commit).
   - مهم: `.github/workflows/build.yml` او `data/icon.png` هم شامل کړه.
4. د repository په سر کې **Actions** ټب → که وپوښتل شي "enable" کېکاږه.
5. جوړونه پخپله پیل کیږي (~۱۵-۲۵ دقیقې). شنه ✅ نښه چې ښکاره شوه:
6. هغه build کېکاږه → لاندې **Artifacts** برخه → **FaisalPranks-APK** ډاونلوډ کړه.
7. zip خلاص کړه → دننه APK دی → په خپل فون کې یې نصب کړه.

> که "Install blocked" ووايي: Settings → Apps → Install unknown apps → اجازه ورکړه.

---

## 🛠 بدیل لار — په Termux کې (که کافي انټرنیټ ولرې)

ستا ۶۵ GB ډیسک بس دی، خو ~۳ GB انټرنیټ پکار دی:

```bash
pkg update && pkg upgrade -y
pkg install -y python git zip unzip openjdk-17 autoconf automake libtool
pip install --upgrade buildozer cython
cd faisal-pranks
buildozer android debug
```
APK به دلته وي: `bin/faisalpranks-1.0-debug.apk`

---

## 📂 د فایلونو لیست
```
faisal-pranks/
├── main.py                       ← اصلي اپ کوډ
├── buildozer.spec                ← د جوړونې تنظیمات
├── data/icon.png                 ← ستا لوگو (اپ آیکون)
├── .github/workflows/build.yml   ← د cloud جوړونې سیستم
└── README.md                     ← دا لارښود
```

---

## ⚖️ مهمه یادونه
- دا اپ یوازې **د ټوکو** لپاره دی — هر ایمیل په پای کې څرګندوي چې د Faisal Pranks ټوکه وه.
- د بل چا یا رسمي ادارې په نوم دروغجن (fake) ایمیل مه لېږه.
- Resend خپل قوانین لري؛ سپَم یا دوکه (phishing) ستا حساب بندوي.
