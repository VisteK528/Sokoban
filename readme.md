# Sokoban
Projekt polega na implementacji gry Sokoban

# Zasady
Gra jest rozgrywana na planszy z kwadratów, gdzie każdy kwadrat jest podłogą lub ścianą. Niektóre kwadraty na podłodze zawierają pudełka, a niektóre kwadraty na podłodze są oznaczone jako miejsca do przechowywania.

Gracz jest ograniczony do planszy i może poruszać się poziomo lub pionowo na puste kwadraty (nigdy przez ściany lub pudełka). Gracz może przesunąć skrzynię, podchodząc do niej i przesuwając ją na sąsiedni kwadrat. Pudełek nie można ciągnąć, nie można ich też pchać na kwadraty ze ścianami lub innymi pudełkami. Liczba pudełek równa się liczbie miejsc do przechowywania. Zagadka zostaje rozwiązana, gdy wszystkie pudełka znajdą się w miejscach przechowywania.

Gra powinna oferować kilka poziomów o różnym stopniu trudności. Kolejny poziom odblokowywany jest po ukończeniu poprzedniego. Projekt można zrealizować z wykorzystaniem interfejsu graficznego lub w konsoli. Interfejs powinien umożliwiać restart poziomu.

Jednym z elementów projektu jest wymyślenie sposobu reprezentacji poziomu (np. w pliku), tak aby możliwe było dodawanie w przyszłości kolejnych poziomów. Przykładowe poziomy można znaleźć na stronie: http://www.sokobano.de/en/levels.php

Przykładowa rozgrywka: https://www.youtube.com/watch?v=4mNswr4Zcos