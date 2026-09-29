# CLAUDE.md

## Proje özeti

Bu repo bir Claude skill'idir: **idea-worth-building**. Bir ürün/girişim fikrinin kodlamaya
değip değmediğini araştırma, puanlama ve birim ekonomisiyle değerlendirir.

- Skill klasörü: `idea-worth-building/` (`SKILL.md`, `references/`, `scripts/`)
- Örnek girdiler: `examples/`
- Script'ler yalnızca **Python 3 standart kütüphanesini** kullanır; harici bağımlılık eklemeyin.

## Kurallar

- `idea-worth-building/SKILL.md` frontmatter'ında yalnızca `name` ve `description` bulunur.
  `description` 1024 karakteri geçmemelidir.
- `references/scoring-rubric.md` içindeki "Goal profiles" ağırlık tablosu ile
  `scripts/score.py` içindeki `PROFILES` her zaman aynı olmalıdır (her profil toplamı 100).
- `references/report-template.md` içindeki bölüm numaraları değişirse
  `scripts/check_report.py` de güncellenmelidir (beklenen bölüm aralığı ve bölüme özel kontroller).
- `README.md`'nin İngilizce bölümleri ile `## Türkçe` bölümü her zaman birlikte güncellenir.

## Test komutları

`idea-worth-building/` klasöründen çalıştırın:

```bash
python3 scripts/score.py ../examples/scores.example.json --profile commercial --lang en
# Beklenen: Total 55.0/100, Verdict: PIVOT

python3 scripts/unit_economics.py ../examples/unit-economics.example.json --lang en
# Beklenen: hatasız çalışır (exit 0)
```

## Release kontrol listesi

1. `CHANGELOG.md`'yi güncelle.
2. Commit.
3. Push (`git push origin main`).
4. GitHub'da release oluştur (tag `vX.Y.Z`) ve yayınla.
5. `.github/workflows/release.yml` çalıştıktan sonra `idea-worth-building.zip`'in release'e
   otomatik eklendiğini kontrol et.
