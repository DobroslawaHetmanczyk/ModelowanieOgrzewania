# ModelowanieOgrzewania

## Abstrakt
Projekt ma za zadanie symulować rozkład temperatury w pomieszczeniach w wyznaczonym okresie czasu, uwzględniając różne elementy, takie jak ściany, drzwi, okna, grzejniki. Symulacja opiera się na równaniach dyfuzji ciepła. Wyniki symulacji są wizualizowane za pomocą animacji pokazującej zmiany temperatury w czasie.

## Opis skryptów

- plan_mieszkania.py - tworzy plan mieszkania do problemu badawczego 1.1
- plan_mieszkania2.py - tworzy plan mieszkania do problemu badawczego 1.2
- Problem_z_umiejscowieniem_grzejnikow.py - rozwiązuje problem badawczy 1.1
- Ogrzewanie_z_wylaczaniem_grzejnikow1.py - rozwiązuje problem badawczy 1.2 dla danych 'temperatures.csv' z uwzględnieniem wyłączania grzejników pod nieobecność lokatorów
- Ogrzewanie_z_wylaczaniem_grzejnikow2.py - rozwiązuje problem badawczy 1.2 dla danych 'temperature_data_kelvin.csv' z uwzględnieniem wyłączania grzejników pod nieobecność lokatorów
- Ogrzewanie_z_wylaczaniem_grzejnikow3.py - rozwiązuje problem badawczy 1.2 dla danych 'temperatures_5_7.csv' z uwzględnieniem wyłączania grzejników pod nieobecność lokatorów
- Ogrzewanie_pelne1.py - rozwiązuje problem badawczy 1.2 dla danych 'temperatures.csv' bez wyłączania grzejników
- Ogrzewanie_pelne2.py - rozwiązuje problem badawczy 1.2 dla danych 'temperature_data_kelvin.csv' bez wyłączania grzejników
- Ogrzewanie_pelne3.py - rozwiązuje problem badawczy 1.2 dla danych 'temperatures_5_7.csv' bez wyłączania grzejników
- Ogrzewanie_bez_grzejnikow_tydzien.py - rozwiązuje problem badawczy 1.2 dla danych 'temperatures.csv' z uwzględnieniem wyłączania grzejników pod nieobecność lokatorów ale liczy czas w ciągu jednego tygodnia. Prezentacja sposobu równieżużytego dla pozostałych plików.

## Wymagania

- Python 3.8 lub nowszy
- Biblioteki wymienione w pliku requirements.txt

## Autor

Dobrosława Hetmańczyk

