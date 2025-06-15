import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar, Text
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="hotel_project"
    )

def show_booking_chart():
    try:
        db = connect_db()
        df = pd.read_sql("SELECT hotel_name FROM table_bookings", db)
        count_df = df['hotel_name'].value_counts().reset_index()
        count_df.columns = ['Hotel', 'Bookings']
        plt.figure(figsize=(8, 5))
        plt.bar(count_df['Hotel'], count_df['Bookings'], color='skyblue')
        plt.xticks(rotation=45)
        plt.title("Bookings Per Hotel")
        plt.xlabel("Hotel Name")
        plt.ylabel("No. of Bookings")
        plt.tight_layout()
        plt.show()
        db.close()
    except Exception as e:
        print("Chart Error:", e)

def view_all_bookings():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT hotel_name, customer_name, mobile, guests, booking_time FROM table_bookings")
        records = cursor.fetchall()
        db.close()
        win = Toplevel()
        win.title("All Bookings")
        win.geometry("500x400")
        scrollbar = Scrollbar(win)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text = Text(win, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text.pack(expand=True, fill='both')
        for row in records:
            text.insert(tk.END, f"Hotel: {row[0]}\nName: {row[1]}\nMobile: {row[2]}\nGuests: {row[3]}\nTime: {row[4]}\n{'-'*40}\n")
        scrollbar.config(command=text.yview)
    except Exception as e:
        print("Error fetching bookings:", e)

def export_to_excel():
    try:
        db = connect_db()
        df = pd.read_sql("SELECT * FROM table_bookings", db)
        filename = f"bookings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False)
        db.close()
        messagebox.showinfo("Exported", f"Exported as {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed\n{e}")

def launch_main_gui(hotel_name):
    try:
        root = tk.Tk()
        root.title(f"{hotel_name} - Booking System")
        root.geometry("400x600")
        room_var = tk.StringVar()
        price_var = tk.StringVar(value="1200")
        name_var = tk.StringVar()
        mobile_var = tk.StringVar()
        guests_var = tk.StringVar()
        result_var = tk.StringVar()
        booking_result = tk.StringVar()

        def calculate_price():
            try:
                total = int(room_var.get()) * int(price_var.get())
                result_var.set(f"Total Price: ₹{total}")
            except:
                result_var.set("Invalid input!")

        def book_table():
            name = name_var.get()
            mobile = mobile_var.get()
            guests = guests_var.get()
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not (name and mobile and guests):
                booking_result.set("Fill all fields.")
                return
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO table_bookings (hotel_name, customer_name, mobile, guests, booking_time) VALUES (%s, %s, %s, %s, %s)",
                    (hotel_name, name, mobile, int(guests), time_now)
                )
                db.commit()
                db.close()
                booking_result.set("Table booked successfully!")
            except Exception as e:
                booking_result.set("Error saving to database.")
                print(e)

        tk.Label(root, text=f"Welcome to {hotel_name}", font=("Arial", 14)).pack(pady=10)
        tk.Label(root, text="Room Booking", font=("Arial", 12)).pack()
        tk.Label(root, text="No. of Rooms:").pack()
        tk.Entry(root, textvariable=room_var).pack()
        tk.Label(root, text="Price per Room:").pack()
        tk.Entry(root, textvariable=price_var).pack()
        tk.Button(root, text="Calculate Price", command=calculate_price).pack(pady=5)
        tk.Label(root, textvariable=result_var, fg="blue").pack()
        tk.Label(root, text="").pack()
        tk.Label(root, text="Table Booking", font=("Arial", 12)).pack(pady=10)
        tk.Label(root, text="Your Name:").pack()
        tk.Entry(root, textvariable=name_var).pack()
        tk.Label(root, text="Mobile Number:").pack()
        tk.Entry(root, textvariable=mobile_var).pack()
        tk.Label(root, text="No. of Guests:").pack()
        tk.Entry(root, textvariable=guests_var).pack()
        tk.Button(root, text="Book Table", command=book_table).pack(pady=5)
        tk.Label(root, textvariable=booking_result, fg="green").pack()
        tk.Button(root, text="View All Bookings", command=view_all_bookings).pack(pady=5)
        tk.Button(root, text="Export Bookings to Excel", command=export_to_excel).pack(pady=5)
        tk.Button(root, text="Show Booking Chart", command=show_booking_chart).pack(pady=10)
        root.mainloop()
    except Exception as e:
        print("Error in GUI:", e)

hotels = [
    "Hotel Gurukrupa", "Hotel A1", "Hotel Sai Palace", "Hotel Krishna",
    "Hotel Yashraj", "Hotel Food City", "Hotel Prabhat", "Hotel Samrat",
    "Hotel Galaxy", "Hotel Delight"
]

def start_console():
    print("Welcome to Kalyan Hotel Booking")
    print("Available Hotels:\n")
    for i, h in enumerate(hotels, 1):
        print(f"{i}. {h}")
    try:
        choice = int(input("\nEnter your choice (1-10): "))
        if 1 <= choice <= 10:
            selected_hotel = hotels[choice - 1]
            print(f"\nYou selected: {selected_hotel}")
            print("Launching GUI...")
            launch_main_gui(selected_hotel)
        else:
            print("Invalid choice. Run again.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    start_console()
