import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Tuple
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Klasa bazowa do całkowania funkcji
class Function:
    #Inicjalizacja funkcji z nazwą i LaTeX
    def __init__(self, name: str, latex: str):
        self.name = name
        self.latex = latex
    
    #Metoda do liczenia wartości funkcji w punkcie x
    #W tej klasie jest to tylko szkielet, więc nie ma implementacji
    def evaluate(self, x: float) -> float:
        pass

    #Metoda do zwracania nazwy funkcji
    def __str__(self):
        return self.name

#Funkcje do całkowania
#Każda z nich dziedziczy po klasie Function
#Funkcja wykładnicza
class Exponential(Function):
    def __init__(self):
        super().__init__("e^(-x/2)", r"e^{-x/2}")
    
    def evaluate(self, x: float) -> float:
        return np.exp(-x/2)

#Funkcja wielomianowa
class Polynomial(Function):
    def __init__(self):
        super().__init__("x^2", r"x^2")
    
    def evaluate(self, x: float) -> float:
        return x**2

#Funkcja trygonometryczna
class Trigonometric(Function):
    def __init__(self):
        super().__init__("sin(x)", r"\sin(x)")
    
    def evaluate(self, x: float) -> float:
        return np.sin(x)

#Funkcja racjonalna
class Rational(Function):
    def __init__(self):
        super().__init__("1/(1+x^2)", r"\frac{1}{1+x^2}")
    
    def evaluate(self, x: float) -> float:
        return 1/(1 + x**2)
    
# Funkcja oscylująca
class MultiPeakFunction(Function):
    def __init__(self):
        super().__init__("sin(3x)*cos(x/2)", r"\sin(3x) \cdot \cos\left(\frac{x}{2}\right)")
    
    def evaluate(self, x: float) -> float:
        return np.sin(3*x) * np.cos(x/2)

# Funkcja szybko rosnąca
class GrowingFunction(Function):
    def __init__(self):
        super().__init__("x^3*sin(x)", r"x^3 \cdot \sin(x)")
    
    def evaluate(self, x: float) -> float:
        return x**3 * np.sin(x)

# Funkcja oscylująca z szybkim spadkiem
class ComplexOscillation(Function):
    def __init__(self):
        super().__init__("sin(5x)/(1+x)", r"\frac{\sin(5x)}{1+x}")
    
    def evaluate(self, x: float) -> float:
        return np.sin(5*x)/(1+x)


# Klasa do całkowania metodą Simpsona
# Implementuje zarówno całkowanie na przedziale skończonym, jak i nieskończonym
class SimpsonQuadrature:
    
    #Inicjalizacja klasy z funkcją
    #Funkcja jest przekazywana jako argument
    def __init__(self, function: Function):
        self.function = function
    
    #Metoda do obliczania całki na przedziale skończonym
    #a i b to granice całkowania
    def _simpson_single(self, a: float, b: float) -> float:
        #Połowa przedziału
        h = (b - a) / 2
        #Środek przedziału
        mid = (a + b) / 2
        #zastosowanie wzoru Simpsona
        #e^(-x) jest już uwzględnione w funkcji
        #wzór Simpsona to:
        #I = (b-a)/6 * (f(a) + 4*f((a+b)/2) + f(b))
        return (h / 3) * (
            np.exp(-a) * self.function.evaluate(a) + 
            4 * np.exp(-mid) * self.function.evaluate(mid) + 
            np.exp(-b) * self.function.evaluate(b)
        )

    #Metoda do obliczania całki na każdym przedziale skończonym, n to liczba podprzedziałów
    def _simpson_composite(self, a: float, b: float, n: int) -> float:
        #n musi być liczbą parzystą
        if n % 2 != 0:
            n += 1 
        
        #Długość podprzedziału
        h = (b - a) / n
        #Inicjalizacja wyniku
        result = 0
        
        #Iteracja po podprzedziałach (po 2 podprzedziały)
        for i in range(n // 2):
            #Obliczanie początku i końca podprzedziału
            subinterval_start = a + 2 * i * h
            subinterval_end = subinterval_start + 2 * h
            #Obliczanie całki na podprzedziale
            result += self._simpson_single(subinterval_start, subinterval_end)
            
        return result

    #Metoda do obliczania całki na przedziale skończonym zwiększając liczbę podprzedziałów dopóki nie osiągniemy zadanej dokładności
    #a i b to granice całkowania, tol to zadana dokładność
    def integrate_finite(self, a: float, b: float, tol: float) -> Tuple[float, int]:
        n = 2  #startujemy od 2 podprzedziałów
        #Obliczamy pierwszą całkę
        prev_result = self._simpson_composite(a, b, n)
        #Inicjalizujemy liczbę iteracji
        iterations = 1
        
        #Pętla do obliczania całki
        while True:
            n *= 2  #Podwajamy liczbę podprzedziałów
            #Nowe przybliżenie całki z większą liczbą podprzedziałów
            current_result = self._simpson_composite(a, b, n)
            iterations += 1
            
            #Sprawdzamy czy różnica między nowym a poprzednim wynikiem jest mniejsza od zadanej dokładności
            if abs(current_result - prev_result) < tol:
                return current_result, iterations
            
            #Jeśli nie, to aktualizujemy poprzedni wynik i kontynuujemy
            prev_result = current_result

    #Metoda do obliczania całki na przedziale nieskończonym [0,∞) poprzez rozbicie na przedziały skończone
    #Zaczynamy od przedziału [0,a) i zwiększamy a aż do osiągnięcia zadanej dokładności
    def integrate_infinite(self, tol: float) -> Tuple[float, int]:
        #Zaczynamy od przedziału [0,a) gdzie a=1
        a = 1.0
        #szerokość przedziału
        delta = 1.0
        #Obliczamy całkę na przedziale [0,a) z większą dokładnością
        total_result = self.integrate_finite(0, a, tol / 10)[0]
        iterations = 1
        
        #Pętla do obliczania całki
        #Zwiększamy a o delta i obliczamy całkę na przedziale [a,a+delta)
        while True:
            segment_result, _ = self.integrate_finite(a, a + delta, tol / 10)
            iterations += 1
            
            #Sprawdzamy czy różnica między nowym a poprzednim wynikiem jest mniejsza od zadanej dokładności "efektywna nieskończoność"
            if abs(segment_result) < tol:
                return total_result, iterations
            
            #Jeśli nie, to aktualizujemy całkowity wynik i zwiększamy a o delta
            total_result += segment_result
            a += delta
            delta *= 1.5  #Zwiększamy delta, aby szybciej zbiegać do nieskończoności


# Klasa do całkowania metodą Gaussa-Laguerre'a
# Implementuje kwadraturę Gaussa-Laguerre'a dla funkcji o wadze e^(-x)
class GaussLaguerreQuadrature:

    #Inicjalizacja klasy z funkcją do całkowania
    def __init__(self, function: Function):
        self.function = function
        #Słownik z węzłami i wagami dla kwadratury Gaussa-Laguerre'a dla 2, 3, 4 i 5 węzłów
        #pierwsza lista to węzły, druga to wagi dla każdego węzła
        self.nodes_weights = {
            2: ([0.585786, 3.41421], [0.853553, 0.146447]),
            3: ([0.415775, 2.29428, 6.28995], [0.711093, 0.278518, 0.0103893]),
            4: ([0.322548, 1.74576, 4.53662, 9.39507], [0.603154, 0.357419, 0.0388879, 0.000539295]),
            5: ([0.263560, 1.41340, 3.59642, 7.08581, 12.6408], [0.521756, 0.398667, 0.0759424, 0.00361176, 0.0000233699])
        }
    
    #Metoda do obliczania całki metodą Gaussa-Laguerre'a
    def integrate(self, n: int) -> float:
        #Sprawdzamy czy liczba węzłów jest poprawna
        if n not in self.nodes_weights:
            raise ValueError(f"Liczba węzłów musi być jedną z podanych: {list(self.nodes_weights.keys())}")
        
        #Pobieramy węzły i wagi dla danej liczby węzłów i inicjalizujemy wynik
        nodes, weights = self.nodes_weights[n]
        result = 0.0
        
        #Iterujemy po węzłach i wagach
        #Obliczamy całkę jako sumę wag * wartości funkcji w węzłach
        for i in range(n):
            #nie ma potrzeby mnożyć przez e^(-x) bo jest to już uwzględnione w węzłach i wagach
            result += weights[i] * self.function.evaluate(nodes[i])
            
        return result

# Klasa GUI do całkowania numerycznego
# Używa tkinter do stworzenia prostego interfejsu graficznego
class SimpleIntegrationGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Całkowanie numeryczne")
        self.root.geometry("800x800")
        
        # Lista funkcji do całkowania
        #Każda funkcja jest instancją klasy Function
        self.functions = [
            Exponential(),
            Polynomial(),
            Trigonometric(),
            Rational(),
            MultiPeakFunction(),
            GrowingFunction(),
            ComplexOscillation()
        ]
        
        # Tworzenie głównych elementów GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Główna ramka
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        #ramka wyboru funkcji
        func_frame = ttk.LabelFrame(main_frame, text="Wybierz funkcję", padding="10")
        func_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Tworzenie radiobuttonów dla każdej funkcji
        self.function_var = tk.IntVar(value=0)
        for i, func in enumerate(self.functions):
            ttk.Radiobutton(
                func_frame, 
                text=f"f(x) = {func.name}", 
                variable=self.function_var, 
                value=i
            ).pack(anchor=tk.W, padx=20, pady=2)
        
        #Wpisanie dokładności
        tol_frame = ttk.Frame(main_frame)
        tol_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(tol_frame, text="Dokładność:").pack(side=tk.LEFT, padx=5)
        self.tolerance_var = tk.StringVar(value="1e-6")
        ttk.Entry(tol_frame, textvariable=self.tolerance_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Przycisk do obliczania
        ttk.Button(
            main_frame, 
            text="Oblicz", 
            command=self.calculate
        ).pack(pady=10)
        
        #ramka wyników
        results_frame = ttk.LabelFrame(main_frame, text="Wyniki", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tworzenie pola tekstowego do wyświetlania wyników
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            wrap=tk.WORD, 
            height=10, 
            font=('Arial', 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        #ramka wykresu
        self.plot_frame = ttk.LabelFrame(main_frame, text="Wykres funkcji", padding="10")
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tworzenie wstepnego pustego wykresu
        self.figure = None
        self.create_empty_plot()
    
    def create_empty_plot(self):
        #Czyszczenie wykresu jesli istniał
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
            
        self.figure = plt.figure(figsize=(7, 4))
        
        canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Metoda do obliczania całki i wyświetlania wyników
    def calculate(self):
        try:
            # Czyszczenie pola tekstowego
            self.results_text.delete(1.0, tk.END)
            
            # Pobieranie wybranej funkcji i dokładności
            function = self.functions[self.function_var.get()]
            tol = float(self.tolerance_var.get())
            
            # Obliczanie całki na przedziale [0,∞) metodą Simpsona
            simpson = SimpsonQuadrature(function)
            simpson_result, simpson_iterations = simpson.integrate_infinite(tol)
            
            #Wyświetlanie wyników
            self.results_text.insert(tk.END, f"Całkowanie f(x) = {function} z wagą e^(-x) na przedziale [0,∞)\n")
            self.results_text.insert(tk.END, f"Zadana dokładność: {tol}\n\n")
            
            self.results_text.insert(tk.END, "Metoda złożonej kwadratury Newtona-Cotesa (metoda Simpsona):\n")
            self.results_text.insert(tk.END, f"  Wynik: {simpson_result:.10f}\n")
            self.results_text.insert(tk.END, f"  Liczba iteracji: {simpson_iterations}\n\n")
            
            # Obliczanie całki metodą Gaussa-Laguerre'a
            gauss = GaussLaguerreQuadrature(function)
            self.results_text.insert(tk.END, "Kwadratura Gaussa-Laguerre'a:\n")
            
            # Obliczanie całki dla 2, 3, 4 i 5 węzłów i porównywanie wyników
            for n in [2, 3, 4, 5]:
                gauss_result = gauss.integrate(n)
                diff = abs(simpson_result - gauss_result)
                self.results_text.insert(tk.END, f"  {n} węzły: {gauss_result:.10f} (różnica: {diff:.10e})\n")
            
            # Tworzenie wykresu
            self.update_plot(function)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Metoda do aktualizacji wykresu na podstawie wybranej funkcji
    def update_plot(self, function):
        # Wyczyść poprzedni wykres
        plt.close(self.figure) if self.figure else None
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
            
        # Stwórz nowy wykres
        self.figure = plt.figure(figsize=(7, 4))
        ax = self.figure.add_subplot(111)
        
        # Generowanie danych do wykresu
        x = np.linspace(0, 10, 1000)
        y = [np.exp(-xi) * function.evaluate(xi) for xi in x]
        
        # Rysowanie wykresu
        ax.plot(x, y)
        ax.grid(True)
        ax.set_title(f"$e^{{-x}} \\cdot {function.latex}$")
        ax.set_xlabel("x")
        ax.set_ylabel(f"y")
        
        # wstawienie wykresu w ramce
        canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def on_close(self):
        # Zamykanie wszystkich wykresów matplotlib
        plt.close('all')
        # Zniszczenie głównego okna
        self.root.destroy()
        # Zakończenie procesu
        self.root.quit()

# Funkcja główna do uruchomienia aplikacji
if __name__ == "__main__":
    plt.rcParams.update({
        "text.usetex": False,
        "font.family": "serif",
        "mathtext.fontset": "stix"
    })
    
    root = tk.Tk()
    app = SimpleIntegrationGUI(root)
    # Obsługa zamknięcia okna
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
