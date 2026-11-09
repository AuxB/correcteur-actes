#!/usr/bin/env python3
"""Range dans le projet les XML corrigés sur l'iPhone.

Usage, depuis le dossier du projet (actes) :
    python3 correcteur/integrer_corrections.py ~/Downloads/corrections_2026-11-09_18h30.zip
    python3 correcteur/integrer_corrections.py archive.zip --essai      # montre ce qui serait fait

Chaque XML de l'archive remplace le fichier du même chemin dans le dossier de destination
(ou, à défaut, l'unique fichier du même nom trouvé dans ses sous-dossiers). Les fichiers
remplacés sont d'abord copiés dans _sauvegardes_corrections/<date>/.
"""
import argparse
import datetime
import pathlib
import shutil
import sys
import unicodedata
import zipfile

SAUVEGARDES = '_sauvegardes_corrections'


def nfc(texte):
    return unicodedata.normalize('NFC', texte)


def main():
    parseur = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parseur.add_argument('archive', help='fichier zip exporté par le Correcteur')
    parseur.add_argument('--dossier', default='.', help='dossier de destination (par défaut le dossier courant)')
    parseur.add_argument('--essai', action='store_true', help="affiche ce qui serait fait sans rien modifier")
    args = parseur.parse_args()

    dest = pathlib.Path(args.dossier).expanduser().resolve()
    horodatage = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%M%S')
    dossier_sauvegarde = dest / SAUVEGARDES / horodatage

    index = {}
    for f in dest.rglob('*.xml'):
        if SAUVEGARDES in f.parts:
            continue
        index.setdefault(nfc(f.name), []).append(f)

    remplaces, ajoutes, ignores = 0, 0, []
    with zipfile.ZipFile(pathlib.Path(args.archive).expanduser()) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            nom = nfc(info.filename)
            rel = pathlib.PurePosixPath(nom)
            if rel.is_absolute() or '..' in rel.parts:
                ignores.append(f'{nom} (chemin refusé)')
                continue
            if rel.name == 'etat_correction.json':
                cible = dossier_sauvegarde / 'etat_correction.json'
                if not args.essai:
                    cible.parent.mkdir(parents=True, exist_ok=True)
                    cible.write_bytes(z.read(info))
                continue
            if rel.suffix.lower() != '.xml':
                continue

            cible = dest.joinpath(*rel.parts)
            if not cible.exists():
                candidats = index.get(rel.name, [])
                if len(candidats) == 1:
                    cible = candidats[0]
                elif len(candidats) > 1:
                    ignores.append(f'{nom} (plusieurs fichiers de ce nom : '
                                   + ', '.join(str(c.relative_to(dest)) for c in candidats) + ')')
                    continue

            if cible.exists():
                print(f'remplace  {cible.relative_to(dest)}')
                remplaces += 1
                if not args.essai:
                    copie = dossier_sauvegarde / cible.relative_to(dest)
                    copie.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(cible, copie)
            else:
                print(f'ajoute    {cible.relative_to(dest)}')
                ajoutes += 1
            if not args.essai:
                cible.parent.mkdir(parents=True, exist_ok=True)
                cible.write_bytes(z.read(info))

    print(f'\n{remplaces} fichier(s) remplacé(s), {ajoutes} ajouté(s), {len(ignores)} ignoré(s).')
    for i in ignores:
        print('  ignoré :', i)
    if args.essai:
        print('Mode essai, rien n\'a été modifié.')
    elif remplaces:
        print(f'Anciennes versions copiées dans {dossier_sauvegarde.relative_to(dest)}')
    return 1 if ignores else 0


if __name__ == '__main__':
    sys.exit(main())
