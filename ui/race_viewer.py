import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

class RaceViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Horse Racing Analyzer")
        self.root.geometry("1000x800")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create treeview for races
        self.tree = ttk.Treeview(self.main_frame, columns=('Time', 'Course', 'Race Name', 'Class', 'Distance', 'Forecast', 'Tip'), show='headings')
        
        # Define headings
        self.tree.heading('Time', text='Time')
        self.tree.heading('Course', text='Course')
        self.tree.heading('Race Name', text='Race Name')
        self.tree.heading('Class', text='Class')
        self.tree.heading('Distance', text='Distance')
        self.tree.heading('Forecast', text='Forecast')
        self.tree.heading('Tip', text='Tip')
        
        # Set column widths
        self.tree.column('Time', width=80)
        self.tree.column('Course', width=100)
        self.tree.column('Race Name', width=200)
        self.tree.column('Class', width=80)
        self.tree.column('Distance', width=100)
        self.tree.column('Forecast', width=150)
        self.tree.column('Tip', width=100)
        
        # Add treeview to grid
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Add buttons frame
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Add refresh button
        self.refresh_button = ttk.Button(self.buttons_frame, text="Refresh Race Data", command=self.refresh_data)
        self.refresh_button.grid(row=0, column=0, padx=5)
        
        # Add status label
        self.status_label = ttk.Label(self.buttons_frame, text="")
        self.status_label.grid(row=0, column=1, padx=5)
        
        # Load data
        self.refresh_data()
        
    def refresh_data(self):
        try:
            # Get race data (this will be replaced with API call)
            data = self.get_race_data()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add new items
            for race in data:
                self.tree.insert('', 'end', values=(
                    race['off_time'],
                    race['course'],
                    race['race_name'],
                    race['race_class'],
                    race['distance_round'],
                    race['betting_forecast'],
                    race['tip']
                ))
            
            self.status_label.config(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            
    def get_race_data(self):
        try:
            # Get API credentials
            username = os.getenv("RACING_API_USERNAME")
            password = os.getenv("RACING_API_PASSWORD")
            base_url = os.getenv("RACING_API_BASE_URL")
            
            # Create auth header
            auth = (username, password)
            
            # Get race cards
            url = f"{base_url}/v1/racecards/free"
            params = {
                'region_codes': ['gb', 'ire']
            }
            
            response = requests.get(url, auth=auth, params=params)
            response.raise_for_status()
            
            return response.json()['racecards']
            
        except Exception as e:
            print(f"Error fetching race data: {e}")
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = RaceViewer(root)
    root.mainloop()
