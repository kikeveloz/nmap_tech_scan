import subprocess
import re
import nmap
from colorama import Fore, Style, init

# Inicializar colorama para colores en la terminal
init(autoreset=True)

# Función para obtener la IP real del dominio usando nslookup
def obtener_ip(dominio):
    try:
        resultado = subprocess.run(["nslookup", dominio], capture_output=True, text=True)
        salida = resultado.stdout.split("\n")

        ips = []
        grabando = False

        for linea in salida:
            if "Non-authoritative answer:" in linea:
                grabando = True  # Solo tomamos IPs después de esta línea
                continue
            if grabando:
                match = re.search(r"Address:\s+([0-9.]+)", linea)
                if match:
                    ips.append(match.group(1))

        if len(ips) > 1:
            print(Fore.YELLOW + f"\n[⚠] Se detectaron múltiples IPs para {dominio}. Es posible que esté detrás de un CDN.")
            print(Fore.YELLOW + "[⚠] Busca la IP real con OSINT antes de continuar." + Style.RESET_ALL)
            print(Fore.YELLOW + f"IPs detectadas: {', '.join(ips)}" + Style.RESET_ALL)
            return None
        elif ips:
            return ips[0]  # Retorna la única IP real encontrada
        else:
            print(Fore.RED + "[!] No se encontró ninguna IP para el dominio." + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Fore.RED + f"[!] Error al obtener la IP: {e}" + Style.RESET_ALL)
        return None

# Función para detectar tecnologías usando WhatWeb
def detectar_tecnologias(dominio):
    try:
        print(Fore.YELLOW + f"\n[+] Escaneando tecnologías en {dominio} con WhatWeb..." + Style.RESET_ALL)
        
        resultado = subprocess.run(["whatweb", dominio], capture_output=True, text=True)
        
        if resultado.stdout:
            print(Fore.CYAN + "\n[+] Tecnologías detectadas:" + Style.RESET_ALL)
            print(Fore.GREEN + resultado.stdout.strip() + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "[!] No se detectaron tecnologías con WhatWeb." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] Error al ejecutar WhatWeb: {e}" + Style.RESET_ALL)

# Función para escanear la IP con Nmap y guardar en archivo
def escanear_nmap(ip):
    archivo_salida = "nmap_resultado.txt"
    
    try:
        print(Fore.YELLOW + f"\n[+] Escaneando {ip} con Nmap (todos los puertos abiertos)..." + Style.RESET_ALL)

        # Ejecutar Nmap con -p- --open -n -Pn -sS y guardar el resultado en un archivo
        subprocess.run(["nmap", "-p-", "--open", "-n", "-Pn", "-sS", ip, "-oN", archivo_salida], check=True)

        print(Fore.GREEN + f"[+] Escaneo completado. Resultado guardado en {archivo_salida}" + Style.RESET_ALL)

        # Extraer puertos abiertos del archivo
        return extraer_puertos_abiertos(archivo_salida)

    except Exception as e:
        print(Fore.RED + f"[!] Error al ejecutar Nmap: {e}" + Style.RESET_ALL)
        return []

# Función para extraer puertos abiertos del archivo de resultados de Nmap
def extraer_puertos_abiertos(archivo):
    puertos_abiertos = []
    
    try:
        with open(archivo, "r") as file:
            for linea in file:
                match = re.search(r"(\d+)/tcp\s+open", linea)
                if match:
                    puertos_abiertos.append(match.group(1))
        
        if puertos_abiertos:
            print(Fore.CYAN + f"\n[+] Puertos abiertos detectados: {', '.join(puertos_abiertos)}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "[!] No se encontraron puertos abiertos." + Style.RESET_ALL)

        return puertos_abiertos
    except Exception as e:
        print(Fore.RED + f"[!] Error al extraer puertos: {e}" + Style.RESET_ALL)
        return []

# Función para escanear los puertos específicos con Nmap -sVC
def escanear_puertos_detallado(ip, puertos):
    if not puertos:
        print(Fore.YELLOW + "[!] No hay puertos para escanear con Nmap -sVC." + Style.RESET_ALL)
        return

    try:
        print(Fore.YELLOW + f"\n[+] Escaneando servicios y versiones en {ip} con Nmap -sVC..." + Style.RESET_ALL)

        # Ejecutar Nmap -sVC con los puertos abiertos detectados
        subprocess.run(["nmap", "-p", ",".join(puertos), "-sVC", ip], check=True)
    
    except Exception as e:
        print(Fore.RED + f"[!] Error al ejecutar Nmap -sVC: {e}" + Style.RESET_ALL)

# Función principal
def main():
    dominio = input(Fore.CYAN + "\n🔹 Ingrese la URL a evaluar (sin http/https): " + Style.RESET_ALL).strip()

    ip = obtener_ip(dominio)
    if not ip:
        return

    print(Fore.GREEN + f"\n[+] IP obtenida: {ip}" + Style.RESET_ALL)

    detectar_tecnologias(dominio)

    puertos_abiertos = escanear_nmap(ip)

    escanear_puertos_detallado(ip, puertos_abiertos)

# Ejecutar script
if __name__ == "__main__":
    main()
