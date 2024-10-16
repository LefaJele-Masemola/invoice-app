import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
from datetime import datetime

class Invoice:
    def __init__(self, invoice_number, customer_name):
        self.invoice_number = invoice_number
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.customer_name = customer_name
        self.items = []
        self.subtotal = 0
        self.tax_rate = 0.15  # Assuming a 15% tax rate
        self.total = 0

    def add_item(self, description, quantity, unit_price):
        total_price = quantity * unit_price
        self.items.append({
            "description": description,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": total_price
        })
        self.subtotal += total_price
        self.total = self.subtotal * (1 + self.tax_rate)

    def generate_invoice(self, filename="invoice.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt=f"Invoice Number: {self.invoice_number}", ln=True)
        pdf.cell(200, 10, txt=f"Date: {self.date}", ln=True)
        pdf.cell(200, 10, txt=f"Customer Name: {self.customer_name}", ln=True)
        
        pdf.cell(200, 10, txt="", ln=True)
        pdf.cell(200, 10, txt="Items:", ln=True)
        for item in self.items:
            pdf.cell(200, 10, txt=f"- {item['description']} (x{item['quantity']}): R{item['unit_price']} each, Total: R{item['total_price']}", ln=True)
        
        pdf.cell(200, 10, txt="", ln=True)
        pdf.cell(200, 10, txt=f"Subtotal: R{self.subtotal}", ln=True)
        pdf.cell(200, 10, txt=f"Tax (15%): R{self.subtotal * self.tax_rate}", ln=True)
        pdf.cell(200, 10, txt=f"Total: R{self.total}", ln=True)
        
        pdf.output(filename)
        messagebox.showinfo("Success", f"Invoice saved as {filename}")

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Generator")
        
        self.invoice_number = tk.StringVar()
        self.customer_name = tk.StringVar()
        self.description = tk.StringVar()
        self.quantity = tk.IntVar()
        self.unit_price = tk.DoubleVar()
        
        self.invoice = None
        
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Invoice Number:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.invoice_number).grid(row=0, column=1)
        
        tk.Label(self.root, text="Customer Name:").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.customer_name).grid(row=1, column=1)
        
        tk.Label(self.root, text="Item Description:").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.description).grid(row=2, column=1)
        
        tk.Label(self.root, text="Quantity:").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.quantity).grid(row=3, column=1)
        
        tk.Label(self.root, text="Unit Price:").grid(row=4, column=0)
        tk.Entry(self.root, textvariable=self.unit_price).grid(row=4, column=1)
        
        tk.Button(self.root, text="Add Item", command=self.add_item).grid(row=5, column=0, columnspan=2)
        tk.Button(self.root, text="Generate Invoice", command=self.generate_invoice).grid(row=6, column=0, columnspan=2)
    
    def add_item(self):
        if not self.invoice:
            self.invoice = Invoice(self.invoice_number.get(), self.customer_name.get())
        
        self.invoice.add_item(self.description.get(), self.quantity.get(), self.unit_price.get())
        messagebox.showinfo("Success", "Item added to invoice")
    
    def generate_invoice(self):
        if not self.invoice:
            messagebox.showerror("Error", "No items in the invoice")
        else:
            filename = f"invoice_{self.invoice_number.get()}.pdf"
            self.invoice.generate_invoice(filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
