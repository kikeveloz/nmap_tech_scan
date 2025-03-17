# WebRecon - Escaneo de Tecnologías y Puertos con Nmap

## 🛠️ Descripción

`nmap_tech_scan.py` es un script automatizado en Python para realizar **reconocimiento web y escaneo de puertos**. Este script:
- Obtiene la **IP real** de un dominio mediante `nslookup`.
- Detecta si el dominio está detrás de un **CDN** y advierte al usuario.
- Extrae **tecnologías web** del sitio utilizando `WhatWeb`.
- Realiza un **escaneo de puertos abiertos** con `Nmap` (`-p- --open -n -Pn -sS`).
- Filtra los puertos abiertos y ejecuta un segundo escaneo detallado con `Nmap -sVC`.

Este script es ideal para **pentesters, investigadores de seguridad y OSINT analysts**.

---

## 🚀 **Requisitos**
Antes de ejecutar el script, asegúrate de tener los siguientes paquetes instalados en tu **Kali Linux**:

📌 **Herramientas necesarias:**
```bash
sudo apt install whatweb nmap dnsutils -y
pip install python-nmap colorama

📌 **Ejecución:**
```bash
python3 nmap_tech_scan.py

🔹 Ingrese la URL a evaluar (sin http/https):ejemplo.com
