"""Command line: `balipy tes.bali` (alias: `bpy`)"""
import argparse
import sys

from . import __version__
from .aksara import ke_aksara
from .core import REPL, aksarakan, jalankan, terjemahkan


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="balipy", description="BaliPython - Python dengan Aksara Bali")
    p.add_argument("file", nargs="?", help="file .bali yang mau dijalankan")
    p.add_argument("-c", dest="perintah", help="jalankan kode langsung dari argumen")
    p.add_argument("--latin", action="store_true",
                   help="mode Latin: keyword ditulis pakai huruf Latin (tanpa keyboard Aksara)")
    p.add_argument("--lihat", action="store_true", help="tampilkan hasil terjemahan ke Python")
    p.add_argument("--aksarakan", action="store_true",
                   help="ubah file mode Latin jadi kode Aksara Bali, lalu cetak")
    p.add_argument("--aksara", metavar="TEKS", help="transliterasi teks Latin ke Aksara Bali")
    p.add_argument("--versi", action="version", version=f"BaliPython {__version__}")
    a = p.parse_args(argv)

    if a.aksara is not None:
        try:
            print(ke_aksara(a.aksara))
            return 0
        except ValueError as e:
            print(f"[BaliPython] {e}", file=sys.stderr)
            return 1

    if a.perintah is not None:
        sumber, nama = a.perintah, "<-c>"
    elif a.file:
        try:
            with open(a.file, encoding="utf-8") as f:
                sumber, nama = f.read(), a.file
        except FileNotFoundError:
            print(f"[BaliPython] File nenten panggihin: {a.file}", file=sys.stderr)
            return 1
    else:
        banner = (f"BaliPython {__version__} (Python {sys.version.split()[0]})"
                  f"{' [mode Latin]' if a.latin else ''}\n"
                  "Ketik medal() atau Ctrl+D untuk keluar.")
        REPL(a.latin).interact(banner=banner, exitmsg="Suksma!")
        return 0

    if a.aksarakan:
        print(aksarakan(sumber), end="")
        return 0
    if a.lihat:
        print(terjemahkan(sumber, a.latin), end="")
        return 0
    return jalankan(sumber, nama, latin=a.latin)


if __name__ == "__main__":
    sys.exit(main())
