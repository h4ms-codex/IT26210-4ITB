import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, scrolledtext
import requests

def fetch_ip_data():
    try:
        response = requests.get("https://ipapi.co/json/", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch IP info:\n{e}")
        return None

def display_selected_info():
    data = fetch_ip_data()
    if not data:
        return

    output = []

    if var_ip.get():
        ip = data.get("ip")
        version = "IPv6" if ":" in ip else "IPv4"
        output.append(f"Public IP Address: {ip} ({version})")

    if var_location.get():
        city = data.get("city")
        region = data.get("region")
        country = data.get("country_name")
        country_code = data.get("country")
        output.append(f"Location: {city}, {region}, {country} ({country_code})")

    if var_coords.get():
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        output.append(f"Latitude / Longitude: {latitude}, {longitude}")

    if var_timezone.get():
        timezone = data.get("timezone")
        output.append(f"Timezone: {timezone}")

    if var_isp.get():
        isp = data.get("org")
        asn = data.get("asn")
        output.append(f"ISP / Provider: {isp}")
        output.append(f"ASN: {asn}")

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "\n".join(output))

def save_data_to_file():
    data = fetch_ip_data()
    if not data:
        return

    output = []

    if var_ip.get():
        ip = data.get("ip")
        version = "IPv6" if ":" in ip else "IPv4"
        output.append(f"Public IP Address: {ip} ({version})")

    if var_location.get():
        city = data.get("city")
        region = data.get("region")
        country = data.get("country_name")
        country_code = data.get("country")
        output.append(f"Location: {city}, {region}, {country} ({country_code})")

    if var_coords.get():
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        output.append(f"Latitude / Longitude: {latitude}, {longitude}")

    if var_timezone.get():
        timezone = data.get("timezone")
        output.append(f"Timezone: {timezone}")

    if var_isp.get():
        isp = data.get("org")
        asn = data.get("asn")
        output.append(f"ISP / Provider: {isp}")
        output.append(f"ASN: {asn}")

    if not output:
        messagebox.showwarning("No Data", "No info selected to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Save IP Info As"
    )

    if not file_path:
        return

    try:
        with open(file_path, "w") as f:
            f.write("\n".join(output))
        messagebox.showinfo("Saved", f"Selected info saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

# ----- GUI Setup -----
root = tk.Tk()
root.title("IP Info Viewer")
root.geometry("500x500")
root.resizable(False, False)

var_ip = tk.BooleanVar(value=True)
var_location = tk.BooleanVar()
var_coords = tk.BooleanVar()
var_timezone = tk.BooleanVar()
var_isp = tk.BooleanVar()

tk.Label(root, text="Select information to display:", font=("Arial", 12, "bold")).pack(pady=10)

checkbox_frame = tk.Frame(root)
checkbox_frame.pack()

tk.Checkbutton(checkbox_frame, text="IP Address", variable=var_ip).grid(row=0, column=0, sticky="w")
tk.Checkbutton(checkbox_frame, text="Location", variable=var_location).grid(row=1, column=0, sticky="w")
tk.Checkbutton(checkbox_frame, text="Coordinates", variable=var_coords).grid(row=2, column=0, sticky="w")
tk.Checkbutton(checkbox_frame, text="Timezone", variable=var_timezone).grid(row=3, column=0, sticky="w")
tk.Checkbutton(checkbox_frame, text="ISP / ASN", variable=var_isp).grid(row=4, column=0, sticky="w")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Fetch Info", command=display_selected_info, width=20).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Save to File", command=save_data_to_file, width=20).grid(row=0, column=1, padx=5)

output_text = scrolledtext.ScrolledText(root, width=60, height=15, wrap=tk.WORD)
output_text.pack(pady=10)

root.mainloop()

