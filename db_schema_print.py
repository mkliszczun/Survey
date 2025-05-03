from app.models import db  # Zaimportuj instancję bazy danych z Twojej aplikacji
from app.models import * # Zaimportuj Twoje modele (tabele)

# Upewnij się, że 'twoja_aplikacja' jest poprawną nazwą Twojego modułu aplikacji Flask
# Jeśli masz problem z importami, być może będziesz musiał dostosować ścieżki

try:
    from run import app  # Spróbuj zaimportować instancję aplikacji Flask
except ImportError:
    print("Nie można zaimportować 'app' z 'app.py'. Sprawdź nazwę pliku i strukturę projektu.")
    exit()

with app.app_context():
    print("Używana baza danych:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("Lista tabel:")
    for table_name in db.metadata.tables.keys():
        print(f"- {table_name}")

    print("\nSzczegóły tabel:")
    for table_name, table in db.metadata.tables.items():
        print(f"\n--- Tabela: {table_name} ---")
        for column in table.columns:
            print(f"  - {column.name} ({column.type})", end="")
            if column.primary_key:
                print(" PRIMARY KEY", end="")
            if column.foreign_keys:
                for fk in column.foreign_keys:
                    print(f" FOREIGN KEY -> {fk.column.table.name}.{fk.column.name}", end="")
            print()