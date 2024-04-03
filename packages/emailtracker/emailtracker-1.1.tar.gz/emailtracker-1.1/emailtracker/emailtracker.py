import re
import requests
import tkinter as tk
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk

def get_ip_info(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()
    return data

def extract_info(header_text):
    # Regular expressions to match relevant fields in the header
    sender_pattern = re.compile(r"From:\s*(.*?)\s*<.*?>")
    ip_pattern = re.compile(r"Received:.*?\[([^\]]+)\]")
    ip_address_pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
    
    # Extract sender and IP address
    sender_match = sender_pattern.search(header_text)
    ip_matches = ip_pattern.findall(header_text)
    
    if sender_match and ip_matches:
        sender = sender_match.group(1)
        ip_address = ip_address_pattern.search(ip_matches[-1]).group(1)
        
        # Get IP information using ip-api.com
        try:
            ip_info = get_ip_info(ip_address)
            return {
                "Sender": sender,
                "IP Address": ip_address,
                "Country": ip_info.get("country", ""),
                "Region & City": f"{ip_info.get('regionName', '')}, {ip_info.get('city', '')}",
                "Coordinates": f"{ip_info.get('lat', '')}, {ip_info.get('lon', '')}",
                "ISP": ip_info.get("isp", ""),
                "Local Time": ip_info.get("timezone", ""),
                "Domain": ip_info.get("as", ""),
                "Net Speed": ip_info.get("as", ""),
                "IDD & Area Code": ip_info.get("org", ""),
                "ZIP Code": ip_info.get("zip", ""),
                "Usage Type": ip_info.get("usageType", ""),
                "ASN": ip_info.get("as", ""),
                # Add more fields as needed
            }
        except Exception as e:
            print(f"Error fetching IP information: {e}")
            return None
    else:
        return None

def extract():
    def extract_and_display():
        header_text = text_box.get("1.0", tk.END)
        info = extract_info(header_text)
        
        if info:
            result_text.delete("1.0", tk.END)
            for key, value in info.items():
                result_text.insert(tk.END, f"{key:<20}: {value}\n")
        else:
            CTkMessagebox(title="Error", message="Unable to extract information from the email header", icon="warning", option_1="ok")

    # Create the main window
    root = ctk.CTk()
    root.title("Email Tracker By Korishee")
    root.geometry("700x650+500+0")

    # Create labels for text boxes
    label = ctk.CTkLabel(root, text="KORISHEE THE CYBERMASTER", font=("Comic Sans MS", 18 , "bold"))
    label.pack()
    input_label = ctk.CTkLabel(root, text="Enter your Email Header:")
    input_label.pack()

    # Create a text box for input with placeholder text
    text_box = ctk.CTkTextbox(root, width=800, height=250)
    text_box.pack(pady=5)

    # Create a button to extract data
    extract_button = ctk.CTkButton(root, text="Extract Data",fg_color="red",hover_color="green", command=extract_and_display)
    extract_button.pack()

    # Create a label for the result text box
    result_label = ctk.CTkLabel(root, text="Extracted information:")
    result_label.pack()

    # Create a text box for displaying results with placeholder text
    result_text = ctk.CTkTextbox(root, width=800, height=400)
    result_text.pack(pady=5)

    # Run the GUI
    root.mainloop()

# Call the extract function to execute the code
if __name__ == "__main__":
    extract()
