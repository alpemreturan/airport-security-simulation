import tkinter as tk
from tkinter import messagebox
from models.passenger import Passenger
from models.stack import Stack
from models.queue import Queue
from models.linkedlist import LinkedList
from utils.possibility import generate_random_baggage
import json
import os
import random
import csv


class SecuritySimulationGUI:
    ID_RANGE = (1, 99)

    def __init__(self, root):
        self.root = root
        self.root.title("Baggage Security Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_rowconfigure(1, weight=3)  
        self.root.grid_rowconfigure(2, weight=2) 
        self.root.grid_rowconfigure(3, weight=1)  
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        title_label = tk.Label(
            self.root,
            text="Baggage Security Simulator",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="black"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.passenger_queue = Queue()
        self.baggage_stack = Stack()
        self.blacklist = LinkedList()
        self.log = []
        self.clean_passengers = []
        self.alarm_count = 0
        self.caught_blacklist = []
        self.suspicious_passengers = []
        self.passenger_counter = 0
        self.used_ids = set()
        self.max_passengers = self.ID_RANGE[1] - self.ID_RANGE[0] + 1

        self.load_blacklist()

        self.create_queue_panel()
        self.create_stack_panel()
        self.create_blacklist_panel()
        self.create_log_panel()
        self.create_control_panel()

    def load_blacklist(self):
        file_path = os.path.join(os.path.dirname(__file__), "data", "black_list.json")
        with open(file_path, "r") as file:
            blacklist_data = json.load(file)
            for passenger_id in blacklist_data:
                self.blacklist.add(int(passenger_id))

    def create_queue_panel(self):
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(frame, text="Passenger Queue", font=("Arial", 16), bg="#f0f0f0").pack()
        self.queue_listbox = tk.Listbox(frame, height=15, width=30, font=("Arial", 14))
        self.queue_listbox.pack(fill=tk.BOTH, expand=True)

    def create_stack_panel(self):
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        tk.Label(frame, text="Baggage Stack", font=("Arial", 16), bg="#f0f0f0").pack()
        self.stack_listbox = tk.Listbox(frame, height=15, width=30, font=("Arial", 14))
        self.stack_listbox.pack(fill=tk.BOTH, expand=True)

    def create_blacklist_panel(self):
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        tk.Label(frame, text="Blacklist", font=("Arial", 16), bg="#f0f0f0").pack()
        self.blacklist_listbox = tk.Listbox(frame, height=15, width=30, font=("Arial", 14))
        for passenger in self.blacklist.to_list():
            self.blacklist_listbox.insert(tk.END, f"ID: {passenger}")
        self.blacklist_listbox.pack(fill=tk.BOTH, expand=True)

    def create_log_panel(self):
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        tk.Label(frame, text="Log", font=("Arial", 16), bg="#f0f0f0").pack()
        self.log_text = tk.Text(frame, height=10, width=100, font=("Arial", 14))
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def create_control_panel(self):
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)
        frame.grid_columnconfigure(4, weight=1)

        button_font = ("Arial", 14)
        tk.Button(frame, text="New Passenger", font=button_font, command=self.create_passenger).grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=5)
        tk.Button(frame, text="Load Data", font=button_font, command=self.load_data).grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=5)
        tk.Button(frame, text="Start Simulation", font=button_font, command=self.start_simulation).grid(row=0, column=2, padx=10, pady=10, ipadx=10, ipady=5)
        tk.Button(frame, text="Clear Logs", font=button_font, command=self.clear_logs).grid(row=0, column=3, padx=10, pady=10, ipadx=10, ipady=5)
        tk.Button(frame, text="Show Report", font=button_font, command=self.show_report).grid(row=0, column=4, padx=10, pady=10, ipadx=10, ipady=5)

    def create_passenger(self):
        if len(self.used_ids) >= self.max_passengers:
            messagebox.showinfo("Warning", "All IDs have been used! No more passengers can be added.")
            return

        random_id = random.randint(*self.ID_RANGE)
        while random_id in self.used_ids:
            random_id = random.randint(*self.ID_RANGE)

        self.used_ids.add(random_id)
        self.passenger_counter += 1
        passenger_display_name = f"Passenger #{self.passenger_counter}"

        baggage = generate_random_baggage()
        passenger = Passenger(random_id, baggage)
        self.passenger_queue.enqueue(passenger)

        self.queue_listbox.insert(tk.END, passenger_display_name)
        self.log_event(f"{passenger_display_name} added to queue.")

    def load_data(self):
        remaining_slots = self.max_passengers - len(self.used_ids)
        if remaining_slots <= 0:
            messagebox.showinfo("Warning", "All IDs have been used! No more passengers can be added.")
            return

        for _ in range(min(30, remaining_slots)):
            self.create_passenger()
        self.log_event(f"{min(30, remaining_slots)} Passenger loaded successfully.")

    def start_simulation(self):
        if self.passenger_queue.is_empty():
            messagebox.showinfo("Warning, There are no passengers in the queue!")
            return

        self.current_passenger = self.passenger_queue.dequeue()
        self.queue_listbox.delete(0)
        self.passenger_display_name = f"Passenger #{self.passenger_counter - len(self.passenger_queue.to_list())}"
        self.log_event(f"{self.passenger_display_name} arrived at the checkpoint.")
    
        self.stack_listbox.delete(0, tk.END)
        while not self.baggage_stack.is_empty():
            self.baggage_stack.pop()

        self.current_baggage = iter(self.current_passenger.baggage)
        self.baggage_scan()

    def baggage_scan(self):
        try:
            item = next(self.current_baggage)
            self.baggage_stack.push(item)
            self.stack_listbox.insert(0, item)

            if item in ["Knife", "Gun", "Explosive"]:
                self.stack_listbox.itemconfig(0, {'background': '#FF5A5A'})
                self.log_event(f"ALARM! Dangerous material found: {item}")
                self.alarm_count += 1

            self.root.after(1000, self.baggage_scan)

        except StopIteration:
            self.log_event(f"{self.passenger_display_name} Baggage screening has been completed.")
            self.is_in_blacklist()

    def is_in_blacklist(self):
        is_blacklisted = self.blacklist.search(self.current_passenger.passenger_id)
        if is_blacklisted:
            self.current_passenger.risk_score += 1
            self.caught_blacklist.append(self.current_passenger.passenger_id)
            self.log_event(f"{self.passenger_display_name} found on the blacklist! Risk score increased.")

        if is_blacklisted or any(item in ["Knife", "Gun", "Explosive"] for item in self.current_passenger.baggage):
            self.suspicious_passengers.append(self.current_passenger.passenger_id)
            self.log_event(f"{self.passenger_display_name} marked as suspicious.")
        else:
            self.clean_passengers.append(self.current_passenger.passenger_id)
            self.log_event(f"{self.passenger_display_name} passed the scan.")

    def clear_logs(self):
        self.log = []
        self.log_text.delete(1.0, tk.END)

    def log_event(self, event):
        self.log.append(event)
        self.log_text.insert(tk.END, event + "\n")
        self.log_text.see(tk.END)

    def show_report(self):
        total_passengers = len(self.clean_passengers) + len(self.suspicious_passengers) + len(self.passenger_queue.to_list())

        for passenger_id in self.caught_blacklist:
            if passenger_id not in self.clean_passengers and passenger_id not in self.suspicious_passengers:
                total_passengers += 1

        stack_count = len(self.caught_blacklist) + len(self.suspicious_passengers)

        report_data = {
            "Total Passengers": total_passengers,
            "Those Alarmed": self.alarm_count,
            "Clear Passes": ', '.join(map(str, self.clean_passengers)),
            "Caught on the Black List": ', '.join(map(str, self.caught_blacklist)),
            "Number of Baggage Taken to Stack": stack_count
        }

        messagebox.showinfo(
            "Report",
            f"Total Passengers: {report_data['Total Passengers']}\n"
            f"Those Alarmed: {report_data['Those Alarmed']}\n"
            f"Clear Passes: {report_data['Clear Passes']}\n"
            f"Caught on the Black List: {report_data['Caught on the Black List']}\n"
            f"Number of Baggage Taken to Stack: {report_data['Number of Baggage Taken to Stack']}"
        )

        csv_file_path = os.path.join(os.path.dirname(__file__), "report.csv")
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Report Title", "Value"])
            for key, value in report_data.items():
                writer.writerow([key, value])

        self.log_event(f"The report was saved to the file 'report.csv'.")