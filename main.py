import os

account = 0
magazyn = {}
actions = []

# sprawdzam czy plik accoun.txt istnieje, jesli nie tworze go
if not os.path.exists('account.txt'):
    with open('account.txt', 'w') as f:
        f.write('0')

# sprawdzanie czy plik magazyn istnieje, jesli nie tworze go i ustawiam jako
# pusty
if not os.path.exists('inventory.txt'):
    with open('inventory.txt', 'w') as f:
        pass
else:
    # pobieranie danych z pliku magazynu (inventory.txt)
    with open('inventory.txt', 'r') as f:
        for line in f:
            product, price, quantity = line.strip().split(',')
            magazyn[product] = [int(price), int(quantity)]

# sprawdzanie czy plik actions.txt istnieje, jesli nie tworze go i ustawiam jako
# pustą liste
if not os.path.exists('actions.txt'):
    with open('actions.txt', 'w') as f:
        pass
else:
    # pobieranie danych z actions.txt
    with open('actions.txt', 'r') as f:
        for line in f:
            action = eval(line.strip())
            actions.append(action)

while True:
    print("Dostepne opcje:")
    print("saldo")
    print("sprzedaz")
    print("zakup")
    print("konto")
    print("lista")
    print("magazyn")
    print("przeglad")
    print("koniec")

    command = input("Wybierz opcje: ")

    # tworzenie salda ( dodawanie i odejmowanie podanej wartości)
    if command == "saldo":
        amount = float(input("Wprowadz kwote: "))
        if amount < 0 and abs(amount) > account:
            print("Nie można odjąć więcej niż jest na koncie")
        else:
            account += amount
            actions.append(("saldo", amount))
            print("Saldo zaktualizowane")

    # komenda sprzedaż
    elif command == "sprzedaz":
        product_name = input("Wprowadz nazwe produktu: ")
        price = int(input("Wprowadz cene: "))
        quantity = int(input("Wprowadz ilosc: "))
        if product_name not in magazyn:
            print("Brak produktu w magazynie")
        elif price <= 0 or quantity <= 0:
            print("Podaj prawidłową cenę i ilość")
        elif magazyn[product_name][1] < quantity:
            print("Nie ma wystarczającej ilości produktu w magazynie")
        else:
            account += price * quantity
            magazyn[product_name][1] -= quantity
            actions.append(("sprzedaz", product_name, price, quantity))
            print("Sprzedaz wykonana")

    # komenda zakup
    elif command == "zakup":
        product_name = input("Wprowadz nazwe produktu: ")
        price = int(input("Wprowadz cene: "))
        quantity = int(input("Wprowadz ilosc: "))
        if price <= 0 or quantity <= 0:
            print("Nieprawidłowa cena lub ilosc")
        elif account < price * quantity:
            print("Nie wystarczające środki na koncie")
        else:
            if product_name not in magazyn:
                magazyn[product_name] = [price, quantity]
            else:
                magazyn[product_name][1] += quantity
            account -= price * quantity
            actions.append(("zakup", product_name, price, quantity))
            print("Zakup wykonany")

    # wyswietlanie stanu konta
    elif command == "konto":
        print(f"Stan konta: {account}")

    # komenda lista
    elif command == "lista":
        print("Stan magazynu:")
        # wyświetlanie stanu magazynu
        for product, details in magazyn.items():
            print(f"Produkt: {product}, Cena: {details[0]}, "
                  f"Ilosc: {details[1]}")

    # komenda magazyn
    elif command == "magazyn":
        product_name = input("Wprowadz nazwe produktu: ")
        # jesli jest w magazynie to pokaz nazwe, cene i ilosc
        if product_name in magazyn:
            print(f"Produkt: {product_name}, Cena: {magazyn[product_name][0]}, "
                  f"Ilosc: {magazyn[product_name][1]}")
        else:
            print("Brak produktu w magazynie")

    # komenda przedgląd
    elif command == "przeglad":
        start = input("Wprowadz początek zakresu (lub zostaw puste): ")
        end = input("Wprowadz koniec zakresu (lub zostaw puste): ")
        # index startu
        start = int(start) if start else 0
        # idx koncowy
        end = int(end) if end else len(actions)
        # jesli uzytkownik poda idx spoza zakresu
        if start < 0 or end > len(actions):
            print("Zakres poza granicami. Dostępne akcje: ", len(actions))
        else:
            for action in actions[start:end]:
                print(action)
    # koniec
    elif command == "koniec":
        with open('account.txt', 'w') as f:
            f.write(str(account))

        # save magazyn to inventory.txt file
        with open('inventory.txt', 'w') as f:
            for product, details in magazyn.items():
                f.write(f"{product},{details[0]},{details[1]}\n")

        # save actions to actions.txt file
        with open('actions.txt', 'w') as f:
            for action in actions:
                f.write(str(action) + '\n')
        break
