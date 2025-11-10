from varasto import Varasto, InvalidTilavuus


def main():
    # :p
    variables = {
        "mehua": Varasto(100.0),
        "olutta": Varasto(100.0, 20.2)
    }

    # super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line super long line 

    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {variables['mehua']}")
    print(f"Olutvarasto: {variables['olutta']}")

    print("Olut getterit:")
    print(f"saldo = {variables['olutta'].saldo}")
    print(f"tilavuus = {variables['olutta'].tilavuus}")
    print(f"paljonko_mahtuu = {variables['olutta'].paljonko_mahtuu()}")

    main1(variables)

def main1(variables):
    print("Mehu setterit:")
    print("Lisätään 50.7")
    variables['mehua'].lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {variables['mehua']}")
    print("Otetaan 3.14")
    variables['mehua'].ota_varastosta(3.14)
    print(f"Mehuvarasto: {variables['mehua']}")

    main2(variables)

def main2(variables):
    print("Virhetilanteita:")
    print("Varasto(-100.0);")

    try:
        variables["huono"] = Varasto(-100.0)
    except InvalidTilavuus:
        pass

    main3(variables)

def main3(variables):
    print("Varasto(100.0, -50.7)")

    try:
        variables["huono"] = Varasto(100.0, -50.7)
    except InvalidTilavuus:
        pass

    main4(variables)

def main4(variables):
    print(f"Olutvarasto: {variables['olutta']}")
    print("olutta.lisaa_varastoon(1000.0)")
    variables['olutta'].lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {variables['olutta']}")

    print(f"Mehuvarasto: {variables['mehua']}")
    print("mehua.lisaa_varastoon(-666.0)")
    variables['mehua'].lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {variables['mehua']}")

    main5(variables)

def main5(variables):
    print(f"Olutvarasto: {variables['olutta']}")
    print("olutta.ota_varastosta(1000.0)")
    variables['saatiin'] = variables['olutta'].ota_varastosta(1000.0)
    print(f"saatiin {variables['saatiin']}")
    print(f"Olutvarasto: {variables['olutta']}")

    main6(variables)

def main6(variables):
    print(f"Mehuvarasto: {variables['mehua']}")
    print("mehua.otaVarastosta(-32.9)")
    variables['saatiin'] = variables['mehua'].ota_varastosta(-32.9)
    print(f"saatiin {variables['saatiin']}")
    print(f"Mehuvarasto: {variables['mehua']}")


if __name__ == "__main__":
    main()
