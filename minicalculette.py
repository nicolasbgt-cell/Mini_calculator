import tkinter as tk
import functools
import re


def print_welcome_message() -> None:
    print("Bienvenue sur la mini-calculatrice !")


def input_two_number() -> tuple[float, float]:
    num1 = float(input("Entrez le premier nombre : "))
    num2 = float(input("Entrez le deuxieme nombre : "))
    return num1, num2


def print_menu_and_get_choice() -> str:
    print("=== MENU ===")
    print("1. Addition")
    print("2. Soustraction")
    print("3. Multiplication")
    print("4. Division")

    user_choice = input("Entrez votre choix (1-4) : ")

    while user_choice not in ["1", "2", "3", "4"]:

        user_choice = input("Choix invalide. Entrez votre choix : ")

    return user_choice


def sum(a: float, b: float) -> float:
    return a + b


def substraction(a: float, b: float) -> float:
    return a - b


def multiplication(a: float, b: float) -> float:
    return a * b


def division(a: float, b: float) -> float | None:
    if b != 0:
        return a / b
    else:
        print("Erreur : division par zero")
        return None


def run_calculation(user_choice: str) -> float | None:
    num1, num2 = input_two_number()
    result: float | None = None
    match user_choice:
        case '1':
            result = sum(num1, num2)
        case '2':
            result = substraction(num1, num2)
        case '3':
            result = multiplication(num1, num2)
        case '4':
            result = division(num1, num2)
        case _:
            print("Choix invalide.")
    return result


class Calculatrice:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Mini Calculatrice")
        self.root.configure(bg="#1e1e2e")
        self.expression = ""
        self._build_ui()

    def _build_ui(self) -> None:
        self.expression_label = tk.Label(
                self.root,
                text="",
                font=("Courier New", 14),
                bg="#1e1e2e",
                fg="#888899",
                anchor="e",
                )
        self.expression_label.grid(row=0, column=0, columnspan=4,
                                   sticky="ew", padx=16, pady=(16, 0))

        self.result_label = tk.Label(
                self.root,
                text="0",
                font=("Courier New", 36, "bold"),
                bg="#1e1e2e",
                fg="#cdd6f4",
                anchor="e",
                )
        self.result_label.grid(row=1, column=0, columnspan=4,
                               sticky="ew", padx=16, pady=(0, 16))

        buttons: list[list[str]] = [
                ["7", "8", "9", "÷"],
                ["4", "5", "6", "×"],
                ["1", "2", "3", "-"],
                ["C", "0", ".", "+"],
                ["", "", "", "="],
                ]
        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                if label == "":
                    continue
                tk.Button(
                        self.root, text=label,
                        font=("Courier New", 20, "bold"),
                        command=functools.partial(self._on_click, label)
                        ).grid(row=r + 2, column=c, padx=6, pady=6)

    def _on_click(self, label: str) -> None:
        if label == "C":
            self.expression = ""
            self.expression_label.config(text="")
            self.result_label.config(text="0")
        elif label == "=":
            try:
                expr = self.expression
                result: float | None = None
                if "+" in expr[1:]:
                    a, b = expr.split("+")
                    result = sum(float(a), float(b))
                elif "-" in expr[1:]:
                    a, b = expr.split("-")
                    result = substraction(float(a), float(b))
                elif "*" in expr:
                    a, b = expr.split("*")
                    result = multiplication(float(a), float(b))
                elif "/" in expr:
                    a, b = expr.split("/")
                    result = division(float(a), float(b))

                self.expression_label.config(text=expr.replace("*", "×")
                                             .replace("/", "÷"))
                self.result_label.config(text=str(result))
                self.expression = ""
            except Exception:
                self.result_label.config(text="Erreur")
        elif label == ".":
            last_number = re.split(r"[+\-*/]", self.expression)[-1]
            if "." not in last_number:
                self.expression += "."
                self.result_label.config(text=self.expression)
        else:
            self.expression += {"÷": "/", "×": "*"}.get(label, label)
            self.result_label.config(text=self.expression)


if __name__ == "__main__":
    root = tk.Tk()
    Calculatrice(root)
    root.mainloop()
