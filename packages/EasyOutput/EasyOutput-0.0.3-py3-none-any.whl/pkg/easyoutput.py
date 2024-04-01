from colorama import Fore, Style

def Info(message):
    print(f"{Fore.BLUE + Style.BRIGHT}Info{Style.RESET_ALL}: {message}")

def Error(message):
    print(f"{Fore.RED}Error{Style.RESET_ALL}: {Fore.YELLOW + message + Style.RESET_ALL}")

def Connection_Error(message):
    print(f"{Fore.RED}Connection Error{Style.RESET_ALL}: {Fore.YELLOW + message + Style.RESET_ALL}")

def Success(message):
    print(f"{Fore.GREEN + Style.BRIGHT}Success{Style.RESET_ALL}: {message}")
    
def Successful_Connection(message):
    print(f"{Fore.GREEN + Style.BRIGHT}Successful Connection{Style.RESET_ALL}: {message}")
    
def Note(message):
    print(f"{Fore.YELLOW}Note{Style.RESET_ALL}: {message}")
    
def Wait(message):
    print(f"{Fore.LIGHTWHITE_EX}Wait{Style.RESET_ALL}: {message}")
    
def Title(title):
    print(f"=== {Fore.GREEN + Style.BRIGHT + title + Style.RESET_ALL} ===")