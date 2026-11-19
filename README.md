# BaliPython ᬩᬮᬶ

Python dengan **Aksara Bali**. Keyword ditulis pakai Aksara Bali (kata-katanya Basa Bali), semua fitur dan library Python tetap jalan.

```
ᬕᬯᬾ sapa(adan):
    ᬬᭂᬦ᭄ adan == "Wayan":
        ᬢᬸᬮᬶᬲ᭄("Om Swastyastu, Wayan!")
    ᬮᬶᬬᬦ᭄:
        ᬢᬸᬮᬶᬲ᭄("Halo,", adan)

ᬉᬮᬂ i ᬭᬶᬂ ᬚᬂᬓ(3):
    sapa("Dunia")
```

Kode di atas sama dengan versi Latin-nya:

```
gawe sapa(adan):
    yen adan == "Wayan":
        tulis("Om Swastyastu, Wayan!")
    lian:
        tulis("Halo,", adan)

ulang i ring jangka(3):
    sapa("Dunia")
```

## Instalasi

Butuh Python 3.10+. Nggak ada dependensi lain.

```bash
git clone https://github.com/AdityaDevID/balipython
cd balipython
pip install .
```

Atau langsung dari GitHub:

```bash
pip install git+https://github.com/AdityaDevID/balipython
```

## Cara pakai

```bash
balipy tes.bali                    # jalanin file Aksara (alias: bpy)
balipy                             # REPL interaktif
balipy -c 'tulis("hai")' --latin   # 1 baris, mode Latin
balipy --latin tes.bali            # jalanin file yang keyword-nya ditulis Latin
balipy --aksarakan tes.bali        # ubah file mode Latin jadi kode Aksara Bali
balipy --aksara "rahayu"           # transliterasi teks Latin ke Aksara Bali
balipy --lihat tes.bali            # lihat hasil terjemahan ke Python
```

### Belum punya keyboard Aksara Bali?

Ada dua jalan:

1. **Tulis pakai Latin**, jalanin dengan `--latin`. Aksen `é` boleh dihilangkan (`gawe` = `gawé`).
2. Kalau mau hasil akhirnya Aksara: tulis Latin dulu, lalu ubah otomatis dengan `balipy --aksarakan`.

Buat *melihat* Aksara Bali, editor/terminal kamu butuh font yang mendukung blok Unicode Balinese (U+1B00 sampai U+1B7F), misalnya **Noto Sans Balinese**. Kalau kotak-kotak, itu cuma soal font, kodenya tetap jalan.

Contoh lengkap ada di `examples/latin/` dan `examples/aksara/` (isinya sama).

## Cara kerja

Transpiler ringan. Kode dibaca pakai modul `tokenize` bawaan Python, token keyword Aksara Bali diganti ke keyword Python (string, komentar, dan atribut seperti `obj.ring` nggak ikut diganti), lalu dijalankan dengan `exec`. Python memang menerima huruf Aksara Bali sebagai nama variabel, jadi kamu juga bebas bikin nama fungsi dan variabel dalam Aksara. Nomor baris tetap sama, jadi pesan error menunjuk baris yang benar.

Tabel di bawah ditulis dalam Latin di `src/balipy/core.py` lalu diubah ke Aksara otomatis oleh `src/balipy/aksara.py`, jadi nambah kata cukup edit satu baris.

## Kata kunci

| Aksara Bali | Latin | Python |
|---|---|---|
| ᬬᭂᬦ᭄ | `yen` | `if` |
| ᬬᭂᬦ᭄ᬮᬶᬬᬦ᭄ | `yenlian` | `elif` |
| ᬮᬶᬬᬦ᭄ | `lian` | `else` |
| ᬉᬮᬂ | `ulang` | `for` |
| ᬲᬮᬫᬶ | `salami` | `while` |
| ᬭᬶᬂ | `ring` | `in` |
| ᬕᬯᬾ | `gawé` | `def` |
| ᬩᬮᬶᬬᬂ | `baliang` | `return` |
| ᬧᬶᬓᭀᬮᬶᬄ | `pikolih` | `yield` |
| ᬲᭀᬭᭀᬄ | `soroh` | `class` |
| ᬢᬦᬤᬦ᭄ | `tanadan` | `lambda` |
| ᬧᬢᬸᬢ᭄ | `Patut` | `True` |
| ᬇᬯᬂ | `Iwang` | `False` |
| ᬲᬸᬯᬸᬂ | `Suung` | `None` |
| ᬫᬶᬯᬄ | `miwah` | `and` |
| ᬉᬢᬯᬶ | `utawi` | `or` |
| ᬢᬦ᭄ | `tan` | `not` |
| ᬧᬸᬦᬶᬓ | `punika` | `is` |
| ᬘᭀᬩᬓ᭄ | `cobak` | `try` |
| ᬢᬂᬓᭂᬧ᭄ | `tangkep` | `except` |
| ᬯᭂᬓᬲᬦ᭄ | `wekasan` | `finally` |
| ᬉᬦ᭄ᬘᬮᬂ | `uncalang` | `raise` |
| ᬢᭂᬕᭂᬲᬂ | `tegesang` | `assert` |
| ᬩᬓ᭄ᬢ | `bakta` | `import` |
| ᬲᬓᬶᬂ | `saking` | `from` |
| ᬧᬶᬦᬓ | `pinaka` | `as` |
| ᬲᬭᭂᬂ | `sareng` | `with` |
| ᬮᬶᬯᬢ᭄ | `liwat` | `pass` |
| ᬧᭂᬕᬢ᭄ | `pegat` | `break` |
| ᬮᬦ᭄ᬢᬸᬭᬂ | `lanturang` | `continue` |
| ᬇᬮᬗᬂ | `ilangang` | `del` |
| ᬚᬕᬢ᭄ | `jagat` | `global` |

## Fungsi bawaan

| Aksara Bali | Latin | Python |
|---|---|---|
| ᬢᬸᬮᬶᬲ᭄ | `tulis` | `print` |
| ᬢᬓᬾᬦ᭄ | `takén` | `input` |
| ᬚᬂᬓ | `jangka` | `range` |
| ᬤᬯ | `dawa` | `len` |
| ᬯᬗᬸᬦ᭄ | `wangun` | `type` |
| ᬘᬘᬄ | `cacah` | `int` |
| ᬧᭂᬘᬳᬦ᭄ | `pecahan` | `float` |
| ᬅᬓ᭄ᬲᬭ | `aksara` | `str` |
| ᬩᬭᬶᬲ᭄ | `baris` | `list` |
| ᬓᬫᬸᬲ᭄ | `kamus` | `dict` |
| ᬯᬤᬄ | `wadah` | `set` |
| ᬉᬭᬸᬢᬂ | `urutang` | `sorted` |
| ᬩᬮᬶᬓᬂ | `balikang` | `reversed` |
| ᬚᬸᬫ᭄ᬮᬄ | `jumlah` | `sum` |
| ᬧᬶᬦᬶᬳᬕᭂᬂ | `pinihageng` | `max` |
| ᬧᬶᬦᬶᬳᬮᬶᬢ᭄ | `pinihalit` | `min` |
| ᬫᬸᬢ᭄ᬮᬓ᭄ | `mutlak` | `abs` |
| ᬩᬸᬮᭂᬢᬂ | `buletang` | `round` |
| ᬩᬸᬓ | `buka` | `open` |
| ᬇᬢᬸᬗᬂ | `itungang` | `enumerate` |
| ᬕᬩᬸᬂ | `gabung` | `zip` |
| ᬉᬩᬄ | `ubah` | `map` |
| ᬲᬭᬶᬂ | `saring` | `filter` |
| ᬲᬫᬶ | `sami` | `all` |
| ᬯᭂᬦ᭄ᬢᭂᬦ᭄ | `wenten` | `any` |
| ᬢᬸᬮᬸᬂ | `tulung` | `help` |
| ᬫᭂᬤᬮ᭄ | `medal` | `exit` |

Keyword dan fungsi Python aslinya tetap bisa dipakai (`print`, `if`, dst), jadi boleh dicampur. Di mode `--latin`, kata-kata di atas (mis. `ring`, `lian`, `baris`) jadi kata yang dicadangkan, jangan dipakai sebagai nama variabel.

## Aturan transliterasi

`a` = aksara dasar, `i` = ulu, `u` = suku, `e` = pepet, `é` = taling, `o` = taling + tedung. `ng` di akhir suku kata = cecek, `r` = surang, `h` = bisah. Konsonan penutup dan gugus konsonan pakai adeg-adeg (font yang membentuk gantungan). Dua vokal berurutan disambung `ya` (setelah i/é) atau `wa` (setelah u/o).

## Catatan penting

- Pilihan kata Basa Bali di sini masih **versi awal**. Kalau ada yang kurang pas atau ada padanan yang lebih lazim, PR/issue dari penutur Bali sangat welcome.
- Pesan error dari Python masih berbahasa Inggris.
- Ejaan hasil transliterasi mengikuti aturan umum Aksara Bali dan bisa beda tipis dengan tulisan tangan tradisional. Perbaikan dari yang paham aksara juga welcome.

## Tes

```bash
pip install pytest
pytest
```

## Lisensi

MIT
