from flask import Flask, jsonify, request, render_template, session,flash,jsonify,redirect, url_for
import requests
import mysql.connector
from datetime import datetime
from flask import Response
import time 
from werkzeug.security import generate_password_hash, check_password_hash
import razorpay
from mysql.connector import Error
import requests
import urllib.parse
from decimal import Decimal, InvalidOperation
import threading
import json

BASHSMS_USER = "terion_123"
BASHSMS_PASS = "123456"
BASHSMS_SENDER = "BUZWAP"
BASHSMS_BASE_URL = "http://bhashsms.com/api/sendmsgutil.php"

app = Flask(__name__)
app.secret_key = "your_secret_key"  # needed for sessions
RAZORPAY_KEY_ID = "rzp_live_RJ1IW6GM6gU1b0"
RAZORPAY_KEY_SECRET = "hBePSUuSZRgDEtTxS7tH3NLh"
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

units = 1

BREVO_API_KEY = "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"
BREVO_SENDER_EMAIL = "sales@ionicboost.org"
BREVO_SENDER_NAME = "Ionic Boost"

DJANGO_DB_CONFIG = {
    "host": "localhost",
    "user": "root",       # <-- Django DB user
    "password": "admin",   # <-- Django DB password
    "database": "dispenser_db",   # <-- the Django database/schema name
    "port": 3306
}

def get_django_db_connection():
    try:
        conn = mysql.connector.connect(**DJANGO_DB_CONFIG)
        return conn
    except Error as e:
        app.logger.error("Failed to connect to Django DB: %s", e)
        return None
    
# ---- DB Connection ----
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="ionic_boost"
    )

def get_price_from_django_table(default=Decimal('0.00')):
    """
    Fetch price from the Django table.
    Adjust 'django_table_name' and column name 'price' to your actual names.
    For single-row product, we attempt to fetch the row with id=1.
    """
    conn = get_django_db_connection()
    print("Django DB connection:", conn)
    if not conn:
        return default

    try:
        print("Querying Django DB for price...") 
        cursor = conn.cursor(dictionary=True)
        # Adjust the table name if your Django table is different.
        # You can use fully qualified name: `django_db_name`.`app_modelname`
        cursor.execute("SELECT price FROM main_ionicboost WHERE id = %s LIMIT 1", (1,))
        row = cursor.fetchone()
        print("Fetched price from Django DB:", row)
    except Exception as e:
        app.logger.error("Error querying Django DB for price: %s", e)
        row = None
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

    if row and row.get("price") is not None:
        try:
            return Decimal(str(row["price"]))
        except (InvalidOperation, TypeError):
            return default
    return default

Ionic_Price1 = get_price_from_django_table()  # test fetch at startup
Ionic_Price = float(Ionic_Price1)
# ---- Shiprocket credentials ----
SHIPROCKET_EMAIL = "sales@ionicboost.org"
SHIPROCKET_PASSWORD = "HFrwQB4uYuADgkO#"

# ---- Shiprocket API helpers ----
def get_auth_token():
    url = "https://apiv2.shiprocket.in/v1/external/auth/login"
    payload = {"email": SHIPROCKET_EMAIL, "password": SHIPROCKET_PASSWORD}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("token")
    else:
        raise Exception("Auth failed: " + response.text)

def check_serviceability(token, pincode, weight=0.8):
    url = "https://apiv2.shiprocket.in/v1/external/courier/serviceability/"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "pickup_postcode": "110001",
        "delivery_postcode": pincode,
        "weight": weight,
        "cod": 0,
        "mode": "Surface"
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

def create_order(token, order, units: int, price: float):
    """
    Create a Shiprocket adhoc order (defensive).
    - token: Shiprocket Bearer token (string)
    - order: dict containing name, address, city, state, pincode, email, whatsapp_number
    - units: integer units to order
    - price: per-unit selling price (float)
    """
    # Validate presence of required fields
    required = ["name", "address", "city", "state", "pincode", "email", "whatsapp_number"]
    missing = [k for k in required if not order.get(k)]
    if missing:
        raise ValueError(f"Missing required order fields: {missing}")

    if not isinstance(units, int) or units <= 0:
        raise ValueError(f"Invalid units: {units}")

    try:
        price = float(price)
    except Exception:
        raise ValueError(f"Invalid price: {price}")

    # Normalize pincode & phone as strings
    pincode = str(order["pincode"]).strip()
    phone = str(order["whatsapp_number"]).strip()

    payload = {
        "order_id": f"IB{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pickup_location": "warehouse",
        "billing_customer_name": order["name"],
        "billing_last_name": "-",
        "billing_address": order["address"],
        "billing_city": order["city"],
        "billing_pincode": pincode,
        "billing_state": order["state"],
        "billing_country": "India",
        "billing_email": order["email"],
        "billing_phone": phone,
        "shipping_is_billing": True,
        "order_items": [
            {
                "name": "Ionic Boost",
                "sku": "sku.10020",
                "units": units,
                "selling_price": price,
                "tax": 18,
                "hsn": "33059040"
            }
        ],
        "payment_method": "Prepaid",
        "sub_total": round(price * units, 2),
        "length": 18,
        "breadth": 25,
        "height": 1.5,
        "weight": 0.08
    }

    url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Log request body
    body_text = json.dumps(payload, ensure_ascii=False)
    print("=== Shiprocket REQUEST ===")
    print("URL:", url)
    print("HEADERS:", headers)
    print("BODY:", body_text)

    resp = requests.post(url, headers=headers, data=body_text, timeout=30)

    # Always log full response
    print("=== Shiprocket RESPONSE ===")
    print("STATUS:", resp.status_code)
    print("TEXT:", resp.text)

    if not resp.ok:
        # raise runtime error with full response text so caller can see exact validation errors
        raise RuntimeError(f"Shiprocket API error {resp.status_code}: {resp.text}")

    return resp.json()

def generate_awb(token, shipment_id):
    url = "https://apiv2.shiprocket.in/v1/external/courier/assign/awb"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"shipment_id": shipment_id}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

def generate_pickup(token, shipment_id):
    url = "https://apiv2.shiprocket.in/v1/external/courier/generate/pickup"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"shipment_id": [shipment_id]}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

def track_shipment(token, awb_code):
    url = f"https://apiv2.shiprocket.in/v1/external/courier/track/awb/{awb_code}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


# ---- ROUTES ----
'''@app.route("/")
def index():
    return """
    <h1>Ionic Boost Order System</h1>
    <a href="/order">Create New Order</a><br>
    <a href="/orders">View All Orders</a>
    """
'''
@app.route("/order", methods=["GET", "POST"])
def order_page():
    username = session.get('user') 
    if request.method == "POST":
        data = request.form
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO order_1 (name, whatsapp_number, email, address, city, state, pincode)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data["name"],
                data["whatsapp_number"],
                data["email"],
                data["address"],
                data["city"],
                data["state"],
                data["pincode"]
            ))
            order_id = cursor.lastrowid
            conn.commit()
            return redirect(url_for('place_order', order_id=order_id))
        except Exception as e:
            conn.rollback()
            return f"Error saving order: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    return render_template("order_form.html", username=username)



@app.route("/place-order/<int:order_id>")
def place_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM order_1 WHERE id=%s", (order_id,))
        order = cursor.fetchone()
        if not order:
            return jsonify({"error": "Order not found"}), 404

        token = get_auth_token()

        # ---- CREATE ORDER in Shiprocket if not yet created ----
        if not order["shipment_id"]:
            order_resp = create_order(token, order)
            shipment_id = order_resp.get("shipment_id")
            print("Shipment ID:", shipment_id)
            order_id_sr = order_resp.get("order_id")  # Shiprocket order ID

            if not shipment_id:
                return jsonify({"error": "Order creation failed", "raw": order_resp}), 400

            # Save shipment_id & Shiprocket order ID to DB
            cursor.execute("""
                UPDATE order_1
                SET shipment_id = %s, order_id_sr = %s
                WHERE id = %s
            """, (shipment_id, order_id_sr, order_id))
            conn.commit()
        else:
            shipment_id = order["shipment_id"]
            order_id_sr = order.get("order_id_sr")

        # ---- Tracking & AWB not fetched here; will be fetched after Ready to Ship ----
        awb_code = order.get("awb_code")  # may be None
        courier_name = order.get("courier_name")
        tracking_url = f"https://shiprocket.co/tracking/{awb_code}" if awb_code else "Not available yet"

        return render_template("order_success.html",
                               order_id=order_id,
                               shipment_id=shipment_id,
                               awb_code=awb_code,
                               courier_name=courier_name,
                               tracking_url=tracking_url)
    finally:
        cursor.close()
        conn.close()

@app.route("/order-status/<int:order_id>")
def order_status(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT shipment_id, order_id_sr FROM order_1 WHERE id=%s", (order_id,))
        order = cursor.fetchone()
        if not order:
            return jsonify({"error": "Order not found"}), 404

        shipment_id = order["shipment_id"]
        order_id_sr = order["order_id_sr"]

        if not shipment_id or not order_id_sr:
            return jsonify({
                "awb_code": None,
                "courier_name": None,
                "tracking_url": None,
                "message": "Shipment or order not yet created"
            })

        token = get_auth_token()

        # Fetch manually assigned AWB using Orders API
        url = f"https://apiv2.shiprocket.in/v1/external/orders?ids[]={order_id_sr}"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        order_data = resp.json().get("data", [])

        awb_code = None
        courier_name = None
        tracking_url = None

        if order_data:
            awb_code = order_data[0].get("awb_code")
            courier_name = order_data[0].get("courier_name")
            if awb_code:
                tracking_url = f"https://shiprocket.co/tracking/{awb_code}"

        # Update DB
        cursor.execute("""
            UPDATE order_1
            SET awb_code=%s, courier_name=%s
            WHERE id=%s
        """, (awb_code, courier_name, order_id))
        conn.commit()

        return jsonify({
            "awb_code": awb_code,
            "courier_name": courier_name,
            "tracking_url": tracking_url or "Not available yet"
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        conn.close()

def fetch_awb_for_order_db(order_db_id):
    """
    Try to fetch AWB for the DB order id. Tries shipments endpoint first, then orders endpoint.
    Returns dict: {"awb_code": ..., "courier_name": ..., "tracking_url": ...} or raises.
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT shipment_id, order_id_sr FROM order_1 WHERE id = %s", (order_db_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Order not found in DB")

        shipment_id = row.get("shipment_id")
        order_id_sr = "IB20251016121102"

        print(f"🔍 Checking AWB for order_id={order_id_sr}")


        token = get_auth_token()
        awb_code = None
        courier_name = None
        tracking_url = None

        # 1) Try shipments endpoint if shipment_id present
        if shipment_id:
            try:
                # Shiprocket shipments endpoint (returns list under "data")
                shipments_url = f"https://apiv2.shiprocket.in/v1/external/shipments?shipment_id={shipment_id}"
                resp = requests.get(shipments_url, headers={"Authorization": f"Bearer {token}"})
                resp.raise_for_status()
                js = resp.json()
                # Some responses put payload under "data" -> list
                data_list = js.get("data") or js.get("response", {}).get("data")
                if isinstance(data_list, list) and len(data_list) > 0:
                    s = data_list[0]
                    # AWB can be at s["awb_code"] or s["awb"] depending on API
                    awb_code = s.get("awb_code") or s.get("awb")
                    courier_name = (s.get("courier", {}) or {}).get("courier_name") or s.get("courier_name")
                    if awb_code:
                        tracking_url = f"https://shiprocket.co/tracking/{awb_code}"
                        print(f"\n==============================")
                        print(f"✅ AWB found via shipments endpoint: {awb_code}")
                        print(f"📦 Courier: {courier_name}")
                        print(f"🚚 Shipment ID: {shipment_id}")
                        print(f"==============================\n")
            except Exception as e:
                # don't fail yet; we'll try orders endpoint
                print("⚠ Shipments endpoint attempt failed or returned no AWB:", str(e))

        # 2) If no AWB yet, try orders endpoint using order_id_sr
        if not awb_code and order_id_sr:
            try:
                # Orders endpoint supports query by ids[] -> returns data list
                orders_url = f"https://apiv2.shiprocket.in/v1/external/orders?ids[]={order_id_sr}"
                resp = requests.get(orders_url, headers={"Authorization": f"Bearer {token}"})
                resp.raise_for_status()
                js = resp.json()
                data_list = js.get("data") or js.get("response", {}).get("data")
                if isinstance(data_list, list) and len(data_list) > 0:
                    o = data_list[0]
                    awb_code = o.get("awb_code") or o.get("awb")
                    courier_name = o.get("courier_name") or (o.get("courier", {}) or {}).get("courier_name")
                    if awb_code:
                        tracking_url = f"https://shiprocket.co/tracking/{awb_code}"
                        print(f"\n==============================")
                        print(f"✅ AWB found via orders endpoint: {awb_code}")
                        print(f"📦 Courier: {courier_name}")
                        print(f"📄 Shiprocket order_id: {order_id_sr}")
                        print(f"==============================\n")
            except Exception as e:
                print("⚠ Orders endpoint attempt failed:", str(e))

        # 3) If we found the AWB, update DB
        if awb_code:
            cur.execute("""
                UPDATE order_1
                SET awb_code = %s, courier_name = %s, tracking_url = %s
                WHERE id = %s
            """, (awb_code, courier_name, tracking_url, order_db_id))
            conn.commit()

        return {"awb_code": awb_code, "courier_name": courier_name, "tracking_url": tracking_url}

    finally:
        cur.close()
        conn.close()


# --- Replace your existing /refresh_awb route with this improved one ---
@app.route("/refresh_awb/<int:order_id>")
def refresh_awb(order_id):
    """Fetch only courier name and tracking URL from Shiprocket for an existing shipment."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Step 1: Get shipment_id from DB
        cursor.execute("SELECT shipment_id FROM order_1 WHERE id=%s", (order_id,))
        row = cursor.fetchone()
        if not row or not row["shipment_id"]:
            return jsonify({"error": "Shipment ID not found in database"}), 404

        shipment_id = row["shipment_id"]
        token = get_auth_token()

        # Step 2: Fetch live tracking info from Shiprocket
        url = f"https://apiv2.shiprocket.in/v1/external/courier/track/shipment/{shipment_id}"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        # Step 3: Extract courier name and tracking link
        tracking_data = data.get("tracking_data", {})
        courier_name = tracking_data.get("courier_name")
        tracking_url = tracking_data.get("track_url")

        if not courier_name and not tracking_url:
            return jsonify({"error": "Tracking information not yet available"}), 404

        # Step 4: Update DB
        cursor.execute("""
            UPDATE order_1
            SET courier_name=%s, tracking_url=%s
            WHERE id=%s
        """, (courier_name, tracking_url, order_id))
        conn.commit()

        # Step 5: Return JSON response
        return jsonify({
            "courier_name": courier_name,
            "tracking_url": tracking_url
        })

    except Exception as e:
        print("❌ Error fetching tracking info:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/order_success/<int:order_id>")
def order_success(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM order_1 WHERE id=%s", (order_id,))
        order = cursor.fetchone()
        if not order:
            return "Order not found", 404

        # Pass order details to the HTML page
        return render_template(
            "order_success.html",
            order_id=order["id"],
            courier_name=order.get("courier_name"),
            tracking_url=order.get("tracking_url")
        )
    finally:
        cursor.close()
        conn.close()

# ----------------- DOWNLOAD INVOICE -----------------
import time  # Add this at the top of your file if not already imported

@app.route("/download-invoice/<int:order_id>")
def download_invoice(order_id):
    """Generate invoice and check if AWB exists (without assigning)."""
    try:
        token = get_auth_token()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT order_id_sr, shipment_id FROM order_1 WHERE id = %s", (order_id,))
        row = cursor.fetchone()

        if not row or not row["order_id_sr"]:
            return "No Shiprocket order ID found for this order"

        order_id_sr = row["order_id_sr"]
        shipment_id = row["shipment_id"]

        # ---- Step 1: Generate Invoice ----
        invoice_url_endpoint = "https://apiv2.shiprocket.in/v1/external/orders/print/invoice"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {"ids": [order_id_sr]}
        resp = requests.post(invoice_url_endpoint, headers=headers, json=payload)
        resp.raise_for_status()
        invoice_url = resp.json().get("invoice_url")

        if not invoice_url:
            return "Invoice not available yet. Please try again later."

        # ---- Step 2: Check if AWB already exists ----
        shipment_details_url = f"https://apiv2.shiprocket.in/v1/external/shipments?shipment_id={shipment_id}"
        awb_resp = requests.get(shipment_details_url, headers={"Authorization": f"Bearer {token}"})
        awb_resp.raise_for_status()
        shipment_data = awb_resp.json().get("data", [])

        awb_code = None
        courier_name = None

        if shipment_data and isinstance(shipment_data, list):
            awb_code = shipment_data[0].get("awb_code")
            courier_name = shipment_data[0].get("courier", {}).get("courier_name")

        tracking_url = f"https://shiprocket.co/tracking/{awb_code}" if awb_code else None

        # ---- Step 3: Update DB (if AWB exists) ----
        cursor.execute("""
            UPDATE order_1
            SET awb_code = %s, courier_name = %s
            WHERE id = %s
        """, (awb_code, courier_name, order_id))
        conn.commit()

        cursor.close()
        conn.close()

        # ---- Step 4: Return invoice PDF ----
        pdf_resp = requests.get(invoice_url)
        pdf_resp.raise_for_status()
        return Response(
            pdf_resp.content,
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=invoice_{order_id_sr}.pdf"}
        )

    except Exception as e:
        return f"Error generating invoice or checking AWB: {str(e)}"

@app.route('/previous_order')
def previous_orders():
    # require login
    if "user_id" not in session:
        flash("Please login first to view your orders.", "warning")
        return redirect(url_for("login"))

    # prefer whatsapp in session, fallback to user email if available
    user_whatsapp = session.get("whatsapp")
    user_email = None
    # try to fetch email from users table if available
    if "user_id" in session:
        try:
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT email FROM users WHERE id = %s", (session["user_id"],))
            u = cur.fetchone()
            if u:
                user_email = u.get("email")
        except Exception as e:
            print("Error fetching user email:", e)
        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

    # Build query: match by whatsapp_number OR email (covers most cases)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if user_whatsapp and user_email:
            cursor.execute("""
                SELECT id, name, whatsapp_number, email, address, city, state, pincode,
                       shipment_id, order_id_sr, awb_code, courier_name, tracking_url, created_at
                FROM order_1
                WHERE whatsapp_number = %s OR email = %s
                ORDER BY created_at DESC, id DESC
            """, (user_whatsapp, user_email))
        elif user_whatsapp:
            cursor.execute("""
                SELECT id, name, whatsapp_number, email, address, city, state, pincode,
                       shipment_id, order_id_sr, awb_code, courier_name, tracking_url, created_at
                FROM order_1
                WHERE whatsapp_number = %s
                ORDER BY created_at DESC, id DESC
            """, (user_whatsapp,))
        elif user_email:
            cursor.execute("""
                SELECT id, name, whatsapp_number, email, address, city, state, pincode,
                       shipment_id, order_id_sr, awb_code, courier_name, tracking_url, created_at
                FROM order_1
                WHERE email = %s
                ORDER BY created_at DESC, id DESC
            """, (user_email,))
        else:
            # if nothing available, return empty list (shouldn't normally happen)
            orders = []
            return render_template("track_orders.html", orders=orders)

        orders = cursor.fetchall()

        # normalize created_at to a string (if it's a datetime object)
        for o in orders:
            ca = o.get("created_at")
            if hasattr(ca, "strftime"):
                o["created_at_str"] = ca.strftime("%Y-%m-%d %H:%M:%S")
            else:
                o["created_at_str"] = ca or "-"

        return render_template("previous_orders.html", orders=orders)

    except Exception as e:
        print("Error fetching orders:", e)
        flash("Unable to fetch your orders right now. Try again later.", "danger")
        return redirect(url_for("home"))
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


""" @app.route("/track/<awb_code>")
def track_awb(awb_code):
    try:
        token = get_auth_token()  # Get Shiprocket auth token
        url = f"https://apiv2.shiprocket.in/v1/external/courier/track/awb/{awb_code}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        tracking_data = resp.json()

        return render_template("track_awb.html", awb_code=awb_code, tracking_data=tracking_data)

    except Exception as e:
        return f"Error fetching tracking info: {str(e)}"
 """

def send_whatsapp_confirm(phone_number, params_list):
    params_str = ",".join(params_list)
    
    payload = {
        "user": BASHSMS_USER,
        "pass": BASHSMS_PASS,
        "sender": BASHSMS_SENDER,
        "phone": phone_number,
        "text": "shipping_msgs",  # template name
        "priority": "wa",
        "stype": "normal",
        "Params": params_str
    }

    encoded_params = urllib.parse.urlencode(payload)
    full_url = f"{BASHSMS_BASE_URL}?{encoded_params}"
    print("Sending WhatsApp:", full_url)

    resp = requests.get(full_url)
    if resp.status_code == 200:
        print("WhatsApp sent successfully:", resp.text)
    else:
        print("WhatsApp sending failed:", resp.status_code, resp.text)



sent_shipments = set()
POLL_INTERVAL = 60  # seconds, adjust as needed

def poll_shiprocket_and_notify():
    global sent_shipments
    if not isinstance(sent_shipments, set):
        sent_shipments = set()

    print("✅ Shiprocket Polling Thread Started...")

    while True:
        try:
            # Get orders from Shiprocket API
            url = "https://apiv2.shiprocket.in/v1/external/orders"
            token = get_shiprocket_token()  # your function to get auth token
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            orders = response.json().get("data", [])

            print(f"🔄 Received {len(orders)} orders")

            for order in orders:
                order_id = order.get("channel_order_id") or order.get("id")
                shipments = order.get("shipments", [])

                print(f"\n📦 Processing order: {order_id}, Shipments: {len(shipments)}")

                for shipment in shipments:
                    shipment_id = shipment.get("id")
                    courier = shipment.get("courier", "").strip()

                    # Skip if courier is not assigned
                    if not courier:
                        print(f"  - Shipment {shipment_id} courier not assigned, skipping...")
                        continue

                    # Skip if already notified
                    if shipment_id in sent_shipments:
                        print(f"  - Shipment {shipment_id} already notified, skipping...")
                        continue

                    # Fetch tracking URL from Shiprocket
                    try:
                        track_resp = requests.get(
                            f"https://apiv2.shiprocket.in/v1/external/courier/track/shipment/{shipment_id}",
                            headers={"Authorization": f"Bearer {token}"}
                        )
                        track_resp.raise_for_status()
                        tracking_data = track_resp.json().get("tracking_data", {})
                        tracking_url = tracking_data.get("track_url", "")
                    except Exception as track_err:
                        print(f"⚠ Could not fetch tracking URL for shipment {shipment_id}: {track_err}")
                        tracking_url = ""

                    # Prepare customer info
                    customer_name = order.get("customer_name") or "Customer"
                    customer_phone = order.get("customer_phone")
                    if not customer_phone:
                        print(f"  - No customer phone for order {order_id}, skipping WhatsApp")
                        continue
                    if len(customer_phone) <= 10:
                        customer_phone = "91" + customer_phone

                    # Include tracking URL in params
                    params_list = [customer_name, order_id, tracking_url]
                    print(f"  - Will send WhatsApp to {customer_phone} with params {params_list}")

                    # Send WhatsApp
                    try:
                        result = send_whatsapp_confirm(customer_phone, params_list)
                        if result is None:
                            print(f"  - WhatsApp sent successfully (no return) for order {order_id}")
                        else:
                            resp_text, resp_status = result
                            print(f"  - BashSMS response (status {resp_status}): {resp_text}")

                        # Mark shipment as notified
                        sent_shipments.add(shipment_id)
                        print(f"✅ WhatsApp sent for shipment {shipment_id}")

                    except Exception as wa_err:
                        print(f"⚠ WhatsApp send failed for order {order_id}: {wa_err}")

            # Wait before next poll
            time.sleep(POLL_INTERVAL)

        except requests.HTTPError as e:
            status = getattr(e, "response", None).status_code if getattr(e, "response", None) else None
            print(f"🚨 Shiprocket API Error: {e} (status {status})")
            if status == 401:
                print("🔐 Token expired — fetching new token...")
                token = get_shiprocket_token()
            time.sleep(POLL_INTERVAL)

        except Exception as e:
            print(f"❌ Unexpected error in poll loop: {e}")
            time.sleep(POLL_INTERVAL)

@app.route("/orders")
def view_orders():
    print("hello")
    get_price_from_django_table()
    username = session.get('user')
    whatsapp = session.get("whatsapp")  # ✅ correct session key
    if not whatsapp:
        return "Please log in first", 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # ✅ Fetch only orders matching the WhatsApp number
        cursor.execute(
            "SELECT * FROM order_1 WHERE whatsapp_number = %s ORDER BY id DESC",
            (whatsapp,)
        )
        orders = cursor.fetchall()
        return render_template("orders.html", orders=orders, username=username)
    except Exception as e:
        return f"Error fetching orders: {str(e)}"
    finally:
        cursor.close()
        conn.close()



def check_invoice_status(token, order_id):
    """
    Checks if the invoice URL exists for a given Shiprocket order_id.
    """
    url = f"https://apiv2.shiprocket.in/v1/external/orders/show/{order_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json().get("data", {})
    print("Invoice URL:", data.get("invoice_url"))
    return data.get("invoice_url")

@app.context_processor
def inject_user():
    return dict(user=session.get("user"))

@app.route('/failed')
def failed():
    reason = request.args.get("reason", "Unknown error")
    return render_template("failed.html", reason=reason)



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    username = session.get('user') 
    Ionic_Price1 = get_price_from_django_table()
    Ionic_Price = float(Ionic_Price1)
    print("hello")
    if request.method == 'POST':
        use_existing = request.form.get("use_existing")
        payment_method = request.form.get("payment")
        name = session.get("user") or "Test User"

        if use_existing == "yes":
            # fetch saved details from DB
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT name, email, whatsapp_number, address, city, state, pincode 
                FROM users 
                WHERE id=%s
            """, (session["user_id"],))
            saved_user = cursor.fetchone()
            cursor.close()
            conn.close()

            name = saved_user["name"]
            email = saved_user["email"]
            whatsapp_number = saved_user["whatsapp_number"]
            address = saved_user["address"]
            city = saved_user["city"]
            state = saved_user["state"]
            pincode = saved_user["pincode"]
        else:
            name = request.form.get("name")
            email = request.form.get("email")
            whatsapp_number = request.form.get("whatsapp_number")
            address = request.form.get("address")
            city = request.form.get("city")
            state = request.form.get("state")
            pincode = request.form.get("pincode")

        # Razorpay order creation
        amount = Ionic_Price  # ₹100
        print("Amount in checkout:", amount)
        order_data = {"amount": amount, "currency": "INR", "payment_capture": 1}
        razorpay_order = razorpay_client.order.create(data=order_data)

        # Save transaction
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO transactions 
            (order_id, amount, currency, status, user_name, user_email, whatsapp_number, user_address, city, state, pincode, payment_method)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        val = (razorpay_order['id'], amount, "INR", "created",
               name, email, whatsapp_number, address, city, state, pincode, payment_method)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()

        return render_template("checkout.html",
                               key_id=RAZORPAY_KEY_ID,
                               order_id=razorpay_order['id'],
                               amount=float(amount),
                               user=name,
                               user_data={
                                   "email": email,
                                   "whatsapp_number": whatsapp_number,
                                   "address": address,
                                   "city": city,
                                   "state": state,
                                   "pincode": pincode
                               })

    # ✅ GET request → prefill saved user details
    user_data = None
    if "user_id" in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT name, email, whatsapp_number, address, city, state, pincode 
            FROM users 
            WHERE id=%s
        """, (session["user_id"],))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
    print("Rendering checkout page", Ionic_Price)
    return render_template("checkout.html",
                           user=session.get("user"),
                           user_data=user_data,
                           amount=float(Ionic_Price),
                           key_id=RAZORPAY_KEY_ID,
                           order_id="",
                           )

# -----------------------
# Home Page
# -----------------------
@app.route("/")
def home():
    Ionic_Price1 = get_price_from_django_table()
    Ionic_Price = float(Ionic_Price1)
    username = session.get('username', None)
    if "user" in session:
        username = session.get('user')  # name stored in session
        print("Logged in user:", username)
    return render_template("index.html", username=username,price=Ionic_Price)


@app.route("/purchase")
def purchase():
    Ionic_Price1 = get_price_from_django_table()
    Ionic_Price = float(Ionic_Price1)
    if "user_id" not in session:
        flash("Please login first to continue.", "warning")
        return redirect(url_for("login"))
    username = session.get('user') 
    return render_template("purchase.html", user=session.get("user"),price=Ionic_Price, username=username)

@app.route('/success')  # custom route for success page
def payment_success():
    return redirect(url_for("purchase"))

def send_whatsapp(phone_number, params_list):
    params_str = ",".join(params_list)
    
    # Prepare URL
    payload = {
        "user": BASHSMS_USER,
        "pass": BASHSMS_PASS,
        "sender": BASHSMS_SENDER,
        "phone": phone_number,
        "text": "shipping",  # template name
        "priority": "wa",
        "stype": "normal",
        "Params": params_str
    }

    # Encode URL properly
    encoded_params = urllib.parse.urlencode(payload)
    full_url = f"{BASHSMS_BASE_URL}?{encoded_params}"
    print(full_url)

    # Send request
    resp = requests.get(full_url)
    if resp.status_code == 200:
        print("WhatsApp sent successfully:", resp.text)
    else:
        print("WhatsApp sending failed:", resp.status_code, resp.text)

def send_email(to, subject, html_content):
    try:
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }
        data = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": to}],
            "subject": subject,
            "htmlContent": html_content
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code in [200, 201]:
            print(f"✅ Email sent successfully to {to}")
        else:
            print(f"❌ Email failed ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"❌ Exception while sending email: {str(e)}")

@app.route('/verify', methods=['POST'])
def verify_signature():
    # -------------------------
    # Step 1: Fetch form data
    # -------------------------
    payment_id = request.form.get("razorpay_payment_id")
    order_id = request.form.get("razorpay_order_id")
    signature = request.form.get("razorpay_signature")

    name = request.form.get("name")
    email = request.form.get("email")
    whatsapp_number = request.form.get("whatsapp_number")
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    pincode = request.form.get("pincode")

    # -------------------------
    # Step 2: Verify Razorpay payment signature
    # -------------------------
    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })
    except Exception as e:
        print("Razorpay verification failed:", e)
        #return redirect(url_for("failed", reason=f"Payment verification failed: {str(e)}"))

    # -------------------------
    # Step 3: Insert order into DB
    # -------------------------
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        print(name)
        cursor.execute("""
            INSERT INTO order_1
            (name, whatsapp_number, email, address, city, state, pincode, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """, (name, whatsapp_number, email, address, city, state, pincode))
        new_order_id = cursor.lastrowid
        conn.commit()

        # Fetch inserted order
        cursor.execute("SELECT * FROM order_1 WHERE id=%s", (new_order_id,))
        order = cursor.fetchone()

    except Exception as e:
        print("DB insertion failed:", e)
        return redirect(url_for("failed", reason=f"DB insertion failed: {str(e)}"))

    # -------------------------
    # Step 4: Shiprocket order creation and AWB generation
    # -------------------------
    try:
        token = get_auth_token()
        print("Shiprocket token (first 10 chars):", token[:10] if token else "None")
        # Optional: Check serviceability
        try:
            check_serviceability(token, order["pincode"])
            print("hii")
        except Exception as e:
            print(f"Serviceability check failed: {e}")

        try:
            Ionic_Price = float(get_price_from_django_table())
        except Exception as e:
            print("Failed to get Ionic_Price:", e)
            Ionic_Price = None

        units = 1  # change if you support multi-unit or cart logic

        # Log order dict that will be sent
        print("Order data to send to Shiprocket:", order)
        print("Units:", units, "Price:", Ionic_Price)

        # Shiprocket order creation
        order_resp = create_order(token, order, units, Ionic_Price)
        print("helo")
        shipment_id = order_resp.get("shipment_id") or order_resp.get("response", {}).get("data", {}).get("shipment_id")
        order_id_sr = order_resp.get("order_id") or order_resp.get("response", {}).get("data", {}).get("order_id")
        order_id_app = order_resp.get("channel_order_id") or order_resp.get("response", {}).get("data", {}).get("channel_order_id")

        if not shipment_id or not order_id_sr:
            print("shipp")
            return jsonify({"error": "Shiprocket order creation failed", "raw": order_resp}), 400

        # Generate AWB
        #awb_resp = generate_awb(token, shipment_id)
        """ print("s")
        awb_data = awb_resp.get('response', {}).get('data', {})
        awb_code = awb_data.get('awb_code')
        courier_name = awb_data.get('courier_name')

        # Generate Pickup
        pickup_resp = generate_pickup(token, shipment_id)
        print("hello")
        # Tracking info
        tracking_url = f"https://shiprocket.co/tracking/{awb_code}" if awb_code else "Not available"
        tracking_info = track_shipment(token, awb_code) if awb_code else {}
        print("vanakam")
        # Update order_1 with Shiprocket info"""
        cursor.execute("""
            UPDATE order_1 
            SET shipment_id=%s, order_id_sr=%s
            WHERE id=%s
        """, (shipment_id, order_id_sr, new_order_id))
        conn.commit()
        print("vbjkl")

      #  order_resp = create_order(token, order)
       # shipment_id = order_resp.get("shipment_id")
        #order_id_sr = order_resp.get("order_id")

        # Save shipment info in DB
        cursor.execute("""
            UPDATE order_1 
            SET shipment_id=%s, order_id_sr=%s
            WHERE id=%s
        """, (shipment_id, order_id_sr, new_order_id))
        conn.commit()

        html_content = f"""
            <p>Hello {order['name']},</p>
            <p>Your order no <b>#{order_id_app}</b> as per our record has been received and is now being processed.</p>
            <p>Your order total is Rs. {Ionic_Price}/-</p>
            <p>Thank you for your order.</p>
            <p><b>Terion Innovix Private Limited</b></p>
        """
        
        params_list = [str(order_id_app), str(Ionic_Price), name]
        phone_number = f"91{whatsapp_number}"

        send_whatsapp(phone_number, params_list)
        send_email(order['email'], "Order Confirmation - Terion Innovix", html_content)

        # -------------------------
        # Step 5: Render success page
        # -------------------------
        return render_template("order_success.html",
                               order_id=new_order_id,
                               shipment_id=shipment_id)

    except Exception as e:
        print("Shiprocket error:", e)
        return render_template("order_success.html", error=f"Error processing order: {str(e)}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()


'''
@app.route('/order', methods=['POST'])  # custom route to create an order
def create_order():
    amount = 500  # amount in paise (₹5.00)
    currency = "INR"

    order_data = {
        "amount": amount,
        "currency": currency
    }

    razorpay_order = razorpay_client.order.create(data=order_data)
    return {"order_id": razorpay_order['id'], "amount": amount}
'''
# -----------------------
# Register
# -----------------------
# -----------------------
# Register  
# -----------------------

@app.route("/order_summary/<razorpay_order_id>")
def order_summary(razorpay_order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM shiprocket_orders 
        WHERE razorpay_order_id=%s
    """, (razorpay_order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()

    if not order:
        flash("Order not found!", "danger")
        return redirect(url_for("home"))

    return render_template("order_summary.html", order=order)

@app.route('/register', methods=['GET', 'POST'])
def register():		
    try:
        if request.method == 'POST':	
            name = request.form['name']
            whatsapp = request.form['whatsapp']
            email = request.form['email']   # ✅ NEW FIELD
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            pincode = request.form['pincode']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # ✅ Password match check
            if password != confirm_password:
                flash("Passwords do not match!", "danger")
                return redirect(url_for('register'))

            # ✅ Hash password
            password_hash = generate_password_hash(password)

            conn = get_db_connection()
            cursor = conn.cursor()

            # ✅ Check duplicate (whatsapp OR email)
            cursor.execute("SELECT * FROM users WHERE whatsapp_number=%s OR email=%s", (whatsapp, email))
            existing = cursor.fetchone()
            if existing:
                flash("WhatsApp number or Email already registered!", "danger")
                cursor.close()
                conn.close()
                return redirect(url_for('register'))

            # ✅ Insert new user
            cursor.execute("""
                INSERT INTO users (name, whatsapp_number, email, address, city, state, pincode, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, whatsapp, email, address, city, state, pincode, password_hash))

            conn.commit()
            cursor.close()
            conn.close()

            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
    except Exception as e:
        app.logger.error("Registration error", exc_info=True)
        return "Internal Server Error", 500

def get_shiprocket_token():
    url = "https://apiv2.shiprocket.in/v1/external/auth/login"
    resp = requests.post(url, json={"email": SHIPROCKET_EMAIL, "password": SHIPROCKET_PASSWORD})
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Shiprocket Auth Failed:", resp.status_code, resp.text)  # <-- exact reason
        raise
    return resp.json().get("token")


def create_shiprocket_order(token, user, order_id, amount):
    url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "order_id": order_id,
        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pickup_location": "warehouse",
        "billing_customer_name": user["name"],
        "billing_last_name": "-",
        "billing_address": user["address"],
        "billing_city": user["city"],
        "billing_pincode": user["pincode"],
        "billing_state": user["state"],
        "billing_country": "India",
        "billing_email": user["email"],
        "billing_phone": user["whatsapp_number"],
        "shipping_is_billing": True,
        "order_items": [
            {"name": "IONIC BOOST", "sku": "ionic001", "units": 1, "selling_price": str(amount/100)}
        ],
        "payment_method": "Prepaid",
        "sub_total": amount/100,
        "length": 10, "breadth": 10, "height": 10, "weight": 1.0
    }

    resp = requests.post(url, json=payload, headers=headers)
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Shiprocket Order Creation Failed:", resp.status_code, resp.text)  # <-- exact reason
        raise
    return resp.json()


def generate_awb(token, shipment_id):
    url = "https://apiv2.shiprocket.in/v1/external/courier/assign/awb"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"shipment_id": [shipment_id]}
    resp = requests.post(url, json=payload, headers=headers)
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Shiprocket AWB Generation Failed:", resp.status_code, resp.text)  # <-- exact reason
        raise
    return resp.json()

import os
RECAPTCHA_SECRET = "6LcqHQUsAAAAAEZMYPIDorFD5SgYTr-3HPYoob0U"
def verify_recaptcha(token, remote_ip=None):
    """Verify Google reCAPTCHA v2 checkbox token server-side."""
    if not token:
        return False
    try:
        resp = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": RECAPTCHA_SECRET,
                "response": token,
                "remoteip": remote_ip or "",
            },
            timeout=5,
        )
        data = resp.json()
        return bool(data.get("success"))
    except Exception:
        return False
    
# -----------------------
# Login
# -----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        token = request.form.get("g-recaptcha-response")
        """ if not verify_recaptcha(token, request.remote_addr):
            flash("Please complete the reCAPTCHA.", "danger")
            return redirect(url_for("login")) """
        whatsapp_number = request.form["whatsapp"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE whatsapp_number=%s OR email=%s", (whatsapp_number, whatsapp_number))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # ✅ Verify password
        if user and check_password_hash(user["password_hash"], password):
            session["user"] = user["name"]        # show name in header
            print("User logged in:", user["name"])
            session["whatsapp"] = user["whatsapp_number"]
            session["user_id"] = user["id"]

            flash("Login successful!", "success")
            return redirect(url_for("purchase"))
        else:
            flash("Invalid credentials. Please try again.", "danger")
            return redirect(url_for("login"))

    # ✅ If already logged in → go home
    if "user_id" in session:
        return redirect(url_for("purchase"))

    return render_template("login.html")


# -----------------------
# Logout
# -----------------------
@app.route("/logout")
def logout():
    session.clear()  # ✅ clears all user data
    flash("Logged out successfully!", "info")
    return redirect(url_for("home"))  # ✅ redirect to login page


# -----------------------
# Edit Profile (GET + POST)
# -----------------------
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    username = session.get('user')
    if "user_id" not in session:  # ✅ must be logged in
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        # collect values from form
        email = request.form["email"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        pincode = request.form["pincode"]

        cursor.execute("""
            UPDATE users 
            SET email=%s, address=%s, city=%s, state=%s, pincode=%s 
            WHERE id=%s
        """, (email, address, city, state, pincode, user_id))
        conn.commit()

        flash("Profile updated successfully!", "success")
        cursor.close()
        conn.close()
        return redirect(url_for("home"))

    # ✅ fetch user details for form prefill
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("edit_profile.html", user=user, username=username)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")

@app.route("/privacy_policy")
def privacy_policy():
    return render_template("privacy_policy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html",price=Ionic_Price)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/return_policy")
def return_policy():
    return render_template("return.html")
# -----------------------
# Previous Purchases
# -----------------------
@app.route("/previous_purchases")
def previous_purchases():
    get_price_from_django_table()
    print("hello")
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT item_name, purchase_date FROM purchases WHERE user_id=%s", (user_id,))
    purchases = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("previous_purchases.html", purchases=purchases)

if __name__ == "__main__":
    polling_thread = threading.Thread(target=poll_shiprocket_and_notify, daemon=True)
    polling_thread.start()

    # Important: disable reloader
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
