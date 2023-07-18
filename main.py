from shekel import ILS
from dollar import USD
from result import Result
import requests
import os

# Get exchange rates from REST api
def api_session():
    response = requests.get("https://api.currencyapi.com/v3/latest?apikey=cur_live_dYaXB4q1zozH9cgBWYXexNjZ0I2dvTNuxMmF2v1E")
    if response.status_code == 200:
        value_data = response.json()
        # creates a dictionary of the specific exchange rate in use of the converter.
        currency_live = {"USD to ILS":value_data["data"]["ILS"]["value"],
                        "ILS to USD":1/value_data["data"]["ILS"]["value"]}
        return currency_live
    else:
        print("Could not get rate from API using default rate")
        return 0

# Gets a value to convert from the user, receive only positive number.
def get_value_to_convert():
    while True:
        value_conv = input("Please enter an amount to convert: ")
        try:
            value_conv = float(value_conv)
        except ValueError:
            print("INVALID: You need to enter a number.")
            continue
        if value_conv>0:
            return value_conv
        else:
            print("INVALID: The amount must be higher then zero")

# Provides the choice of conversion to the user, receive as parameter the current rates dictionary.
def get_user_value(rates):
    results = []
    while True:
        user_choice = input("Please choose an option (1/2):\n1. Dollars to Shekels\n2. Shekels to Dollars\n")
        if user_choice == "1":
            value_to_convert = get_value_to_convert()
            usd = USD()
            if rates != 0:
                usd.set_value(rates["USD to ILS"])
            else:
                pass
            calc = Result(round(usd.calculate(value_to_convert),2), "USD to ILS")
            print(calc.value)
            return calc
        elif user_choice == "2":
            value_to_convert = get_value_to_convert()
            ils = ILS()
            if rates != 0:
                ils.set_value(rates["ILS to USD"])
            else:
                pass
            calc = Result(round(ils.calculate(value_to_convert),2), "ILS to USD")
            print(calc.value)
            return calc
        else:
            print("Your choice is invalid, please pick again.")

# This functions checks if user would like to have another round.
def again():
    while True:
        massage = input("Do you want make another calculation? (Y/N): ")
        massage = massage.upper()
        if massage == "Y":
            return True
        elif massage == "N":
            return False
        else:
            print("Your choice is invalid.")

# Receive the conversions results list and saves it as a .txt file
def export_results(list):
    try:
        file = open("results.txt", "w")
        for res in list:
            file.write(f"{res.value} , {res.currency}\n")
    except IOError:
        print("An Error as occurred")
    finally:
        file.close()

# Opens up the result .txt file automatically
def open_file():
    os.startfile("results.txt")

# Main function running the currency converter
def main():
    results = []
    print("Welcome to currency converter.")
    exchange_list = api_session()
    results.append(get_user_value(exchange_list))
    while again():
        results.append(get_user_value(exchange_list))
    print("")
    print("Thanks for using our currency converter.")
    print("These are your conversions results:")
    for a in results:
        print(f"{a.value} , {a.currency}")
    export_results(results)
    open_file()

main()