import re
import subprocess
import tkinter as tk
from tkinter import ttk

# Mapeia os nomes das lojas aos seus IPs
store_ips = {
    "Alcantara (NRI 2477793)": "201.18.15.185",
    "Americas (RJO 9468484)": "200.223.248.201",
    "Angra dos Reis (ARS 1973443)": "200.223.248.201",
    "Araruama (AMA 1971495)": "201.59.183.41",
    "Arraial do Cabo (ACB 1939007)": "201.18.39.89",
    "Bangu (RJO 9468469)": "201.59.254.145",
    "Bangu 3 (RJO 4328002)": "187.12.190.185",
    "Bangu 4 (RJO 60011154)": "200.165.200.41",
    "Bangu 5 (RJO 60017413)": "187.12.219.185",
    "Barra do Pirai (BPI 1967304)": "200.217.66.65",
    "Barra (RJO 9960984)": "201.59.97.209",
    "Barra Mansa (BMA 1988619)": "187.12.189.169",
    "Bonsucesso 2(RJO 9884703)": "201.59.219.225",
    "Botafogo (RJO 9483627)": "201.59.97.241",
    "Buzios (ARBU 1950266)": "200.223.157.105",
    "Cabo Frio 1 (CBF 2001473)": "201.32.53.225",
    "Cabo Frio 3 (CBF 1987972)": "201.59.118.25",
    "Campo Grande 3 (RJO 9468453)": "200.223.243.249",
    "Campos 1 (CPS 2023393)": "200.216.72.41",
    "Campos 2 (CPS 2012069)": "200.222.52.113",
    "Campos 3 (RJO 9468433)": "200.141.174.161",
    "Carioca (RJO 9468492)": "200.223.248.177",
    "Caxias (DQX 2136086)": "200.222.91.33",
    "Caxias 2 (DQX 2136087)": "201.32.171.105",
    "Center (RJO 9468498)": "200.149.78.217",
    "Centro (RJO 9468507)": "200.216.161.217",
    "Centro 2 (RJO 9468515)": "201.18.144.113",
    "Copacabana 1 (RJO 4288264)": "200.151.150.81",
    "Copacabana 2 (RJO 9575106)": "200.223.233.113",
    "Downtown (RJO 9468522)": " 200.223.251.233",
    "Freguesia (RJO 9469517)": "201.18.5.73",
    "Friburgo (NOF 1957393)": "201.59.97.121",
    "Grande Rio (SMI 2054659)": "201.18.169.217",
    "Guadalupe (RJO 9795889)": "200.151.150.81",
    "ilha (RJO 9469527)": "201.16.5.80",
    "Iguaba (IGGR 1937799)": "200.223.212.201",
    "Iguatemi (RJO 9469525)": "201.18.39.1",
    "Itaborai 3 (IOY 1969540)": "200.223.245.25",
    "Itaborai 4 (IOY 1961875)": "201.59.13.193",
    "Itaguai 2 (IGI 1995756)": "187.41.69.17",
    "Itaperuna 2 (IRA 1954406)": "201.18.17.74",
    "Km32 (NIU 2320457)": "200.151.252.233",
    "LoteXV (BERO 2148799)": "200.222.74.113",
    "Macaé (MCE 2005452)": "201.18.169.1",
    "Macaé 2 (MCE 2005453)": "201.18.239.1",
    "Madureira (RJO 9469531)": "201.18.161.41",
    "Madureira 2 (RJO 9469533)": "200.165.167.169",
    "Madureira 4 (RJO 60020346)": "200.151.121.49",
    "Magé 2 (MGE 1957962)": "200.222.60.153",
    "Marica (MRC 1954282)": "201.18.17.241",
    "Marica 2 (MRC 1958274)": "187.12.189.33",
    "Meier (RJO 9469540)": "200.141.166.193",
    "Mesquita (MSQ 2008766)": "200.222.39.49",
    "Metropolitano (RJO 60002083)": "200.164.226.225",
    "Nilopolis 2 (NLP 2040649)": "200.223.139.201",
    "Niteroi 2 (NRI 2477886)": "200.222.96.81",
    "Niteroi 4": "187.91.166.194",
    "Norte (RJO 9469554)": "200.222.52.225",
    "Nova America (RJO 9469557)": "200.217.26.129",
    "Nova Iguaçu (NIU 2235437)": "201.18.5.153",
    "Nova Iguaçu 2 (NIU 2235439)": "201.18.144.129",
    "Nova Iguaçu 3 (NIU 2235441)": "189.80.34.201",
    "Olinda Ellis (RJO 9469567)": "201.18.231.169",
    "Park Shopping (RJO 9469563)": "201.18.145.145",
    "Penha (RJO 9469565)": "200.222.46.169",
    "Piabeta (PIBT 1948025)": "201.59.136.169",
    "Queimados (QUEA 1981510)": "201.18.239.105",
    "Recreio (RJO 9468459)": "200.223.139.129",
    "Rio bonito (RBT 1939863)": "201.18.145.161",
    "Rio das Ostras (RIOS 1969514)": "200.149.232.233",
    "Rio das Pedras (RJO 9470843)": "201.59.94.1",
    "Santa Cruz (RJO 9470844)": "201.59.118.17",
    "Santa Cruz 2 (RJO 9470847)": "200.223.212.193",
    "Santa Cruz da Serra (DQX 2136288)": "201.59.254.17",
    "São Gonçalo (NRI 2478030)": "201.59.151.57",
    "São Gonçalo 2 (NRI 2478031)": "201.18.145.49",
    "São Gonçalo 4 (NRI 2478033)": "201.59.219.153",
    "São João (SMI 2054661)": "201.59.151.41",
    "São Pedro (SPA 1957508)": "200.216.68.249",
    "Saquarema (SQR 1944161)": "189.109.35.41",
    "Tijuca (RJO 9470891)": "200.222.80.217",
    "Tijuca 2 (RJO 9470897)": "200.223.157.129",
    "Top (NIU 21 2273944)": "200.223.245.161",
    "Teresópolis (TRL 1992564)": "200.222.64.41",
    "Valença (VLC 1958679)": "201.59.97.41",
    "Via Brasil (RJO 21 9470923)": "200.222.65.185",
    "Vilar dos Teles 2 (SMI 2100071)": "200.149.227.201",
    "West 3 (RJO 9470947)": "200.223.251.185",
}

# Dicionário para armazenar o status das lojas
store_status = {store: "Não testado" for store in store_ips}

# Função para realizar o ping e retornar o resultado
def ping_store(ip):
    command = ['ping', '-n', '1', ip]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True, timeout=5)
        ms_match = re.search(r"tempo=(\d+)ms", output, re.IGNORECASE)
        if ms_match:
            ms = ms_match.group(1)
            status = "Online"
        else:
            ms = "N/A"
            status = "Offline"
    except Exception as e:
        ms = "N/A"
        status = "Offline"
    return status, ms

# Função para atualizar o status de uma loja
def update_store_status(store):
    status, ms = ping_store(store_ips[store])
    color = "Blue" if status == "Online" else "red"
    store_status_labels[store].config(text=f"{store}: {status} ({ms} ms)", fg=color)
    store_status[store] = status
    if status == "Offline":
        offline_stores.append(store)
    else:
        if store in offline_stores:
            offline_stores.remove(store)
    update_offline_label()

# Função para atualizar a exibição das lojas offline
def update_offline_label():
    offline_var.set(f"Lojas Offline ({len(offline_stores)}):\n{', '.join(offline_stores)}")

# Função para atualizar os status de todas as lojas
def update_status():
    global current_store_index
    if current_store_index < len(store_ips):
        store = list(store_ips.keys())[current_store_index]
        update_store_status(store)
        current_store_index += 1
        root.after(2000, update_status)
    else:
        current_store_index = 0
        root.after(2000, update_status)

# Função para filtrar as lojas de acordo com o termo de pesquisa
def filter_stores():
    query = search_var.get().lower()
    for store, label in store_status_labels.items():
        if query in store.lower():
            label.pack()
        else:
            label.pack_forget()

# Criar a janela principal
root = tk.Tk()
root.title("Status das Lojas")

# Frame principal
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# Barra de pesquisa
search_var = tk.StringVar()
search_entry = ttk.Entry(main_frame, textvariable=search_var, width=50)
search_entry.grid(row=0, column=0, padx=5, pady=5)
search_var.trace_add("write", lambda *args: filter_stores())

# Frame para listas de lojas online e offline
status_frame = tk.Frame(main_frame)
status_frame.grid(row=1, column=2, padx=5, pady=(1, 10))

# Lista de lojas offline
offline_var = tk.StringVar()
offline_label = tk.Label(status_frame, textvariable=offline_var, wraplength=400, justify="left")
offline_label.pack(side="left", fill="both", expand=True)

# Frame para os rótulos das lojas com barra de rolagem
store_scrollbar = tk.Scrollbar(main_frame, orient="vertical")
store_scrollbar.grid(row=2, column=1, sticky="ns")

store_canvas = tk.Canvas(main_frame, yscrollcommand=store_scrollbar.set)
store_canvas.grid(row=2, column=0, sticky="nsew")

store_frame = tk.Frame(store_canvas)
store_frame.pack(fill="both", expand=True)

store_scrollbar.config(command=store_canvas.yview)
store_canvas.bind('<Configure>', lambda e: store_canvas.configure(scrollregion=store_canvas.bbox("all")))

store_canvas.create_window((0, 0), window=store_frame, anchor="nw")

# Rótulos das lojas
store_status_labels = {}
for store in store_ips:
    store_status_labels[store] = tk.Label(store_frame, text=f"{store}: Não testado", width=50, anchor="w")
    store_status_labels[store].pack(padx=5, pady=2, fill="x")

# Iniciar atualização de status
offline_stores = []
current_store_index = 0
update_status()

# Iniciar loop principal da interface gráfica
root.mainloop()
