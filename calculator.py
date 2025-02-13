import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Hesap Makinesi")
        self.window.geometry("300x500")
        
        # Tema renkleri
        self.themes = {
            "light": {
                "bg": "white",
                "display_bg": "white",
                "display_fg": "black",
                "btn_number_bg": "#f5f5f5",
                "btn_number_fg": "black",
                "btn_operator_bg": "#0484f7",
                "btn_operator_fg": "white",
                "btn_hover": "#e0e0e0"
            },
            "dark": {
                "bg": "#1a1a1a",
                "display_bg": "#1a1a1a",
                "display_fg": "white",
                "btn_number_bg": "#333333",
                "btn_number_fg": "white",
                "btn_operator_bg": "#0066cc",
                "btn_operator_fg": "white",
                "btn_hover": "#404040"
            }
        }
        
        self.current_theme = "light"
        
        # Tema değiştirme butonu
        self.theme_btn = tk.Button(
            self.window,
            text="🌙",
            font=("Arial", 12),
            bd=0,
            command=self.toggle_theme
        )
        self.theme_btn.place(x=10, y=10)
        
        # Sonuç ekranı
        self.result_var = tk.StringVar(value="0")
        self.result = tk.Entry(
            self.window,
            textvariable=self.result_var,
            justify="right",
            font=("Arial", 36, "bold"),
            bd=0
        )
        self.result.grid(row=0, column=0, columnspan=4, padx=20, pady=(40,20), sticky="nsew")
        
        # Butonlar
        self.buttons = [
            ('C', 1, 0), ('()', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('±', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3)
        ]
        
        self.button_refs = []  # Buton referanslarını saklamak için
        
        # Butonları yerleştir
        self.create_buttons()
        
        # Grid ağırlıklarını ayarla
        self.window.grid_rowconfigure(0, weight=2)
        for i in range(1, 6):
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.window.grid_columnconfigure(i, weight=1)
            
        self.current_number = "0"
        self.previous_number = None
        self.operation = None
        self.new_number = True
        
        # İlk tema uygulaması
        self.apply_theme()
        
    def create_buttons(self):
        for button in self.buttons:
            text, row, col = button
            btn = tk.Button(
                self.window,
                text=text,
                font=("Arial", 20),
                bd=0,
                command=lambda t=text: self.button_click(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.button_refs.append((btn, text))  # Buton ve metnini sakla
            
            # Hover efekti
            btn.bind("<Enter>", lambda e, btn=btn: self.on_hover(btn))
            btn.bind("<Leave>", lambda e, btn=btn: self.off_hover(btn))
    
    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.theme_btn.configure(text="☀️" if self.current_theme == "dark" else "🌙")
        self.apply_theme()
    
    def apply_theme(self):
        theme = self.themes[self.current_theme]
        
        # Ana pencere teması
        self.window.configure(bg=theme["bg"])
        
        # Sonuç ekranı teması
        self.result.configure(
            bg=theme["display_bg"],
            fg=theme["display_fg"],
            insertbackground=theme["display_fg"]
        )
        
        # Butonların teması
        for btn, text in self.button_refs:
            if text in ('÷', '×', '-', '+', '='):
                btn.configure(
                    bg=theme["btn_operator_bg"],
                    fg=theme["btn_operator_fg"]
                )
            else:
                btn.configure(
                    bg=theme["btn_number_bg"],
                    fg=theme["btn_number_fg"]
                )
        
        # Tema butonu teması
        self.theme_btn.configure(
            bg=theme["btn_number_bg"],
            fg=theme["btn_number_fg"]
        )
    
    def on_hover(self, button):
        theme = self.themes[self.current_theme]
        button.configure(bg=theme["btn_hover"])
    
    def off_hover(self, button):
        theme = self.themes[self.current_theme]
        text = [t for btn, t in self.button_refs if btn == button][0]
        if text in ('÷', '×', '-', '+', '='):
            button.configure(bg=theme["btn_operator_bg"])
        else:
            button.configure(bg=theme["btn_number_bg"])
    
    def button_click(self, value):
        if value.isdigit() or value == ".":
            if self.new_number:
                self.current_number = value
                self.new_number = False
            else:
                self.current_number += value
            self.result_var.set(self.current_number)
            
        elif value in ("+", "-", "×", "÷"):
            self.previous_number = float(self.current_number)
            self.operation = value
            self.new_number = True
            
        elif value == "=":
            if self.previous_number is not None and self.operation is not None:
                current = float(self.current_number)
                if self.operation == "+":
                    result = self.previous_number + current
                elif self.operation == "-":
                    result = self.previous_number - current
                elif self.operation == "×":
                    result = self.previous_number * current
                elif self.operation == "÷":
                    result = self.previous_number / current if current != 0 else "Hata"
                
                if isinstance(result, float):
                    # Sonucu düzgün formatla
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = "{:.8f}".format(result).rstrip('0').rstrip('.')
                
                self.result_var.set(result)
                self.current_number = str(result)
                self.previous_number = None
                self.operation = None
                self.new_number = True
                
        elif value == "C":
            self.current_number = "0"
            self.previous_number = None
            self.operation = None
            self.new_number = True
            self.result_var.set(self.current_number)
            
        elif value == "±":
            if self.current_number != "0":
                if self.current_number.startswith("-"):
                    self.current_number = self.current_number[1:]
                else:
                    self.current_number = "-" + self.current_number
                self.result_var.set(self.current_number)
                
        elif value == "%":
            current = float(self.current_number)
            self.current_number = str(current / 100)
            self.result_var.set(self.current_number)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run() 