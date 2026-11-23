data = {
    "/": " ",
    "-": ",",
    "÷0÷*+": "и",
    "×": "а",
    "÷": "б",
    "=": "в",
    "CM": "г",
    "+": "д",
    "Ds": "е",
    "\"'": "ё",
    "+^": "ж",
    "&": "з",
    "MXI": "й",
    "MCM": "к",
    "|^2|": "л",
    "3": "м",
    "4": "н",
    "sqrt(CM)": "о",
    "10001": "п",
    "10010": "р",
    "10011": "с",
    "10100": "т",
    "10101": "у",
    "10110": "ф",
    "#": "х",
    "11000": "ц",
    "11001": "ч",
    "11010": "ш",
    "11011": "щ",
    "11100": "ъ",
    "11101": "ы",
    "11110": "ь",
    "5": "э",
    "log(+)": "ю",
    "100001": "я",
}

message = "5CMsqrt(CM)÷10011|^2|CMsqrt(CM)4Ds1000110010sqrt(CM)10011CMsqrt(CM)"
result = []
mes = "1010011101/10001sqrt(CM)+101014×MXI/Ds11011\"'-÷0÷*+÷sqrt(CM)/=/10011|^2|sqrt(CM)=×#/sqrt(CM)11010÷0÷*+÷MCM÷0÷*+"

while mes:
    for key, value in data.items():
        if mes.lower().startswith(key.lower()):
            result.append(value)
            mes = mes[len(key):]
            print(result, mes)

print(''.join(result))
result.clear()

data = {value: key for key, value in data.items()}
print(data)

user = input("> ")
for letter in user:
    result.append(data[letter])

print(''.join(result))
