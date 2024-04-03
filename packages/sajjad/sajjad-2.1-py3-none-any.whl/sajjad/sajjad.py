from colorama import Fore
class get_number:
    def add(num1,num2):
        if str(type(num1)) == str(type(num2)) == "<class 'int'>":
            print(num1 + num2)
        else:
            print(Fore.RED+"you shoud type numbers"+Fore.RESET)