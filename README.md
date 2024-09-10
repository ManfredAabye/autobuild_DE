# Autobuild

[![codecov](https://codecov.io/gh/secondlife/autobuild/branch/main/graph/badge.svg?token=8GBLMAFDIN)](https://codecov.io/gh/secondlife/autobuild)

**Autobuild** ist ein Framework zum Erstellen von Paketen und zum Verwalten der
Abhängigkeiten eines Pakets von anderen Paketen. Es bietet eine gemeinsame
Schnittstelle zum Konfigurieren und Erstellen beliebiger Pakete, ist aber kein
Build-System wie make oder cmake. Sie benötigen weiterhin plattformspezifische
make-, cmake- oder Projektdateien zum Konfigurieren und Erstellen Ihrer
Bibliothek. Mit Autobuild können Sie diese Befehle jedoch aufrufen und
das Produkt mit einer gemeinsamen Schnittstelle verpacken.

*Wichtig: Linden Lab Autobuild ist nicht dasselbe wie GNU
Autobuild oder davon abgeleitet, aber sie sind ähnlich genug, um Verwirrung zu stiften.*

Weitere Informationen finden Sie auf der [Wiki-Seite von Autobuild][wiki].

[wiki]: https://wiki.secondlife.com/wiki/Autobuild

## Umgebungsvariablen

| Name | Standard | Beschreibung |
|-|-|-|
| AUTOBUILD_ADDRSIZE | 32 | Zieladressgröße |
| AUTOBUILD_BUILD_ID | - | Build-ID |
| AUTOBUILD_CONFIGURATION | - | Ziel-Build-Konfiguration |
| AUTOBUILD_CONFIG_FILE | autobuild.xml | Name der Autobuild-Konfigurationsdatei |
| AUTOBUILD_CPU_COUNT | - | Anzahl der CPU-Kerne des Build-Systems |
| AUTOBUILD_GITHUB_TOKEN | - | GitHub HTTP-Autorisierungstoken zur Verwendung während des Paketdownloads |
| AUTOBUILD_GITLAB_TOKEN | - | GitLab HTTP-Autorisierungstoken zur Verwendung während des Paketdownloads |
| AUTOBUILD_INSTALLABLE_CACHE | - | Speicherort des lokalen Download-Cache |
| AUTOBUILD_LOGLEVEL | WARNING | Protokollebene |
| AUTOBUILD_PLATFORM | - | Zielplattform |
| AUTOBUILD_SCM_SEARCH | true | Ob bei Verwendung der SCM-Versionserkennung in übergeordneten Verzeichnissen nach .git gesucht werden soll |
| AUTOBUILD_VARIABLES_FILE | - | Zu ladende .env-Datei |
| AUTOBUILD_VCS_BRANCH | git branch | autobuild-package.xml VCS-Info: Zweigname. |
| AUTOBUILD_VCS_INFO | false | Ob Versionskontrollinformationen in autobuild-package.xml aufgenommen werden sollen |
| AUTOBUILD_VCS_REVISION | git commit | autobuild-package.xml VCS-Commit-Referenz, die in autobuild-package.xml aufgenommen werden soll. Standardmäßig aktuelles Git-Commit-Sha. |
| AUTOBUILD_VCS_URL | git remote url | autobuild-package.xml VCS-Info: Repository-URL |
| AUTOBUILD_VSVER | - | Unter Windows zu verwendende Zielversion von Visual Studio |
