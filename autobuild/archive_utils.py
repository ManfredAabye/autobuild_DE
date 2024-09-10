import multiprocessing
import tarfile
import zipfile
from typing import Union

class ArchiveType:
    GZ = "gz"  # GZIP-Archivtyp
    BZ2 = "bz2"  # BZIP2-Archivtyp
    ZIP = "zip"  # ZIP-Archivtyp
    ZST = "zst"  # Zstandard-Archivtyp

# Dateisignaturen zur Erkennung des Archivtyps
# Weitere Informationen: https://www.garykessler.net/library/file_sigs.html
_ARCHIVE_MAGIC_NUMBERS = {
    b"\x1f\x8b\x08": ArchiveType.GZ,  # GZIP-Dateisignatur
    b"\x42\x5a\x68": ArchiveType.BZ2,  # BZIP2-Dateisignatur
    b"\x50\x4b\x03\x04": ArchiveType.ZIP,  # ZIP-Dateisignatur
    b"\x28\xb5\x2f\xfd": ArchiveType.ZST,  # Zstandard-Dateisignatur
}

# Maximale Länge der Signaturen für den Vergleich
_ARCHIVE_MAGIC_NUMBERS_MAX = max(len(x) for x in _ARCHIVE_MAGIC_NUMBERS)

def _archive_type_from_signature(filename: str):
    """Erkennt den Archivtyp anhand der Dateisignatur."""
    with open(filename, "rb") as f:
        # Liest den Anfang der Datei ein, um die Signatur zu prüfen
        head = f.read(_ARCHIVE_MAGIC_NUMBERS_MAX)
        for magic, f_type in _ARCHIVE_MAGIC_NUMBERS.items():
            if head.startswith(magic):  # Vergleicht mit bekannten Signaturen
                return f_type
    return None  # Gibt None zurück, wenn keine Signatur übereinstimmt

def _archive_type_from_extension(filename: str):
    """Erkennt den Archivtyp anhand der Dateiendung."""
    if filename.endswith(".tar.gz"):  # Überprüfung auf GZIP
        return ArchiveType.GZ
    if filename.endswith(".tar.bz2"):  # Überprüfung auf BZIP2
        return ArchiveType.BZ2
    if filename.endswith(".tar.zst"):  # Überprüfung auf Zstandard
        return ArchiveType.ZST
    if filename.endswith(".zip"):  # Überprüfung auf ZIP
        return ArchiveType.ZIP
    return None

def detect_archive_type(filename: str):
    """Bestimmt den Archivtyp durch Überprüfung der Dateiendung und Signatur."""
    f_type = _archive_type_from_extension(filename)
    if f_type:  # Wenn der Typ durch die Endung erkannt wurde
        return f_type
    return _archive_type_from_signature(filename)  # Ansonsten Signatur prüfen

def open_archive(filename: str) -> Union[tarfile.TarFile, zipfile.ZipFile]:
    """Öffnet ein Archiv abhängig vom erkannten Typ."""
    f_type = detect_archive_type(filename)

    if f_type == ArchiveType.ZST:  # Öffnet ein Zstandard-Archiv
        return ZstdTarFile(filename, "r")

    if f_type == ArchiveType.ZIP:  # Öffnet ein ZIP-Archiv
        return zipfile.ZipFile(filename, "r")

    return tarfile.open(filename, "r")  # Öffnet ein TAR-Archiv

class ZstdTarFile(tarfile.TarFile):
    """Spezialisiert für den Umgang mit Zstandard-komprimierten TAR-Dateien."""
    def __init__(self, name, mode='r', *, level=4, zstd_dict=None, **kwargs):
        from pyzstd import CParameter, ZstdFile  # Importiert Zstandard-Parameter und -Dateien
        zstdoption = None
        if mode != 'r' and mode != 'rb':
            # Setzt Zstandard-Komprimierungsoptionen
            zstdoption = {CParameter.compressionLevel: level,
                          CParameter.nbWorkers: multiprocessing.cpu_count(),
                          CParameter.checksumFlag: 1}
        # Öffnet die Zstandard-Datei
        self.zstd_file = ZstdFile(name, mode,
                                  level_or_option=zstdoption,
                                  zstd_dict=zstd_dict)
        try:
            # Initialisiert das TAR-Archiv mit der Zstandard-Datei als Quelle
            super().__init__(fileobj=self.zstd_file, mode=mode, **kwargs)
        except:
            self.zstd_file.close()  # Schließt die Datei bei Fehlern
            raise

    def close(self):
        """Schließt sowohl das TAR-Archiv als auch die Zstandard-Datei."""
        try:
            super().close()
        finally:
            self.zstd_file.close()
