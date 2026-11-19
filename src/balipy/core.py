"""Inti BaliPython: terjemah keyword Aksara Bali (atau Latin) -> Python."""
import builtins
import code
import io
import sys
import tokenize
import traceback
import unicodedata

from .aksara import ke_aksara

# --- Kata kunci: Latin -> Python (sumber kebenaran; Aksara dibuat otomatis) ---
KATA_KUNCI_LATIN = {
    "yen": "if", "yenlian": "elif", "lian": "else",
    "ulang": "for", "salami": "while", "ring": "in",
    "gawé": "def", "baliang": "return", "pikolih": "yield",
    "soroh": "class", "tanadan": "lambda",
    "Patut": "True", "Iwang": "False", "Suung": "None",
    "miwah": "and", "utawi": "or", "tan": "not", "punika": "is",
    "cobak": "try", "tangkep": "except", "wekasan": "finally",
    "uncalang": "raise", "tegesang": "assert",
    "bakta": "import", "saking": "from", "pinaka": "as", "sareng": "with",
    "liwat": "pass", "pegat": "break", "lanturang": "continue",
    "ilangang": "del", "jagat": "global",
}

# --- Fungsi bawaan: Latin -> nama builtin Python ---
FUNGSI_LATIN = {
    "tulis": "print", "takén": "input", "jangka": "range", "dawa": "len",
    "wangun": "type", "cacah": "int", "pecahan": "float", "aksara": "str",
    "baris": "list", "kamus": "dict", "wadah": "set",
    "urutang": "sorted", "balikang": "reversed", "jumlah": "sum",
    "pinihageng": "max", "pinihalit": "min", "mutlak": "abs",
    "buletang": "round", "buka": "open", "itungang": "enumerate",
    "gabung": "zip", "ubah": "map", "saring": "filter",
    "sami": "all", "wenten": "any", "tulung": "help", "medal": "exit",
}


def _nfkc(s: str) -> str:
    return unicodedata.normalize("NFKC", s)


def _tanpa_aksen(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def _builtin(nama: str):
    return sys.exit if nama == "exit" else getattr(builtins, nama)


# Tabel Aksara (kunci dinormalisasi NFKC, sama seperti Python menormalkan identifier)
KATA_KUNCI = {_nfkc(ke_aksara(k)): v for k, v in KATA_KUNCI_LATIN.items()}
FUNGSI_AKSARA = {_nfkc(ke_aksara(k)): _builtin(v) for k, v in FUNGSI_LATIN.items()}

# Tabel Latin (aksen opsional: "gae" = "gaé")
_KUNCI_LATIN = {_tanpa_aksen(k): v for k, v in KATA_KUNCI_LATIN.items()}
FUNGSI_LATIN_NS = {}
for _k, _v in FUNGSI_LATIN.items():
    FUNGSI_LATIN_NS[_k] = FUNGSI_LATIN_NS[_tanpa_aksen(_k)] = _builtin(_v)

# Untuk konversi Latin -> Aksara (kode)
_LATIN_KE_AKSARA = {_tanpa_aksen(k): ke_aksara(k)
                    for k in (*KATA_KUNCI_LATIN, *FUNGSI_LATIN)}


_NAMA_LATIN = {_tanpa_aksen(k) for k in (*KATA_KUNCI_LATIN, *FUNGSI_LATIN)}


def _ganti(sumber: str, peta: dict, norm) -> str:
    """Ganti token NAME yang ada di `peta` (nomor baris tetap sama)."""
    ditambah = not sumber.endswith("\n")
    if ditambah:
        sumber += "\n"
    baris = sumber.splitlines(keepends=True)
    ganti, sebelumnya = [], None
    for tok in tokenize.generate_tokens(io.StringIO(sumber).readline):
        if tok.type == tokenize.NAME:
            baru = peta.get(norm(tok.string))
            if baru is not None and not (sebelumnya is not None and sebelumnya.string == "."):
                (r, c1), (_, c2) = tok.start, tok.end
                ganti.append((r, c1, c2, baru))
        if tok.type not in (tokenize.NL, tokenize.COMMENT):
            sebelumnya = tok
    for r, c1, c2, baru in reversed(ganti):
        b = baris[r - 1]
        baris[r - 1] = b[:c1] + baru + b[c2:]
    hasil = "".join(baris)
    return hasil[:-1] if ditambah else hasil


def terjemahkan(sumber: str, latin: bool = False) -> str:
    """Ubah kode BaliPython jadi kode Python biasa."""
    if latin:
        return _ganti(sumber, _KUNCI_LATIN, _tanpa_aksen)
    return _ganti(sumber, KATA_KUNCI, _nfkc)


def aksarakan(sumber: str) -> str:
    """Ubah kode mode Latin jadi kode Aksara Bali (hanya keyword & fungsi bawaan)."""
    return _ganti(sumber, _LATIN_KE_AKSARA, _tanpa_aksen)


def buat_namespace(latin: bool = False) -> dict:
    ns = {"__name__": "__main__", "__builtins__": builtins}
    ns.update(FUNGSI_LATIN_NS if latin else FUNGSI_AKSARA)
    return ns


def jalankan(sumber: str, nama_file: str = "<balipy>", ns: dict | None = None,
             latin: bool = False) -> int:
    ns = ns if ns is not None else buat_namespace(latin)
    try:
        objek = compile(terjemahkan(sumber, latin), nama_file, "exec")
        exec(objek, ns)
    except BrokenPipeError:
        return 0
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 0
    except (SyntaxError, tokenize.TokenError) as e:
        print(f"[BaliPython] Iwang sintaks: {e}", file=sys.stderr)
        if not latin:
            print("Petunjuk: kalau kodenya ditulis pakai huruf Latin, jalankan dengan --latin",
                  file=sys.stderr)
        return 1
    except Exception as e:
        print("[BaliPython] Wénten iwang:", file=sys.stderr)
        traceback.print_exc()
        nama = getattr(e, "name", None)
        if isinstance(e, NameError) and not latin and nama and \
                _tanpa_aksen(nama) in _NAMA_LATIN:
            print("Petunjuk: kode ini kelihatannya ditulis pakai huruf Latin, "
                  "jalankan dengan --latin", file=sys.stderr)
        return 1
    return 0


class REPL(code.InteractiveConsole):
    def __init__(self, latin: bool = False):
        super().__init__(locals=buat_namespace(latin), filename="<balipy>")
        self.latin = latin

    def runsource(self, source, filename="<balipy>", symbol="single"):
        try:
            py = terjemahkan(source, self.latin)
        except (tokenize.TokenError, IndentationError):
            return True  # blok belum selesai
        return super().runsource(py, filename, symbol)
