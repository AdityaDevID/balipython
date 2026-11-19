"""Transliterasi Latin -> Aksara Bali (Unicode blok U+1B00-U+1B7F).

Aturan singkat (ejaan Bali):
  a  = aksara dasar (vokal bawaan)   i = ulu     u = suku
  e  = pepet (ə)                     é = taling  o = taling + tedung
  -ng akhir/sebelum konsonan = cecek, -r = surang, -h = bisah
  konsonan akhir = adeg-adeg, gugus konsonan = adeg-adeg (font bikin gantungan)
  vokal ketemu vokal: i/é + vokal -> ya penyambung, u/o + vokal -> wa penyambung
"""
import re
import unicodedata

_VOKAL = set("aiueéo")


def _c(nama: str) -> str:
    return unicodedata.lookup("BALINESE " + nama)


KONSONAN = {
    "k": _c("LETTER KA"), "g": _c("LETTER GA"), "ng": _c("LETTER NGA"),
    "c": _c("LETTER CA"), "j": _c("LETTER JA"), "ny": _c("LETTER NYA"),
    "t": _c("LETTER TA"), "d": _c("LETTER DA"), "n": _c("LETTER NA"),
    "p": _c("LETTER PA"), "b": _c("LETTER BA"), "m": _c("LETTER MA"),
    "y": _c("LETTER YA"), "r": _c("LETTER RA"), "l": _c("LETTER LA"),
    "w": _c("LETTER WA"), "s": _c("LETTER SA"), "h": _c("LETTER HA"),
}
VOKAL_MANDIRI = {
    "a": _c("LETTER AKARA"), "i": _c("LETTER IKARA"), "u": _c("LETTER UKARA"),
    "é": _c("LETTER EKARA"), "o": _c("LETTER OKARA"),
    "e": _c("LETTER AKARA") + _c("VOWEL SIGN PEPET"),
}
TANDA_VOKAL = {
    "a": "", "i": _c("VOWEL SIGN ULU"), "u": _c("VOWEL SIGN SUKU"),
    "e": _c("VOWEL SIGN PEPET"), "é": _c("VOWEL SIGN TALING"),
    "o": _c("VOWEL SIGN TALING TEDUNG"),
}
ADEG = _c("ADEG ADEG")
CODA_KHUSUS = {"ng": _c("SIGN CECEK"), "r": _c("SIGN SURANG"), "h": _c("SIGN BISAH")}


def _token(kata: str):
    t, i = [], 0
    while i < len(kata):
        ch = kata[i]
        if ch in _VOKAL:
            t.append(("V", ch)); i += 1
        elif kata[i:i + 2] in ("ng", "ny"):
            t.append(("C", kata[i:i + 2])); i += 2
        elif ch in KONSONAN:
            t.append(("C", ch)); i += 1
        else:
            raise ValueError(f"huruf '{ch}' belum didukung transliterasi")
    return t


def ke_aksara_kata(kata: str) -> str:
    kata = unicodedata.normalize("NFC", kata.lower())
    tok, out, i = _token(kata), [], 0
    while i < len(tok):
        jenis, nilai = tok[i]
        if jenis == "V":
            sebelum = tok[i - 1][1] if i > 0 else None
            if sebelum in ("i", "é"):        # hiatus i/é + vokal -> ya penyambung
                out.append(KONSONAN["y"] + TANDA_VOKAL[nilai])
            elif sebelum in ("u", "o"):      # hiatus u/o + vokal -> wa penyambung
                out.append(KONSONAN["w"] + TANDA_VOKAL[nilai])
            else:                            # awal kata -> vokal mandiri
                out.append(VOKAL_MANDIRI[nilai])
            i += 1
            continue
        j = i
        while j < len(tok) and tok[j][0] == "C":
            j += 1
        gugus = [x[1] for x in tok[i:j]]
        ada_vokal = j < len(tok)
        sebelumnya_vokal = i > 0 and tok[i - 1][0] == "V"
        if (sebelumnya_vokal and gugus[0] in CODA_KHUSUS
                and (len(gugus) >= 2 or not ada_vokal)):
            out.append(CODA_KHUSUS[gugus[0]])
            gugus = gugus[1:]
        if gugus:
            out.append(ADEG.join(KONSONAN[g] for g in gugus))
            if ada_vokal:
                out.append(TANDA_VOKAL[tok[j][1]])
            else:
                out.append(ADEG)
        i = j + 1 if ada_vokal else j
    return "".join(out)


def ke_aksara(teks: str) -> str:
    """Transliterasi teks Latin (spasi & tanda baca dibiarkan) ke Aksara Bali."""
    return re.sub(r"[A-Za-zéÉ]+", lambda m: ke_aksara_kata(m.group(0)), teks)
