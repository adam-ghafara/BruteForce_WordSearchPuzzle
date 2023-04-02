import tkinter as tk
import tkinter.font as tkFont
from os import listdir, getcwd
from random import choice
from functools import partial
from WordSearch import WordSearch


class WordBoard:
    def __init__(self, size=16, color="yellow", file_name="words.txt", words=None):
        assert size > 5
        root = tk.Tk()
        root.title("Word Search Puzzle Games")
        root.resizable(width=False, height=False)

        self._word_grid = tk.Frame(root)
        self._word_list = tk.Frame(root)
        self._menu = tk.Frame(root)

        self._solution_shown = False
        self._size = size
        self._color = color

        new_words_button = tk.DISABLED
        if file_name in listdir(getcwd()):
            new_words_button = tk.NORMAL
            with open(file_name, mode="r") as f:
                self._wordstxt = filter(None, f.read().split("\n"))
                self._wordstxt = list(
                    filter(lambda x: len(x) < self._size - 3, self._wordstxt)
                )
        elif words is None:
            raise FileNotFoundError(
                f"""{file_name} not present in the current directory. {file_name}
                                    must contain words separated by newline (\\n) characters."""
            )

        self._pushed = set()

        self._words = words
        if self._words is None:
            self._choose_random_words()
        else:
            self._words = list(set(map(str.upper, self._words)))

        self._buttons = []
        for i in range(self._size):
            row = []
            for j in range(self._size):
                row.append(
                    tk.Button(
                        self._word_grid, padx=5, command=partial(self._pressed, i, j)
                    )
                )
                row[-1].grid(row=i, column=j, sticky="ew")
            self._buttons.append(row)

        tk.Label(self._menu, text="Menu", pady=5, font=tkFont.Font(weight="bold")).grid(
            row=0, column=0, columnspan=2, sticky="ew"
        )
        tk.Button(
            self._menu,
            text="Kata Baru",
            padx=1,
            pady=1,
            state=new_words_button,
            command=self._select_new,
        ).grid(row=1, column=0, sticky="ew")
        self._export_button = tk.Button(
            self._menu, text="Ekspor", padx=1, pady=1, command=self._export
        )
        self._export_button.grid(row=1, column=1, sticky="ew")
        tk.Button(
            self._menu, text="Cari Kata", padx=1, pady=1, command=self._solution
        ).grid(row=2, column=0, sticky="ew")
        tk.Button(
            self._menu, text="Acak", padx=1, pady=1, command=self._reshuffle
        ).grid(row=2, column=1, sticky="ew")

        self._labels = {}
        self._word_search = None
        self._create_labels()
        self._reshuffle()

        self._word_grid.pack(side=tk.LEFT)
        self._menu.pack(side=tk.TOP, pady=self._size)
        self._word_list.pack(side=tk.TOP, padx=40, pady=20)

        tk.mainloop()

    def _create_labels(self):
        for label in self._labels.values():
            label.destroy()
        self._labels.clear()
        self._labels = {
            "Kata": tk.Label(
                self._word_list, text="Kata", pady=5, font=tkFont.Font(weight="bold")
            )
        }
        self._labels["Kata"].grid(row=2, column=0, columnspan=2)
        for i, word in enumerate(sorted(self._words)):
            self._labels[word] = tk.Label(
                self._word_list, text=word, anchor="w")
            self._labels[word].grid(
                row=(i // 2) + (i % 1) + 3, column=i % 2, sticky="W"
            )

    def _choose_random_words(self):
        self._words = set()
        for _ in range(choice(range(self._size // 3, self._size))):
            self._words.add(choice(self._wordstxt).upper())
        self._words = list(self._words)

    def _pressed(self, row, col):
        if self._buttons[row][col].cget("bg") == self._color:
            self._buttons[row][col].configure(bg="SystemButtonFace")
            self._pushed.remove(
                (self._buttons[row][col].cget("text"), col, row))
        else:
            self._buttons[row][col].configure(bg=self._color)
            self._pushed.add((self._buttons[row][col].cget("text"), col, row))
            for word, coords in self._word_search.solutions.items():
                if coords & self._pushed == coords:
                    for _, col, row in coords:
                        self._buttons[row][col].configure(state=tk.DISABLED)
                    self._labels[word].configure(bg=self._color)

    def _solution(self):
        if self._solution_shown:
            bg = "SystemButtonFace"
            state = tk.NORMAL
            self._pushed.clear()
        else:
            bg = self._color
            state = tk.DISABLED

        self._solution_shown = not self._solution_shown
        for word, coords in self._word_search.solutions.items():
            self._labels[word].configure(bg=bg)
            for _, col, row in coords:
                self._buttons[row][col].configure(state=state, bg=bg)

    def _reshuffle(self):
        self._export_button.configure(text="Export", state=tk.NORMAL)

        if self._solution_shown:
            self._solution_shown = not self._solution_shown
        self._word_search = WordSearch(self._size, self._words)
        self._pushed.clear()

        for i in range(self._size):
            for j in range(self._size):
                self._buttons[i][j].configure(
                    text=self._word_search.board[i][j],
                    bg="SystemButtonFace",
                    state=tk.NORMAL,
                )

        for label in self._labels.values():
            label.configure(bg="SystemButtonFace")

    def _select_new(self):
        self._choose_random_words()
        self._reshuffle()
        self._create_labels()

    def _export(self):
        self._export_button.configure(state=tk.DISABLED)

        number = 0
        file_name = "WordSearch.html"
        while file_name in listdir(getcwd()):
            number += 1
            file_name = f"WordSearch{number}.html"

        with open(file_name, mode="w") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("\t<title>Word Search</title>\n")
            # Scripts required to display LaTeX
            f.write(
                """\t<script type="text/x-mathjax-config">
                    MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\\\(','\\\\)']]}});
                    </script>
                    <script type="text/javascript"
                    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
                    </script>\n"""
            )
            f.write("</head>\n")
            f.write('<h2 align="center">HTML Table WordSearch Grid:</h2>\n<br><br>')

            f.write('<table align="center">\n')
            for i in range(self._size):
                f.write("\t<tr>\n\t\t")
                for j in range(self._size):
                    f.write(
                        f"<td padding=1em>{self._word_search.board[i][j]}</td>")
                f.write("\t</tr>\n")
            f.write("</table>\n<br><br>")

            f.write('<h2 align="center">Latex WordSearch Grid:</h2>\n<br><br>')
            f.write("\\begin{matrix}")
            f.write(" \\\\ ".join([" & ".join(row)
                    for row in self._word_search.board]))
            f.write("\\end{matrix}\n<br><br>")
            f.write('<h2 align="center">WordSearch Grid as String:</h2>\n<br><br>')

            f.write('<div align="center">\n')
            f.write(
                " ::: ".join(
                    ["".join(self._word_search.board[i])
                     for i in range(self._size)]
                )
            )
            f.write("\n<br><br>\n")
            f.write(
                "\n".join(
                    ["".join(self._word_search.board[i])
                     for i in range(self._size)]
                )
            )
            f.write("</div>\n")

            f.write('\n<br><br><h2 align="center">Solution</h2><br><br>\n')
            f.write("\\begin{matrix}")

            coordinates = set()
            for coords in self._word_search.solutions.values():
                for coord in coords:
                    coordinates.add(coord)

            board = []
            for i in range(self._size):
                row = []
                for j in range(self._size):
                    if (self._word_search.board[i][j], j, i) in coordinates:
                        row.append(self._word_search.board[i][j])
                    else:
                        row.append("")
                board.append(row)

            f.write(" \\\\ ".join([" & ".join(row) for row in board]))
            f.write("\\end{matrix}")

            f.write('\n<br><br><h2 align="center">Words</h2><br><br>\n')
            f.write(
                f"""<ul align="center"><li>{'</li><li>'.join(self._words)}</li></ul>\n"""
            )
            f.write(
                f'\n<br><br><h2 align="center">SIZE: {self._size}x{self._size}</h2><br><br>\n'
            )
            f.write("</html>")

        self._export_button.configure(text="Exported")
