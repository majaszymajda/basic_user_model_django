# Akademia BonaSoft 2021

## Obsługa docker'a

1. w folderze .envs/ kopiujemy plik .env.example i uzupełniamy zmienną ``APP_SECRET_KEY`` losowymi znakami
2. W głównym folderze odpalamy dockera za pomocą komendy
`docker-compose up --build`
3. Po poprawnym uruchomieniu, nasz projekt będzie widoczny, zależnie od środowiska w którym uruchomiliśmy dockera, najczęściej jest to:\
`https://host.docker.internal:8000`
`https://localhost:8000`
5. Opcjonalnie uzupełniami kimai losowymi danymi
`docker exec ba-kimai /opt/kimai/bin/console kimai:reset-dev`
4. Dodajemy konto admina do kimai poprzez polecenie
`docker exec ba-kimai /opt/kimai/bin/console kimai:create-user admin admin@example.com ROLE_SUPER_ADMIN password` \
kimai będzie dostępny pod linkiem tak jak wyżej, tyle na porcie `8001`

## Komendy do obsługi docker'a + troubleshooting
- `docker-compose stop` zatrzymanie kontenerów dockerowych(z zachowaniem danych) \
- `docker-compose down` zresetowanie kontenerów dockerowych(z wyczyszczeniem danych np. postgresa i kimai)
- `docker-compose build --no-cache` przebudowanie od zera obrazów i kontenerów dockerowych(--no-cache jest dłuższe, ale dzięki temu odswieżymy biblioteki pythonowe)
- `docker-compose down && docker-compose build --no-cache && docker-compose up` pełny reset naszych kontenerów
- `docker container ls -a` wylistowanie włączonych i wyłączonych kontenerów
- `docker container stop nazwa_lub_id_kontenera` ręczne wyłączenie kontenera
- `docker exec -it nazwa_lub_id_kontenera bash` "wejście" do kontenera django(o ile jest uruchomiony)
- `docker image ls` wylistowanie obrazów dockerowych
- Gdy wyskoczy nam błąd: ``/start: line 7: ./compose/django/wait-for-it.sh: No such file or directory``
trzeba w takim pliku zamienić znaki \r\n na \n

## Pre Commit

- Dodany został pre-commit mający na celu wyłapanie, czy kod jest poprawnie sformatowany i zgodny z linterem.
- Instrukcja instalacji dostępna na: https://pre-commit.com
