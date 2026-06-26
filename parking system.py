from flask import Flask, request
import heapq
from datetime import datetime
import math

app = Flask(__name__)

class ParkingSystem:
    def __init__(self, total_slots):
        self.available_slots = list(range(1, total_slots + 1))
        heapq.heapify(self.available_slots)
        self.records = {}

    def park(self, username, vehicle_number):
        if not self.available_slots:
            return "No slots available!", None

        if vehicle_number in self.records:
            return "Vehicle already parked!", None

        entry_obj = datetime.now()
        entry_time = entry_obj.strftime("%d-%m-%Y %I:%M:%S %p")

        slot = heapq.heappop(self.available_slots)

        self.records[vehicle_number] = {
            "username": username,
            "slot": slot,
            "entry_time": entry_time,
            "entry_obj": entry_obj
        }

        return f"Slot {slot} booked!", None

    def exit(self, vehicle_number):
        if vehicle_number not in self.records:
            return "Vehicle not found!", None

        data = self.records.pop(vehicle_number)

        exit_obj = datetime.now()
        exit_time = exit_obj.strftime("%d-%m-%Y %I:%M:%S %p")

        # ✅ REAL PARKING BILLING
        duration = (exit_obj - data["entry_obj"]).total_seconds() / 3600
        hours = math.ceil(duration)
        amount = hours * 100

        heapq.heappush(self.available_slots, data["slot"])

        bill = {
            "name": data["username"],
            "vehicle": vehicle_number,
            "slot": data["slot"],
            "entry": data["entry_time"],
            "exit": exit_time,
            "amount": amount
        }

        return "Exit Successful!", bill


parking = ParkingSystem(5)


def page(message="", action="", show_table=False, bill=None):
    rows = ""

    if show_table:
        for v, d in parking.records.items():
            rows += f"""
            <tr>
                <td>{d['username']}</td>
                <td>{v}</td>
                <td>{d['slot']}</td>
                <td>{d['entry_time']}</td>
            </tr>
            """

    form_html = ""

    if action == "park":
        form_html = """
        <h3>Park Vehicle</h3>
        <form action="/park" method="post">
            <input name="name" placeholder="Username" required><br>
            <input name="vehicle" placeholder="Vehicle Number" required><br>
            <button type="submit">Submit</button>
        </form>
        """

    elif action == "exit":
        form_html = """
        <h3>Exit Vehicle</h3>
        <form action="/exit" method="post">
            <input name="vehicle" placeholder="Vehicle Number" required><br>
            <button type="submit">Submit</button>
        </form>
        """

    bill_html = ""
    if bill:
        bill_html = f"""
        <h3>💰 Bill Details</h3>
        <p>Name: {bill['name']}</p>
        <p>Vehicle: {bill['vehicle']}</p>
        <p>Slot: {bill['slot']}</p>
        <p>Entry Time: {bill['entry']}</p>
        <p>Exit Time: {bill['exit']}</p>
        <p><b>Amount: ₹{bill['amount']}</b></p>
        """

    table_html = ""
    if show_table:
        table_html = f"""
        <h3>Parking Status</h3>
        <table border="1">
            <tr>
                <th>Name</th>
                <th>Vehicle</th>
                <th>Slot</th>
                <th>Entry Time</th>
            </tr>
            {rows}
        </table>
        """

    return f"""
    <html>
    <head>
        <title>Parking System</title>
        <style>
            body {{ text-align:center; font-family: Arial; }}
            button {{ padding:10px; margin:10px; width:200px; }}
            input {{ padding:8px; margin:5px; }}
            table {{ margin:auto; margin-top:20px; }}
        </style>
    </head>
    <body>

        <h2>🚗 Parking System</h2>
        <p><b>{message}</b></p>

        <button onclick="window.location='/?action=park'">1. Park Vehicle</button>
        <button onclick="window.location='/?action=exit'">2. Exit Vehicle</button>
        <button onclick="window.location='/?show=1'">3. Parking Status</button>

        {form_html}
        {table_html}
        {bill_html}

    </body>
    </html>
    """


@app.route("/")
def home():
    action = request.args.get("action")
    show = request.args.get("show")
    return page(action=action, show_table=bool(show))


@app.route("/park", methods=["POST"])
def park_vehicle():
    name = request.form["name"]
    vehicle = request.form["vehicle"]
    msg, _ = parking.park(name, vehicle)
    return page(message=msg)


@app.route("/exit", methods=["POST"])
def exit_vehicle():
    vehicle = request.form["vehicle"]
    msg, bill = parking.exit(vehicle)
    return page(message=msg, bill=bill)


if __name__ == "__main__":
    app.run(debug=True)
