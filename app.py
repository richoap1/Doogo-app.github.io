from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, jsonify
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
import re
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_session import Session
from dotenv import load_dotenv
# from flask_talisman import Talisman

# Load environment variables from .env file
load_dotenv()

# Flask app configuration
app = Flask(__name__, static_url_path='/static', template_folder='views')
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_key') # Set a secret key for session management
# Talisman(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'Your_email@gmail.com')  # Use environment variable for email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'Your_password')  # Use environment variable for password
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']  # Default sender

mail = Mail(app)

# Google OAuth
google_bp = make_google_blueprint(
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    redirect_to='google_login'
)
app.register_blueprint(google_bp, url_prefix='/google_login')

# Facebook OAuth
facebook_bp = make_facebook_blueprint(
    client_id=os.environ.get('FACEBOOK_CLIENT_ID'),
    client_secret=os.environ.get('FACEBOOK_CLIENT_SECRET'),
    redirect_to='facebook_login'
)
app.register_blueprint(facebook_bp, url_prefix='/facebook_login')
# Define allowed IPs for admin access
ALLOWED_ADMIN_IPS = ['127.0.0.1']  # Add your admin IPs here

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('your_database.db', timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def is_valid_email(email):
    """Check if the email format is valid."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def send_registration_email(user_email, user_name):
    """Send a welcome email to the user after registration."""
    msg = Message("Welcome to Our Service!", recipients=[user_email])
    msg.body = f"Hi {user_name},\n\nThank you for registering with us! We're excited to have you on board.\n\nBest regards,\nDOOGO_ID"
    mail.send(msg)

# Function to send promotional email
def send_promotional_email(user_email):
    msg = Message("Exclusive Promotion Just for You!", recipients=[user_email])
    msg.body = "Hello!\n\nWe have an exciting promotion just for you! Enjoy 20% off your first purchase.\n\nUse code: PROMO20 at checkout.\n\nBest regards,\nDOOGO_ID"
    mail.send(msg)

# Function to create the users table
def create_users_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            name TEXT NOT NULL, 
            address TEXT NOT NULL, 
            gender TEXT NOT NULL,  
            role TEXT DEFAULT 'user'  
        )
    ''')
    conn.commit()
    conn.close()

# Function to create the products table
def create_products_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            discount REAL DEFAULT 0,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Function to create the messages table
def create_messages_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,  -- Change from user_id to email
            content TEXT NOT NULL,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Decorator to restrict admin access based on IP
def restrict_admin_access(f):
    def wrapper(*args, **kwargs):
        if request.endpoint in ['admin_chat', 'admin_login', 'admin_page']:
            if 'user_id' not in session or session.get('role') != 'admin':
                flash("You are not authorized to access this page.")
                return redirect(url_for('login'))  # Redirect to login if not authorized
            
            if request.remote_addr not in ALLOWED_ADMIN_IPS:
                abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return wrapper

@app.before_request
@restrict_admin_access
def before_request():
    pass  # This will run before every request

# Helper functions for formatting
def format_price(price):
    """Format the price to include 'Rp' and use thousands separators."""
    return f"Rp{int(price):,}".replace(',', '.')

def format_price(price):
    """Format the price to include 'Rp' and use thousands separators."""
    return f"Rp{int(price):,}".replace(',', '.')

def format_discount(discount):
    """Format the discount to remove decimal places if it's a whole number."""
    return int(discount) if discount.is_integer() else discount

# Register helper functions in Jinja2
app.jinja_env.globals.update(format_price=format_price)
app.jinja_env.globals.update(format_discount=format_discount)

@app.route('/')
def index():
    return render_template('index.ejs')

@app.route('/about')
def about():
    return render_template('about.ejs')

@app.route('/layanan')
def layanan():
    return render_template('layanan.ejs')

@app.route('/products', methods=['GET', 'POST'])
def products():
    conn = get_db_connection()
    
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity', 1))  # Default to 1 if not specified
        
        # Initialize cart in session if it doesn't exist
        if 'cart' not in session:
            session['cart'] = {}
        
        # Add product to cart
        if product_id in session['cart']:
            session['cart'][product_id] += quantity  # Increment quantity if already in cart
        else:
            session['cart'][product_id] = quantity  # Add new product to cart
        
        session.modified = True  # Mark session as modified
        flash("Product added to cart!")  # Flash message for user feedback
        return redirect(url_for('products'))  # Redirect to the products page

    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    
    return render_template('products.php', products=products)  # Ensure this points to your products template

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['username']  # Email
        password = generate_password_hash(request.form['password'])  # Password
        name = request.form['name']  # Name
        address = request.form['address']  # Address
        gender = request.form['gender']  # Gender

        # Validate email format
        if not is_valid_email(email):
            flash("Invalid email format. Please enter a valid email address.")
            return render_template('register.php', error="Invalid email format.")

        try:
            # Check if the email already exists
            with get_db_connection() as conn:
                existing_user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

                if existing_user:
                    flash("Email already exists. Please choose a different one.")
                    return render_template('register.php', error="Email already exists.")

                # Insert into database
                conn.execute("INSERT INTO users (email, password, name, address, gender) VALUES (?, ?, ?, ?, ?)", 
                            (email, password, name, address, gender))
                conn.commit()   

            # Send registration email
            send_registration_email(email, name)

            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))

        except sqlite3.OperationalError as e:
            flash(f"An error occurred during registration: {str(e)}")
            return render_template('register.php', error=f"An error occurred: {str(e)}")

    return render_template('register.php')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']  # Change from username to email
        password = request.form['password']

        # Check if the user exists
        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if user and (user['password'] is None or check_password_hash(user['password'], password)):
            # Store user information in session
            session['user_id'] = user['id']
            session['name'] = user['name']  # Store the user's name
            session['role'] = user['role']  # Store the user's role
            flash("Login successful!")
            return redirect(url_for('index'))  # Redirect to the index page after successful login
        else:
            flash("Invalid email or password.")
            return redirect(url_for('login'))

    return render_template('login.php')

# Google login route
@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text
    email = resp.json()["emails"][0]["value"]
    name = resp.json()["displayName"]

    # Check if the user exists in the database
    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not user:
            # If the user does not exist, create a new user
            conn.execute("INSERT INTO users (email, name) VALUES (?, ?)", (email, name))
            conn.commit()

    # Store user information in session
    session['user_id'] = user['id']
    session['name'] = name
    session['role'] = 'user'  # Default role for social login
    flash("Login successful!")
    return redirect(url_for('/'))

# Facebook login route
@app.route('/facebook_login')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    resp = facebook.get('/me?fields=id,name,email')
    assert resp.ok, resp.text
    email = resp.json()["email"]
    name = resp.json()["name"]

    # Check if the user exists in the database
    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if not user:
            # If the user does not exist, create a new user
            conn.execute("INSERT INTO users (email, name) VALUES (?, ?)", (email, name))
            conn.commit()

    # Store user information in session
    session['user_id'] = user['id']
    session['name'] = name
    session['role'] = 'user'  # Default role for social login
    flash("Login successful!")
    return redirect(url_for('index'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['username']  # Change from username to email
        password = request.form['password']

        # Check if the admin exists
        with get_db_connection() as conn:
            admin = conn.execute("SELECT * FROM users WHERE email = ? AND role = 'admin'", (email,)).fetchone()  # Change from username to email

        if admin and check_password_hash(admin['password'], password):
            # Store admin information in session
            session['user_id'] = admin['id']
            session['role'] = admin['role']  # Store the admin's role
            flash("Admin login successful!")
            return redirect(url_for('admin_page'))  # Redirect to the admin page after successful login
        else:
            flash("Invalid admin email or password.")
            return redirect(url_for('admin_login'))

    return render_template('admin_login.php')  # Render the admin login page

@app.route('/bantuan', methods=['GET', 'POST'])
def bantuan():
    if request.method == 'POST':
        user_message = request.form['user_message']
        # Store user message in the database
        with get_db_connection() as conn:
            conn.execute("INSERT INTO messages (content, email) VALUES (?, ?)", (user_message, session.get('email')))  # Use email instead of user_id
            conn.commit()
        flash("Message sent successfully!")
        return redirect(url_for('bantuan'))

    # Fetch messages and responses for the logged-in user
    if 'user_id' in session:
        with get_db_connection() as conn:
            messages = conn.execute("SELECT * FROM messages WHERE email = ?", (session.get('email'),)).fetchall()  # Use email instead of user_id
    else:
        messages = []  # No messages if the user is not logged in

    return render_template('bantuan.ejs', messages=messages)

@app.route('/admin_page')
def admin_page():
    # Check if the user is logged in and has the role of admin
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("You are not authorized to access this page.")
        return redirect(url_for('login'))  # Redirect to login if not authorized

    return render_template('admin_page.php')  # Render the admin page

@app.route('/admin_chat', methods=['GET', 'POST'])
def admin_chat():
    # Check if the user is logged in and has the role of admin
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("You are not authorized to access this page.")
        return redirect(url_for('login'))  # Redirect to login if not authorized

    with get_db_connection() as conn:
        # Fetch all users to display in the dropdown
        users = conn.execute("SELECT id, email FROM users WHERE role = 'user'").fetchall()  # Change from username to email
        
        messages = conn.execute("SELECT * FROM messages").fetchall()  # Fetch all messages

    return render_template('admin_chat.php', messages=messages, users=users)

@app.route('/reply_chat/<int:message_id>', methods=['POST'])
def reply_chat(message_id):
    response = request.form['response']

    # Update the message with the admin's response
    with get_db_connection() as conn:
        conn.execute("UPDATE messages SET response = ? WHERE id = ?", (response, message_id))
        conn.commit()

    flash("Response sent successfully!")
    return redirect(url_for('admin_chat'))  # Redirect back to the admin chat page

@app.route('/seller')
def seller():
    # Check if the user is logged in and has the role of seller or admin
    if 'user_id' not in session or session.get('role') not in ['seller', 'admin']:
        flash("You are not authorized to access this page.")
        return redirect(url_for('login'))  # Redirect to login if not authorized

    return render_template('seller.php')

@app.route('/add_product', methods=['POST'])
def add_product():
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    discount = request.form['discount']
    
    # Validate image upload
    if 'image' not in request.files:
        flash("No image uploaded.")
        return redirect(url_for('seller'))

    image = request.files['image']
    if image.filename == '':
        flash("No selected file.")
        return redirect(url_for('seller'))

    # Save the uploaded image
    image_path = os.path.join('static/public/images', image.filename)
    image.save(image_path)

    # Insert product into the database
    with get_db_connection() as conn:
        conn.execute("INSERT INTO products (title, description, price, discount, image_path) VALUES (?, ?, ?, ?, ?)",
                    (title, description, price, discount, image_path))
        conn.commit()

    flash("Product added successfully!")
    return redirect(url_for('products'))  # Redirect to the products page after adding

@app.route('/logout')
def logout():
    # Check if the user is logged in
    if 'user_id' in session:
        # Store the role of the user who is logging out
        user_role = session.get('role')
        
        # Clear only the session data for the user who is logging out
        session.clear()  # This will clear all session data
        
        flash("You have been logged out.")
        
        # If the user was an admin, redirect to the admin login page or home page
        if user_role == 'admin':
            return redirect(url_for('admin_login'))  # Redirect admin to login page
        else:
            return redirect(url_for('index'))  # Redirect regular user to home page
    else:
        flash("You are not logged in.")
        return redirect(url_for('index'))  # Redirect to home page if not logged in

@app.route('/fetch_messages')
def fetch_messages():
    if 'user_id' not in session:
        return {'messages': []}  # Return an empty list if not logged in

    with get_db_connection() as conn:
        messages = conn.execute("SELECT * FROM messages WHERE email = ?", (session.get('email'),)).fetchall()  # Use email instead of user_id

    # Convert messages to a list of dictionaries
    messages_list = [{'id': message['id'], 'content': message['content'], 'response': message['response']} for message in messages]
    return {'messages': messages_list}

@app.route('/fetch_all_messages')
def fetch_all_messages():
    with get_db_connection() as conn:
        messages = conn.execute("SELECT * FROM messages").fetchall()

    # Convert messages to a list of dictionaries
    messages_list = [{'id': message['id'], 'email': message['email'], 'content': message['content'], 'response': message['response']} for message in messages]  # Use email instead of user_id
    return {'messages': messages_list}

@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("You are not authorized to access this page.")
        return redirect(url_for('login'))  # Redirect to login if not authorized

    # Fetch user information from the database
    conn = get_db_connection()
    user = conn.execute("SELECT email, name, address, gender, role FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    conn.close()

    return render_template('profile.php', user=user)  # Pass user data to the template

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    total_price = 0.0
    products = {}

    # Fetch product details from the database
    with get_db_connection() as conn:
        for item_id, quantity in cart_items.items():
            product = conn.execute("SELECT * FROM products WHERE id = ?", (item_id,)).fetchone()
            if product:
                discounted_price = product['price'] * (1 - product['discount'] / 100)
                products[item_id] = {
                    'title': product['title'],
                    'price': discounted_price,
                    'image_path': product['image_path'],  # Include image_path
                    'quantity': quantity,
                    'total': discounted_price * quantity
                }
                total_price += discounted_price * quantity

    # Pass both products and cart_items to the template
    return render_template('cart.php', products=products, cart_items=cart_items, total_price=total_price)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    
    # Fetch product details from the database
    with get_db_connection() as conn:
        product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if product:
            cart[product_id] = cart.get(product_id, 0) + 1  # Increment quantity or set to 1
            session['cart'] = cart
            flash('Product added to cart!')
        else:
            flash('Product not found!')

    return redirect(url_for('product'))  # Redirect to product list or cart page

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    cart = session.get('cart', {})
    quantity = request.json.get('quantity', 1)  # Get quantity from JSON body

    if quantity is None or quantity < 1:
        # If quantity is 0 or invalid, remove the product from the cart
        cart.pop(product_id, None)  # Remove the product if it exists
        flash('Product removed from cart!')
    else:
        # Update the quantity in the cart
        cart[product_id] = quantity
        flash('Product quantity updated!')

    session['cart'] = cart
    return jsonify(success=True)  # Return a success response

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    
    if product_id in cart:
        del cart[product_id]  # Remove the product from the cart
        session['cart'] = cart  # Update the session cart
        flash('Product removed from cart!')
        return jsonify(success=True)  # Return a success response
    else:
        return jsonify(success=False, message='Product not found in cart!'), 404  # Return an error response

if __name__ == '__main__':
    create_users_table()  # Create the users table when the app starts
    create_products_table()  # Create the products table when the app starts
    create_messages_table()  # Create the messages table when the app starts
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run on all interfaces
