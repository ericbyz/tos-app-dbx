#!/usr/bin/env python3
"""Generate dbx.lang for the TOS App Center.

TOS 7.0 baseline ships 14 languages; TOS 7.1 documents a 26-language set.
We generate all 26 so the app displays correctly on both. Sections present
must never have empty name/auth/descript (review rule 8.5) — untranslated
languages are filled with English. Output: UTF-8 without BOM, LF line endings.
"""
import os
import sys

APP_ID = "dbx"
AUTHOR = "ericbyz"
NAME_EN = "DBX"
DESC_EN = ("Lightweight database client for 100+ databases including MySQL, "
           "PostgreSQL, SQLite, Redis and MongoDB. Runs as a web service on "
           "port 4224.")
NOTE_EN = "1. Packaged upstream dbx-web for the TOS App Center."
NOTE_ZH = "1. 将上游 dbx-web 封装为 TOS 应用中心应用。"
IMPORTANT = ""

# (locale, native app name, native description)
LANGS = [
    ("zh-cn",  "DBX 数据库客户端", "轻量级数据库管理客户端，支持 MySQL、PostgreSQL、SQLite、Redis、MongoDB 等 100+ 数据库，安装后通过 4224 端口在浏览器中使用。"),
    ("zh-hk",  "DBX 數據庫客戶端", "輕量級數據庫管理客戶端，支持 MySQL、PostgreSQL、SQLite、Redis、MongoDB 等 100+ 數據庫，安裝後通過 4224 端口在瀏覽器中使用。"),
    ("en-us",  NAME_EN, DESC_EN),
    ("ko-kr",  NAME_EN, "MySQL, PostgreSQL, SQLite, Redis, MongoDB 등 100개 이상의 데이터베이스를 지원하는 경량 데이터베이스 클라이언트입니다. 웹 서비스(포트 4224)로 실행됩니다."),
    ("ja-jp",  NAME_EN, "MySQL、PostgreSQL、SQLite、Redis、MongoDB など 100 以上のデータベースに対応した軽量データベースクライアント。Web サービス（ポート 4224）として動作します。"),
    ("de-de",  NAME_EN, "Leichter Datenbank-Client für über 100 Datenbanken, u. a. MySQL, PostgreSQL, SQLite, Redis und MongoDB. Läuft als Webdienst auf Port 4224."),
    ("fr-fr",  NAME_EN, "Client de base de données léger pour plus de 100 bases de données, dont MySQL, PostgreSQL, SQLite, Redis et MongoDB. Fonctionne en service web sur le port 4224."),
    ("it-it",  NAME_EN, "Client di database leggero per oltre 100 database, tra cui MySQL, PostgreSQL, SQLite, Redis e MongoDB. Funziona come servizio web sulla porta 4224."),
    ("es-es",  NAME_EN, "Cliente de bases de datos ligero para más de 100 bases de datos, incluidas MySQL, PostgreSQL, SQLite, Redis y MongoDB. Se ejecuta como servicio web en el puerto 4224."),
    ("hu-hu",  NAME_EN, "Könnyű adatbázis-kliens több mint 100 adatbázishoz, köztük MySQL, PostgreSQL, SQLite, Redis és MongoDB. Webes szolgáltatásként fut a 4224-es porton."),
    ("pl-pl",  NAME_EN, "Lekki klient baz danych obsługujący ponad 100 baz danych, m.in. MySQL, PostgreSQL, SQLite, Redis i MongoDB. Działa jako usługa internetowa na porcie 4224."),
    ("tr-tr",  NAME_EN, "MySQL, PostgreSQL, SQLite, Redis ve MongoDB dahil 100'den fazla veritabanını destekleyen hafif bir veritabanı istemcisi. 4224 numaralı bağlantı noktasında web servisi olarak çalışır."),
    ("ru-ru",  NAME_EN, "Легковесный клиент баз данных: MySQL, PostgreSQL, SQLite, Redis, MongoDB и более 100 других. Работает как веб-сервис на порту 4224."),
    ("pt-pt",  NAME_EN, "Cliente de bases de dados leve para mais de 100 bases de dados, incluindo MySQL, PostgreSQL, SQLite, Redis e MongoDB. Funciona como serviço web na porta 4224."),
    ("cs-cz",  NAME_EN, "Lehký databázový klient pro více než 100 databází, včetně MySQL, PostgreSQL, SQLite, Redis a MongoDB. Běží jako webová služba na portu 4224."),
    ("da-dk",  NAME_EN, "Let databaseklient til over 100 databaser, herunder MySQL, PostgreSQL, SQLite, Redis og MongoDB. Kører som webtjeneste på port 4224."),
    ("nl-nl",  NAME_EN, "Lichte databaseclient voor meer dan 100 databases, waaronder MySQL, PostgreSQL, SQLite, Redis en MongoDB. Draait als webservice op poort 4224."),
    ("nb-no",  NAME_EN, "Lett databaseklient for over 100 databaser, inkludert MySQL, PostgreSQL, SQLite, Redis og MongoDB. Kjører som webtjeneste på port 4224."),
    ("sv-se",  NAME_EN, "Lätt databasklient för över 100 databaser, inklusive MySQL, PostgreSQL, SQLite, Redis och MongoDB. Körs som webbtjänst på port 4224."),
    ("el-gr",  NAME_EN, "Ελαφρύς πελάτης βάσεων δεδομένων για πάνω από 100 βάσεις, μεταξύ των οποίων MySQL, PostgreSQL, SQLite, Redis και MongoDB. Λειτουργεί ως υπηρεσία web στη θύρα 4224."),
    ("ro-ro",  NAME_EN, "Client de baze de date ușor pentru peste 100 de baze de date, inclusiv MySQL, PostgreSQL, SQLite, Redis și MongoDB. Rulează ca serviciu web pe portul 4224."),
    ("th-th",  NAME_EN, "ไคลเอนต์ฐานข้อมูลแบบเบา รองรับฐานข้อมูลกว่า 100 ระบบ เช่น MySQL, PostgreSQL, SQLite, Redis และ MongoDB ทำงานเป็นเว็บเซอร์วิสบนพอร์ต 4224"),
    ("vi-vn",  NAME_EN, "Ứng dụng khách cơ sở dữ liệu nhẹ hỗ trợ hơn 100 cơ sở dữ liệu, bao gồm MySQL, PostgreSQL, SQLite, Redis và MongoDB. Chạy dưới dạng dịch vụ web trên cổng 4224."),
    ("id-id",  NAME_EN, "Klien basis data ringan untuk 100+ basis data termasuk MySQL, PostgreSQL, SQLite, Redis, dan MongoDB. Berjalan sebagai layanan web di port 4224."),
    ("ar-sa",  NAME_EN, "عميل قواعد بيانات خفيف يدعم أكثر من 100 قاعدة بيانات منها MySQL وPostgreSQL وSQLite وRedis وMongoDB. يعمل كخدمة ويب على المنفذ 4224."),
    ("he-il",  NAME_EN, "קליינט מסדי נתונים קל משקל עבור למעלה מ־100 מסדי נתונים, כולל MySQL, PostgreSQL, SQLite, Redis ו־MongoDB. פועל כשירות אינטרנט בפורט 4224."),
]


def main(out_path: str) -> int:
    lines = []
    for loc, name, desc in LANGS:
        note = NOTE_ZH if loc in ("zh-cn", "zh-hk") else NOTE_EN
        lines.append(f"[{loc}]")
        lines.append(f'name = "{name}"')
        lines.append(f'auth = "{AUTHOR}"')
        lines.append(f'descript = "{desc}"')
        lines.append(f'release_note = "{note}"')
        lines.append(f'important = "{IMPORTANT}"')
        lines.append("")
    content = "\n".join(lines).rstrip("\n") + "\n"
    # UTF-8 without BOM, LF endings
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"wrote {out_path} ({len(LANGS)} languages)")
    return 0


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else f"{APP_ID}.lang"
    sys.exit(main(out))
