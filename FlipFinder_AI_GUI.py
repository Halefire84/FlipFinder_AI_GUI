import tkinter as tk
from tkinter import ttk, messagebox
from flipfinder_core import load_inventory, save_inventory
from ai_value_estimator import estimate_item_value

class FlipFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlipFinder AI - Resale Assistant")
        self.root.geometry("650x500")
        
        self.inventory = load_inventory()
        
        # Title Header
        title_label = ttk.Label(root, text="FlipFinder AI Dashboard", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Input Frame
        input_frame = ttk.LabelFrame(root, text=" Add & Evaluate Inventory Item ")
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(input_frame, text="Item Name:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.name_entry = ttk.Entry(input_frame, width=28)
        self.name_entry.grid(row=0, column=1, padx=8, pady=8)
        
        ttk.Label(input_frame, text="Acquisition Cost ($):").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.cost_entry = ttk.Entry(input_frame, width=28)
        self.cost_entry.grid(row=1, column=1, padx=8, pady=8)
        
        estimate_btn = ttk.Button(input_frame, text="Run AI Estimate & Save", command=self.add_item)
        estimate_btn.grid(row=2, column=0, columnspan=2, pady=12)
        
        # Inventory Display Table
        list_frame = ttk.LabelFrame(root, text=" Tracked Inventory & Valuations ")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tree = ttk.Treeview(list_frame, columns=("Name", "Cost", "Est Value", "Score"), show="headings")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Cost", text="Cost ($)")
        self.tree.heading("Est Value", text="Est. Value ($)")
        self.tree.heading("Score", text="Deal Score")
        
        self.tree.column("Name", width=180)
        self.tree.column("Cost", width=80, anchor="center")
        self.tree.column("Est Value", width=100, anchor="center")
        self.tree.column("Score", width=90, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.refresh_table()

    def add_item(self):
        name = self.name_entry.get().strip()
        try:
            cost = float(self.cost_entry.get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric value for the cost.")
            return
            
        if not name:
            messagebox.showerror("Input Error", "Item name cannot be empty.")
            return
            
        valuation = estimate_item_value(name, cost)
        item_data = {
            "name": name,
            "cost": cost,
            "est_value": valuation["avg_price"],
            "score": valuation["deal_score"]
        }
        
        self.inventory.append(item_data)
        save_inventory(self.inventory)
        self.refresh_table()
        
        self.name_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)
        messagebox.showinfo("Analysis Complete", f"Estimated Market Value: ${valuation['avg_price']}\nDeal Rating: {valuation['deal_score']}")

    def refresh_table(self):
        for row in self.tree.getchildren():
            self.tree.delete(row)
        for item in self.inventory:
            self.tree.insert("", "end", values=(item["name"], f"{item['cost']:.2f}", f"{item['est_value']:.2f}", item["score"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = FlipFinderApp(root)
    root.mainloop()
