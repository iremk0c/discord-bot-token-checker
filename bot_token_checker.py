import requests
import os
import time

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_banner():
    os.system("clear" if os.name == "posix" else "cls")  
    print(f"""{RED}
██     ██ ███████ ███████ ███████ ██    ██
██     ██ ██      ██      ██      ██    ██
██  █  ██ █████   ███████ ███████  ██████
██ ███ ██ ██           ██      ██    ██
 ███ ███  ███████ ███████ ███████    ██
{YELLOW}Bot Token Checker by Wessy{RESET}
""")

def check_bot_token(bot_token):
    print(f"{CYAN}Bot tokeniniz kontrol ediliyor...{RESET}")
    url = "https://discord.com/api/v10/applications/@me"
    headers = {"Authorization": f"Bot {bot_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        bot_data = response.json()
        verified_status = bot_data.get("verified", "Bilinmiyor")
        owner_id = bot_data.get("owner", {}).get("id", "Bilinmiyor")
        avatar = bot_data.get("icon", None)
        avatar_url = f"https://cdn.discordapp.com/app-icons/{bot_data['id']}/{avatar}.png" if avatar else "Avatar yok"

        print(f"\n{GREEN}Geçerli Bot Tokeni.{RESET}")
        print(f"\n{BLUE}Bot Bilgileri:{RESET}")
        print(f" Bot Adı: {bot_data['name']}")
        print(f" Bot ID: {bot_data['id']}")
        print(f" Doğrulandı mı?: {'Evet' if verified_status is True else 'Hayır' if verified_status is False else 'Bilinmiyor'}")
        print(f" Sahip ID: {owner_id}")
        print(f" Avatar: {avatar_url}")
        
        print(f"\n{BLUE}Botun Sunucularına Bakılıyor...{RESET}")
        check_bot_guilds(bot_token)
        check_bot_permissions(bot_token)

    elif response.status_code == 401:
        print(f"\n{RED}Geçersiz Bot Token. Lütfen doğru bir token gir.{RESET}")
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 5))  
        print(f"\n{YELLOW}Rate limit aşıldı. Lütfen {retry_after} saniye bekleyin.{RESET}")
        time.sleep(retry_after)
    else:
        print(f"\n{YELLOW}Hata Kodu: {response.status_code} - {response.text}{RESET}")

def check_bot_guilds(bot_token):
    url = "https://discord.com/api/v10/users/@me/guilds"
    headers = {"Authorization": f"Bot {bot_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        guilds = response.json()
        print(f"\n{BLUE}Botun Katıldığı Sunucular:{RESET}")
        if not guilds:
            print(" Sunucu bulunamadı.")
        else:
            for guild in guilds[:5]:  
                print(f" {guild['name']} - ID: {guild['id']}")
    else:
        print(f"{RED}Sunucu bilgileri alınamadı.{RESET}")

def check_bot_permissions(bot_token):
    url = "https://discord.com/api/v10/users/@me/guilds"
    headers = {"Authorization": f"Bot {bot_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        guilds = response.json()
        print(f"\n{YELLOW}Yetkilere Sahip Olduğu Sunucular:{RESET}")
        has_admin = False

        for guild in guilds:
            permissions = int(guild["permissions"])
            if permissions == 2147483647:  
                print(f" {guild['name']} - ID: {guild['id']} (Admin Yetkisi)")
                has_admin = True
        
        if not has_admin:
            print(" Yetkili olduğu sunucu bulunamadı.")

    else:
        print(f"{RED}Yetki bilgileri alınamadı.{RESET}")

if __name__ == "__main__":
    print_banner()
    
    bot_token = input(CYAN + "Kontrol edilecek Bot Tokenini gir: " + RESET)
    check_bot_token(bot_token.strip())
