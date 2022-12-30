# Sokoban
# Ogólne informacje
Gra składa się z 15 poziomów o różnym stopniu trudności. Możliwe jest dodawanie nowych poziomów poprzez dodatkowy edytor poziomów. Poziomy zapisywane są w formacie JSON.

Gra jest rozgrywana na planszy z kwadratów, gdzie każdy kwadrat jest podłogą lub ścianą. Niektóre kwadraty na podłodze zawierają pudełka, a niektóre kwadraty na podłodze są oznaczone jako cele.

Gracz jest ograniczony do planszy i może poruszać się poziomo lub pionowo na puste kwadraty (nigdy przez ściany lub pudełka). Gracz może przesunąć skrzynię, podchodząc do niej i przesuwając ją na sąsiedni kwadrat. Pudełek nie można ciągnąć, nie można ich też pchać na kwadraty ze ścianami lub innymi pudełkami. Poziom zostaje zaliczony w momencie umieszczenia wszystich pudełek na polach celu.

# Sterowanie
## Gra
Sterowanie w grze odbywa się za pomocą przycisów:
1. W - w górę
2. S - w dół
3. A - w lewo
4. D - w prawo

Ponadto do resetowania poziomu należy użyć myszki
## Edytor świata
W edytorze świata plansza podzielona jest na n wierszy oraz m kolumn gdzie n = (wysokość planszy // wymiary pojedyńczego kwadratu) oraz m = (szerokość planszy // wymiary pojedyńczego kwadratu) (obie wartości podawane w pikselach).

Domyślnie edytor świata jest ustawiony na poziom 1 (zwiększanie i zmiejszanie numeru poziomu odbywa się zapomocą strzałek góra i dół).
Aby załadować poziom, należy wybrać interesujący użytkownika poziom za pomocą strzałek góra i dół, a następnie użyć przycisku LOAD.
W przypadku, gdy interesujący użytkownika poziom jeszcze nie istnieje załadowany zostanie pusty poziom.

Użytkownik posiada następującą pulę obiektów o określonych indeksach(w sytuacji, gdy gracz nie jest jeszcze ustawiony na planszy):
1. Ściana
2. Pudełko
3. Cel
4. Pudełko z celem
5. Gracz
6. Pusta przestrzeń

W przypadku, gdy gracz jest już ustawiony na planszy użytkownik ma do wyboru następującą pulę obiektów:
1. Ściana
2. Pudełko
3. Cel
4. Pudełko z celem
5. Pusta przestrzeń

Domyślnie licznik stawiania obiektów(w każdym polu) ma wartość 0. Aby postawić obiekt z puli należy użyć lewego przycisku myszki. Spowoduje to i zwiększenie licznika stawiania w tym polu o jeden i postawienie i-tego obiektu. Z kolei użycie prawego przycisku myszki spowoduje zmniejszenie licznika stawiania w tym polu o jeden i postawienie i-tego obiektu. Operacja zwiększania oraz zmniejszania w polu odbywa się w cyklu zamkniętym.

Gdy użytkownik uzna, że poziom spełnia wszystkie jego oczekiwania może dokonać jego zapisu do pamięci za pomocą przycisku SAVE.
# Podział projektu
Projekt został podzielony na następujące katalogi oraz moduły
## Katalogi
1. Levels - miejsce przechowywania zapisanych poziomów w formacie JSON
2. Tests - testy jednostkowe
## Moduły główne
1. main.py - moduł główny, z poziomu którego uruchamiana jest gra
2. editor.py - moduł edytora, z poziomu któ©ego uruchamiany jest edytor poziomu
3. settings.py - moduł zawierający ustawienia rozgrywki
## Moduły zasadnicze
1. classes.py - moduł zawierający główne klasy rozgrywki - Tile(Ściana), Box(Pudełko), Player(Gracz), Target(Cel) oraz Entity - klasa wspólna
2. game.py - główny moduł gry zawierający klasę Game
3. interface.py - moduł interface'u graficznego, zawierajacy klasę Interface, Button oraz RGB
4. level_editor.py - główny moduł edytora zawierający klasę LevelEditor
5. level.py - moduł levelu zawierający klasę Level zajmującą się logiką rozgrywki na danym poziomie
6. load_level.py - moduł zawierający klasę LoadLevel zajmującą się wczytywaniem danych poziomu z pliku oraz funkcję check_requirements() zajmującą się sprawdzaniem spójności ładowanego poziomu z aktualnie zainicjalizowaną grą