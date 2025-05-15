# Dokumentacja programu do całkowania numerycznego

## Spis treści
1. [Wstęp teoretyczny](#wstęp-teoretyczny)
2. [Metody całkowania numerycznego](#metody-całkowania-numerycznego)
   - [Złożona kwadratura Newtona-Cotesa (metoda Simpsona)](#złożona-kwadratura-newtona-cotesa-metoda-simpsona)
   - [Kwadratura Gaussa-Laguerre'a](#kwadratura-gaussa-laguerre'a)
3. [Implementacja programu](#implementacja-programu)
   - [Struktura programu](#struktura-programu)
   - [Klasy funkcji](#klasy-funkcji)
   - [Implementacja kwadratury Simpsona](#implementacja-kwadratury-simpsona)
   - [Implementacja kwadratury Gaussa-Laguerre'a](#implementacja-kwadratury-gaussa-laguerre'a)
   - [Interfejs graficzny (GUI)](#interfejs-graficzny-gui)
4. [Instrukcja użytkowania](#instrukcja-użytkowania)
5. [Przykłady użycia](#przykłady-użycia)

## Wstęp teoretyczny

Całkowanie numeryczne jest techniką obliczania przybliżonej wartości całki oznaczonej, gdy bezpośrednie obliczenie całki za pomocą metod analitycznych jest trudne lub niemożliwe. W tym programie zaimplementowano dwie metody całkowania numerycznego:

1. **Złożoną kwadraturę Newtona-Cotesa** opartą na trzech węzłach (wzór Simpsona)
2. **Kwadraturę Gaussa-Laguerre'a** do całkowania na przedziale [0,+∞) z wagą e^(-x)

Program umożliwia obliczanie całek postaci:

$$\int_{0}^{\infty} e^{-x} f(x) dx$$

gdzie f(x) jest dowolną funkcją, którą można zaimplementować w programie.

## Metody całkowania numerycznego

### Złożona kwadratura Newtona-Cotesa (metoda Simpsona)

#### Teoria

Wzór Simpsona jest metodą całkowania numerycznego opartą na przybliżaniu funkcji wielomianem drugiego stopnia. Dla pojedynczego przedziału [a,b] wzór Simpsona ma postać:

$$\int_{a}^{b} f(x) dx \approx \frac{b-a}{6} \left[ f(a) + 4f\left(\frac{a+b}{2}\right) + f(b) \right]$$

Złożona kwadratura Simpsona polega na podziale przedziału całkowania na n podprzedziałów i zastosowaniu wzoru Simpsona na każdym z nich. Jeśli podzielimy przedział [a,b] na n równych części o szerokości h = (b-a)/n, to wzór złożonej kwadratury Simpsona ma postać:

$$\int_{a}^{b} f(x) dx \approx \frac{h}{3} \left[ f(a) + 2\sum_{i=1}^{n/2-1} f(a+2ih) + 4\sum_{i=0}^{n/2-1} f(a+(2i+1)h) + f(b) \right]$$

W przypadku całkowania z wagą e^(-x), funkcja podintegralna ma postać e^(-x)·f(x).

Dla całek niewłaściwych, takich jak ∫₀^∞ e^(-x)·f(x) dx, stosuje się technikę obliczania granicy. Zaczynamy od obliczenia całki na skończonym przedziale [0,a], a następnie dodajemy kolejne przedziały [a,a+δ], [a+δ,a+2δ], itd., aż wartość całki na dodawanym przedziale stanie się mniejsza od zadanej tolerancji.

### Kwadratura Gaussa-Laguerre'a

#### Teoria

Kwadratura Gaussa-Laguerre'a jest specjalnie zaprojektowana do całkowania funkcji na przedziale [0,+∞) z wagą e^(-x). Ma ona postać:

$$\int_{0}^{\infty} e^{-x} f(x) dx \approx \sum_{i=1}^{n} w_i f(x_i)$$

gdzie x_i są węzłami kwadratury (miejscami zerowymi wielomianu Laguerre'a stopnia n), a w_i są odpowiednimi wagami.

Kwadratura Gaussa-Laguerre'a jest dokładna dla wielomianów stopnia do 2n-1, gdzie n jest liczbą węzłów kwadratury.

Węzły i wagi dla kwadratury Gaussa-Laguerre'a są tabelaryzowane i dostępne w literaturze dla różnych wartości n.

## Implementacja programu

### Struktura programu

Program składa się z następujących głównych komponentów:
1. Klasy funkcji do całkowania
2. Implementacja metody Simpsona
3. Implementacja kwadratury Gaussa-Laguerre'a
4. Interfejs graficzny (GUI)

