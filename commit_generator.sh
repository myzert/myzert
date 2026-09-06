#!/bin/bash

# Dapatkan jam, tanggal, dan waktu saat ini
HOUR=$(date +%H)
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%H:%M:%S")

# Tentukan ucapan berdasarkan jam (Waktu lokal)
if [ "$HOUR" -ge 05 ] && [ "$HOUR" -lt 11 ]; then
    GREETING="Selamat pagi indonesia"
elif [ "$HOUR" -ge 11 ] && [ "$HOUR" -lt 15 ]; then
    GREETING="Selamat siang indonesia"
elif [ "$HOUR" -ge 15 ] && [ "$HOUR" -lt 18 ]; then
    GREETING="Selamat sore indonesia"
else
    GREETING="Selamat malam indonesia"
fi

# Pesan commit
COMMIT_MSG="$GREETING (Jam: $TIME, Tanggal: $DATE)"

# Tambahkan dummy file agar selalu ada perubahan jika tidak ada file lain yang diubah
echo "Terakhir dijalankan: $DATE $TIME" > commit_log.txt

# Proses Git Add dan Commit
git add .
git commit -m "$COMMIT_MSG"

echo "✅ Berhasil membuat commit: $COMMIT_MSG"
