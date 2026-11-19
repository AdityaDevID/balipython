import subprocess
import sys
from pathlib import Path

import pytest

from balipy import (FUNGSI_LATIN, KATA_KUNCI_LATIN, aksarakan, buat_namespace,
                    jalankan, ke_aksara, terjemahkan)
from balipy.core import FUNGSI_AKSARA, KATA_KUNCI

ROOT = Path(__file__).resolve().parent.parent
EX = ROOT / "examples"


def test_transliterasi_dasar():
    assert ke_aksara("yen") == "\u1b2c\u1b42\u1b26\u1b44"            # ya + pepet + na + adeg
    assert ke_aksara("tulis") == "\u1b22\u1b38\u1b2e\u1b36\u1b32\u1b44"
    assert ke_aksara("ring") == "\u1b2d\u1b36\u1b02"                  # ra + ulu + cecek
    assert ke_aksara("sareng") == "\u1b32\u1b2d\u1b42\u1b02"
    assert ke_aksara("gawé") == "\u1b15\u1b2f\u1b3e"                  # ga + wa + taling


def test_hiatus_pakai_ya_wa():
    assert ke_aksara("lian") == ke_aksara("liyan")
    assert ke_aksara("buan") == ke_aksara("buwan")


def test_huruf_tidak_didukung():
    with pytest.raises(ValueError):
        ke_aksara("qa")


def test_tidak_ada_tabrakan():
    assert len(KATA_KUNCI) == len(KATA_KUNCI_LATIN)
    assert len(FUNGSI_AKSARA) == len(FUNGSI_LATIN)
    assert not set(KATA_KUNCI) & set(FUNGSI_AKSARA)


def test_keyword_aksara():
    src = f"{ke_aksara('yen')} {ke_aksara('patut')}:\n    {ke_aksara('liwat')}\n"
    assert terjemahkan(src) == "if True:\n    pass\n"


def test_string_dan_komentar_aman():
    src = f'x = "{ke_aksara("yen")}"  # {ke_aksara("yen")}\n'
    assert terjemahkan(src) == src


def test_atribut_tidak_diganti():
    src = f"obj.{ke_aksara('yen')}\n"
    assert terjemahkan(src) == src


def test_kolom_benar_setelah_string_aksara():
    src = f'x = "{ke_aksara("tulis")}"; {ke_aksara("yen")} x:\n    {ke_aksara("liwat")}\n'
    assert terjemahkan(src).endswith("; if x:\n    pass\n")


def test_nomor_baris_tetap():
    src = f"{ke_aksara('gawé')} f():\n    {ke_aksara('baliang')} 1\n\nf()\n"
    assert terjemahkan(src).count("\n") == src.count("\n")


def test_mode_latin_aksen_opsional():
    assert terjemahkan("gawe f():\n    baliang 1\n", latin=True) == "def f():\n    return 1\n"
    assert terjemahkan("gawé f():\n    baliang 1\n", latin=True) == "def f():\n    return 1\n"


def test_jalankan_aksara(capsys):
    kode = f"{ke_aksara('tulis')}('hai', {ke_aksara('dawa')}('abc'))"
    assert jalankan(kode, ns=buat_namespace()) == 0
    assert capsys.readouterr().out == "hai 3\n"


def test_sintaks_salah():
    assert jalankan("yen Patut tulis(1)", latin=True) == 1


def _run(*args):
    return subprocess.run([sys.executable, "-m", "balipy", *args],
                          capture_output=True, text=True, encoding="utf-8")


@pytest.mark.parametrize("nama", ["fizzbuzz.bali", "sato.bali", "dasar.bali"])
def test_contoh_latin_sama_dengan_aksara(nama):
    latin = _run("--latin", str(EX / "latin" / nama))
    aksara = _run(str(EX / "aksara" / nama))
    assert latin.returncode == aksara.returncode == 0
    assert latin.stdout == aksara.stdout and latin.stdout


def test_contoh_aksara_halo():
    out = _run(str(EX / "aksara" / "halo.bali"))
    assert out.returncode == 0 and "Om Swastyastu" in out.stdout


def test_aksarakan_cli():
    out = _run("--aksarakan", str(EX / "latin" / "fizzbuzz.bali"))
    assert ke_aksara("yenlian") in out.stdout and "ring" not in out.stdout


def test_flag_aksara():
    assert _run("--aksara", "yen").stdout.strip() == ke_aksara("yen")
