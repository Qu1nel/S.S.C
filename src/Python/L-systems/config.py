WIDTH = 1920
HEIGHT = 1000

gens = 11
rules = {
    "Honeycombs": ({"A": "AB", "B": "A"}, "A"),
    "Sierpinski triangle": ({"F": "F-G+F+G-F", "G": "GG"}, "F"),
    "Dragon curve": ({"x": "x+yf+", "y": "-fx-y"}, "xy"),
    "koch snowflake": ({"f": "f-f++f-f"}, "f++f++f"),
    "tree": ({"X": "F[+X]F[-X]+X", "F": "FF"}, "X"),
    "Realistic Tree": ({"X": "F[@[-X]+X]"}, "X"),
    "Gosper curve": (
        {"F": "", "L": "FL-FR--FR+FL++FLFL+FR-", "R": "+FL-FRFR--FR-FL++FL+FR"},
        "FL",
    ),
    "Flower": ({"F": "FF[++F][+F][F][-F][--F]"}, "F[+F+F][-F-F][++F][--F]F"),
    "Bush": ({"F": "-F+F+[+F-F-]-[-F+F+F]"}, "F"),
}
