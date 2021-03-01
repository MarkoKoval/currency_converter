from currencies import Ccy

while True:
    try:
        choice = int(input("Enter 0 to exit or 1 to continue: "))

        if choice == 0:
            exit()
        else:
            for index, it in enumerate(Ccy.currency_rates):
                if index % 6 == 0:
                    print("\n")
                else:
                    print(it + " " + str(Ccy.currency_rates[it]), end=" ")

            base_curr_identifier = input("Enter base currency identifier (UAH, USD ....) : ")
            base_curr_amount = float(input("Enter base currency amount (1, 1.2 ...) : "))

            base = Ccy(base_curr_amount, base_curr_identifier)
            print(base)
            added_curr_identifier = input("Enter added currency identifier (UAH, USD ....) : ")
            added_curr_amount = float(input("Enter added currency amount (1, 1.2 ...) : "))

            added = Ccy(added_curr_amount, added_curr_identifier)
            print(added)
            operation = input("Select choice operation type + or - between currencies: ")
            if operation == "+":
                print(base + added)
            elif operation == "-":
                print(base - added)
    except Exception as e:
        print(e)