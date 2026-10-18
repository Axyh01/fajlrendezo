import argparse
import shutil
from datetime import datetime
from pathlib import Path

NAPLO = Path(__file__).parent / "naplo.txt"

KATEGORIAK = {
    "Kepek": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Dokumentumok": [".pdf", ".docx", ".txt", ".odt", ".xlsx", ".pptx"],
    "Telepitok": [".deb", ".appimage", ".sh"],
    "Tomoritett": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Zene_Video": [".mp3", ".wav", ".mp4", ".mkv"],
}


def kategoria_keres(fajl):
    kiterjesztes = fajl.suffix.lower()
    for nev, lista in KATEGORIAK.items():
        if kiterjesztes in lista:
            return nev
    return "Egyeb"


def naploz(uzenet):
    ido = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(NAPLO, "a", encoding="utf-8") as f:
        f.write(f"{ido}  {uzenet}\n")


def rendez(mappa, eles):
    for elem in mappa.iterdir():
        if not elem.is_file():
            continue

        cel_mappa = mappa / kategoria_keres(elem)
        cel_fajl = cel_mappa / elem.name

        if eles:
            cel_mappa.mkdir(exist_ok=True)
            if cel_fajl.exists():
                print(f"KIHAGYVA (már létezik): {elem.name}")
                continue
            shutil.move(str(elem), str(cel_fajl))
            naploz(f"{elem.name}  ->  {cel_mappa.name}")

        print(f"{elem.name}  ->  {cel_mappa.name}")


def main():
    parser = argparse.ArgumentParser(description="Fájlok rendezése kategóriák szerint.")
    parser.add_argument(
        "mappa",
        nargs="?",
        type=Path,
        default=Path.home() / "Letöltések",
        help="a rendezendő mappa (alapértelmezett: Letöltések)",
    )
    parser.add_argument(
        "--eles",
        action="store_true",
        help="tényleg mozgat (nélküle csak próbafuttatás)",
    )
    args = parser.parse_args()

    mappa = args.mappa.expanduser()
    if not mappa.is_dir():
        print(f"Hiba: nem létező mappa: {mappa}")
        return

    if not args.eles:
        print("PRÓBAFUTTATÁS (semmi nem mozog). Éles módhoz: --eles\n")

    rendez(mappa, args.eles)


main()
