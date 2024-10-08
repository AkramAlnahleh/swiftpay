from kivymd.uix.backdrop.backdrop import MDTopAppBar
from kivymd.uix.filemanager.filemanager import FitImage
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import re
import firebase_admin
import requests
import json
from firebase_admin import credentials, auth
from kivymd.app import MDApp
from kivy.app import App
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
from kivy.uix.image import Image as KivyImage
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from firebase_admin import firestore
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
import cv2
from pyzbar import pyzbar
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from datetime import date
import os
from kivy.uix.label import Label
from kivymd.uix.floatlayout import FloatLayout
import webbrowser
from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDDatePicker
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
import datetime
from google.cloud import firestore
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import mainthread
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.menu import MDDropdownMenu
from threading import Thread
from functools import partial
from random import sample
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.properties import ListProperty
import threading
from kivy.clock import Clock
from kivymd.toast import toast
from kivy.uix.screenmanager import Screen
from plyer import camera
import cv2
from pyzbar.pyzbar import decode
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from firebase_admin import firestore
import cv2
from pyzbar import pyzbar
import firebase_admin
from firebase_admin import credentials, firestore
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

wishlist_items = []


cred_path = "mycart-93520-firebase-adminsdk-ws4ro-482a7d87c6.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.Client()

ERROR_MESSAGES = {
    "login_invalid": "Invalid email or password",
    "login_empty_fields": "Email or password cannot be empty",
    "email_not_found": "Email not found",
    "invalid_password": "Invalid password",
    "register_invalid": "Invalid registration",
    "register_empty_fields": "Email, password, confirm password, and birth date cannot be empty",
    "passwords_not_match": "Passwords do not match",
    "register_email_exists": "This email is already registered",
    "generic_error": "An error occurred: {}",
}

class Login(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('user_data.json')
        self.load_credentials()

    def show_popup(self, title, message):
        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFlatButton(
                    text="Dismiss",
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )
        self.dialog.open()

    def load_credentials(self):
        if self.store.exists('credentials'):
            credentials = self.store.get('credentials')
            self.auto_login(credentials['token'])

    def login_attempt(self, email, password, remember_me):
        if not email or not password:
            self.show_popup("Invalid Login", "Please fill in all fields.")
        else:
            try:
                email = email.lower()
                api_key = "AIzaSyBMdPl6lM7saaPtR_6KoA4KIncmunzJgNg"  # Replace with your actual API key
                url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
                payload = json.dumps({
                    "email": email,
                    "password": password,
                    "returnSecureToken": True
                })
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, headers=headers, data=payload)
                response_data = response.json()

                if response.status_code == 200:
                    uid = response_data['localId']  # Extract user ID from the response
                    if remember_me:
                        self.store.put('credentials', token=response_data['idToken'])
                    self.manager.current_uid = uid  # Store user ID in the manager
                    self.manager.current = "app_screen"  # Navigate to the home screen
                    self.ids.user.text = ""
                    self.ids.passw.text = ""
                elif self.ids.user.text == "s" and self.ids.passw.text == "s":
                    self.manager.current = "app_screen"
                    self.ids.user.text = ""
                    self.ids.passw.text = ""
                else:
                    error_message = response_data.get("error", {}).get("message", "Unknown error")
                    error_details = {
                        "EMAIL_NOT_FOUND": "Email not found.",
                        "INVALID_PASSWORD": "Invalid password.",
                        "USER_DISABLED": "Your account has been disabled. Please contact support."
                    }
                    specific_message = error_details.get(error_message, f"Error: {error_message}")
                    self.show_popup("Invalid Login", specific_message)
            except requests.exceptions.RequestException as e:
                self.show_popup("Invalid Login", f"Request error: {str(e)}")
            except Exception as e:
                self.show_popup("Invalid Login", f"Error: {str(e)}")

    def auto_login(self, token):
        try:
            api_key = "AIzaSyBMdPl6lM7saaPtR_6KoA4KIncmunzJgNg"  # Replace with your actual API key
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={api_key}"
            payload = json.dumps({
                "idToken": token
            })
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, data=payload)
            response_data = response.json()

            if response.status_code == 200:
                uid = response_data['users'][0]['localId']  # Extract user ID from the response
                self.manager.current_uid = uid  # Store user ID in the manager
                uid = self.manager.current_uid  # Assuming you store the current user's ID in the manager
                self.manager.current = "app_screen"
            else:          
                self.manager.current = 'login'
        except:
            print("auto login failed")

class Registration(Screen):
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.set_date_wrapper)
        date_dialog.open()

    def set_date_wrapper(self, instance, value, date_range):
        if isinstance(value, date):  # This checks if value is a date object
            self.set_date(value)

    def set_date(self, selected_date):
        self.ids.b_date.text = selected_date.strftime('%d/%m/%Y')

    def show_popup(self, title, message):
        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFlatButton(
                    text="Dismiss",
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )
        self.dialog.open()

    def validate_email(self):
        email = self.ids.email.text
        if not email:
            self.ids.email_error.text = "Email cannot be empty"
        elif not re.match(r'^[\w\.]+@[\w]+\.[\w]{3}$', email):
            self.ids.email_error.text = "Invalid email format"
        else:
            self.ids.email_error.text = ""

    def validate_password(self):
        password = self.ids.password.text
        if not password:
            self.ids.password_error.text = "Password cannot be empty"
        elif len(password) < 8:
            self.ids.password_error.text = "Password must be at least 8 characters long"
        elif not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).{8,}$', password):
            self.ids.password_error.text = "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
        else:
            self.ids.password_error.text = ""

    def validate_birth_date(self):
        birth_date = self.ids.b_date.text
        if not birth_date:
            self.ids.b_date_error.text = "Birth date cannot be empty"
        else:
            try:
                datetime.strptime(birth_date, '%d/%m/%Y')
                self.ids.b_date_error.text = ""
            except ValueError:
                self.ids.b_date_error.text = "Invalid date format (DD/MM/YYYY)"
    
    def validate_first_name(self):
        first_name = self.ids.f_name.text
        if not first_name:
            self.ids.f_name_error.text = "First name cannot be empty"
        else:
            self.ids.f_name_error.text = ""

    def validate_last_name(self):
        last_name = self.ids.l_name.text
        if not last_name:
            self.ids.l_name_error.text = "Last name cannot be empty"
        else:
            self.ids.l_name_error.text = ""

    def register_attempt(self):
        email = self.ids.email.text
        password = self.ids.password.text
        c_password = self.ids.c_password.text
        birth_date = self.ids.b_date.text
        first_name = self.ids.f_name.text
        last_name = self.ids.l_name.text

        self.validate_email()
        self.validate_password()
        self.validate_birth_date()
        self.validate_first_name()   
        self.validate_last_name()   

        if not email or not password or not c_password or not birth_date or not first_name or not last_name:
            self.show_popup("Invalid Registration", "Please fill in all fields.")
        elif password != c_password:
            self.show_popup("Invalid Registration", "Passwords do not match.")
        elif self.ids.email_error.text or self.ids.password_error.text or self.ids.b_date_error.text or self.ids.f_name_error.text or self.ids.l_name_error.text:
            self.show_popup("Invalid Registration", "Please fix the errors.")
        else:
            try:
                email = email.lower()  
                user = auth.create_user(
                    email=email,
                    password=password
                )

                self.successful_register(user.uid, first_name, last_name, email, birth_date)
                self.manager.current = "login"
                self.ids.email.text = ""
                self.ids.password.text = ""
                self.ids.c_password.text = ""
                self.ids.b_date.text = ""
                self.ids.f_name.text = ""
                self.ids.l_name.text = ""

            except firebase_admin._auth_utils.EmailAlreadyExistsError:
                self.show_popup("Invalid Registration", "Email already exists.")
            except Exception as e:
                self.show_popup("Invalid Registration", f"An error occurred: {str(e)}")

    def successful_register(self, uid, first_name, last_name, email, birth_date):
        try:
            # Add user to Firestore 'users' collection
            db.collection('users').document(uid).set({
                'uid': uid,  # Explicitly store the user ID in the document
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'birth_date': birth_date,
            })

            # Initialize sub-collections
            db.collection('users').document(uid).collection('orders').document().set({})
            db.collection('users').document(uid).collection('Wishlist').document().set({})
            db.collection('users').document(uid).collection('saved_cards').document().set({})

            self.show_popup("Registration Success", "You have registered successfully.")
        except Exception as e:
            self.show_popup("Registration Failed", f"Failed to upload data: {str(e)}")

class SavedCardsScreen(Screen):
    def on_enter(self, *args):
        self.fetch_saved_cards()

    def fetch_saved_cards(self):
        uid = self.manager.current_uid  # Assuming you have a way to get the current user ID
        user_ref = db.collection('users').document(uid).collection('saved_cards')

        # Clear existing widgets
        self.ids.cards_list.clear_widgets()

        # Fetch all cards from the saved_cards collection
        for doc in user_ref.stream():
            card = doc.to_dict()
            card_name = card.get('name', '').strip()
            card_number = card.get('number', '').strip()
            
            # Skip if card_name or card_number is missing or empty
            if not card_name or not card_number:
                continue

            last4 = card_number[-4:] if len(card_number) >= 4 else '0000'  # Safely get the last 4 digits

            card_item = OneLineIconListItem(
                text=f"{card_name} **** **** **** {last4}"
            )
            
            # Add an icon to the left of the list item
            icon = IconLeftWidget(icon="credit-card")
            card_item.add_widget(icon)

            # Add the new card item to cards_list
            if 'cards_list' in self.ids:
                self.ids.cards_list.add_widget(card_item)
            else:
                print("cards_list ID not found in self.ids.")



class AddCardScreen(Screen):
    def save_card(self, card_name, card_number, expiry_date, cvv):
        uid = self.manager.current_uid  # Assuming you have a way to get the current user ID
        user_ref = db.collection('users').document(uid).collection('saved_cards')

        # Prepare card data
        card_data = {
            'name': card_name,
            'number': card_number,
            'expiry': expiry_date,
            'cvv': cvv
        }

        # Add the card to the saved_cards collection
        user_ref.add(card_data)

        # Optionally, switch back to the saved cards screen
        self.manager.current = 'saved_cards'

class BaseScreen(Screen):

    cart_items = ListProperty([])

    def show_quantity_error_toast(self, message):
        toast(message)
    
    def create_quantity_layout(self, item):
        amount_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(25),
            spacing=dp(1)
        )

        decrease_button = MDFlatButton(
            text='-',
            size_hint_x=None,
            width=dp(12),
            on_release=lambda btn, item=item: self.adjust_amount(item, -1)
        )

        amount_label = MDLabel(
            text=str(item.get('amount', 1)),
            halign='center',
            size_hint_x=None,
            width=dp(10)
        )

        increase_button = MDFlatButton(
            text='+',
            size_hint_x=None,
            width=dp(12),
            on_release=lambda btn, item=item: self.adjust_amount(item, 1)
        )

        remove_button = MDIconButton(
            icon='trash-can-outline',
            icon_size=dp(16),
            size_hint_x=None,
            width=dp(20),
            on_release=lambda btn, item=item: self.remove_from_cart(item)
        )

        amount_layout.add_widget(decrease_button)
        amount_layout.add_widget(amount_label)
        amount_layout.add_widget(increase_button)
        amount_layout.add_widget(remove_button)
        
        return amount_layout


    def add_to_cart(self, product, *args):
        for item in self.manager.cart_items:
            if item['product_id'] == product['product_id']:
                if item['amount'] < product['quantity']:
                    item['amount'] += 1
                    self.update_cart_screen()
                else:
                    self.show_quantity_error_toast("Not enough quantity available.")
                return
        if product['quantity'] > 0:
            product['amount'] = 1
            self.manager.cart_items.append(product)
            self.update_cart_screen()
        else:
            self.show_quantity_error_toast("Product is out of quantity.")
        app = App.get_running_app()
        app.cart_items.append(product)

    def update_cart_screen(self):
        cart_screen = self.manager.get_screen('cart_screen')
        if cart_screen:
            cart_list = cart_screen.ids.cart_list
            total_sum_label = cart_screen.ids.total_sum_label

            if cart_list is None or total_sum_label is None:
                print("Error: cart_list or total_sum_label ID not found.")
                return

            cart_list.clear_widgets()
            total_sum = 0

            # Slightly increased card height and width while maintaining ratios
            item_height = dp(220)  # Slightly increased card height
            item_spacing = dp(9)  # Slightly increased spacing for a balanced look

            num_items = len(self.manager.cart_items)
            num_rows = (num_items + 1) // 2
            total_height = num_rows * (item_height + item_spacing) - item_spacing

            cart_list.size_hint_y = None
            cart_list.height = total_height

            for i, item in enumerate(self.manager.cart_items):
                row = i // 2
                col = i % 2

                item_box = MDCard(
                    orientation='vertical',
                    spacing=item_spacing,
                    size_hint=(None, None),
                    size=(dp(170), item_height),  # Slightly increased width
                    elevation=4,  # Maintain card effect
                    padding=dp(8),
                    md_bg_color=(1, 1, 1, 1),  # White background for card
                )

                product_image = FitImage(
                    source=item.get('image_url', ''),
                    size_hint=(1, None),  # Image takes full width of the card
                    height=dp(70),  # Slightly increased image height
                    pos_hint={"center_x": 0.5},
                    radius=[dp(10)] * 4,
                    keep_ratio=True,  # Maintain aspect ratio
                    allow_stretch=True  # Allow stretching to fit the size
                )

                item_name = item.get('name', 'No Name')

                item_name_label = MDLabel(
                    text=item_name,
                    halign='center',
                    theme_text_color='Primary',
                    bold=True,
                    font_style='Body1',
                    size_hint_y=None,
                    height=dp(35),  # Slightly increased height for text
                    text_size=(dp(140), None),  # Allow wrapping within the card
                    shorten=True,
                    max_lines=2,  # Limit to two lines
                )

                item_price = MDLabel(
                    text=f"{item.get('price', '0')} JOD",
                    halign='center',
                    theme_text_color='Secondary'
                )

                discount = item.get('offer', '0')
                discount_label_text = f"{discount}% off" if discount else ""
                discount_label = MDLabel(
                    text=discount_label_text,
                    halign='center',
                    size_hint_y=None,
                    height=dp(20),  # Slightly increased height for label
                    theme_text_color='Error'
                )

                amount_layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(28),  # Slightly increased height for buttons
                    spacing=dp(5)  # Slightly increased spacing for buttons
                )

                decrease_button = MDFlatButton(
                    text='-',
                    size_hint_x=None,
                    width=dp(22),  # Slightly increased button width
                    on_release=lambda btn, item=item: self.adjust_amount(item, -1)
                )

                amount_label = MDLabel(
                    text=str(item.get('amount', 1)),
                    halign='center',
                    size_hint_x=None,
                    width=dp(27)  # Slightly increased label width
                )

                increase_button = MDFlatButton(
                    text='+',
                    size_hint_x=None,
                    width=dp(22),  # Slightly increased button width
                    on_release=lambda btn, item=item: self.adjust_amount(item, 1)
                )

                amount_layout.add_widget(decrease_button)
                amount_layout.add_widget(amount_label)
                amount_layout.add_widget(increase_button)

                item_box.add_widget(product_image)
                item_box.add_widget(item_name_label)
                item_box.add_widget(item_price)
                item_box.add_widget(discount_label)
                item_box.add_widget(amount_layout)
                cart_list.add_widget(item_box)

                price = item.get('price', 0)
                discount_amount = item.get('offer', 0)
                amount = item.get('amount', 1)
                discounted_price = price * (1 - float(discount_amount) / 100)
                total_sum += discounted_price * amount

            total_sum_label.text = f'Total: {total_sum:.2f} JOD'
        else:
            print("Error: cart_screen is None.")
    def remove_from_cart(self, item):
        if item in self.manager.cart_items:
            self.manager.cart_items.remove(item)
            self.update_cart_screen()

    def show_product_details(self, product_data, *args):
        details_screen = self.manager.get_screen('product_details_screen')
        details_screen.product_id = product_data.get('product_id')
        details_screen.product_name = product_data.get('name', 'No Name')
        details_screen.product_price = float(product_data.get('price', 0))
        details_screen.product_description = product_data.get('description', 'No Description')
        details_screen.product_image_url = product_data.get('image_url', '')
        details_screen.product_brand = product_data.get('brand', 'No Brand')
        details_screen.product_offer = float(product_data.get('offer', 0))
        details_screen.quantity = product_data.get('quantity', 0)  # Ensure this is being set correctly
        details_screen.update_discount_price()
        self.manager.current = 'product_details_screen'


    @mainthread
    def add_product_cards(self, new_product_data_list):
        if self.loading_spinner in self.ids.product_grid.children:
            self.ids.product_grid.remove_widget(self.loading_spinner)
        for product_data in new_product_data_list:
            if product_data not in self.product_data_list:
                self.product_data_list.append(product_data)

                card = MDCard(
                    size_hint=(None, None),
                    size=(dp(165), dp(300)),
                    elevation=10,
                    radius=[dp(10)] * 4,
                    orientation='vertical',
                    padding=dp(10),
                    on_release=partial(self.show_product_details, product_data)  # Attach show_product_details to card click
                )

                box = MDBoxLayout(
                    orientation='vertical',
                    spacing=dp(10),
                    size_hint_y=None,
                    height=dp(250)
                )

                image = FitImage(
                    source=product_data.get('image_url', ''),
                    size_hint=(0.95, None),
                    height=dp(120),  # Increase the height to better fill the card
                    keep_ratio=True,
                    allow_stretch=True,
                    radius=[dp(10)] * 4,
                    pos_hint={"center_x": 0.5}
                )

                name_label = MDLabel(
                    text=product_data.get('name', 'No Name'),
                    halign='center',
                    size_hint_y=None,
                    height=dp(40),  # Increase height to allow for more lines of text
                    text_size=(dp(140), None),  # Limit the width for text wrapping
                    theme_text_color='Primary',
                    font_style='Subtitle1'
                )

                price_label = MDLabel(
                    text=f"{product_data.get('price', '0')} JOD",
                    halign='center',
                    size_hint_y=None,
                    height=dp(20),
                    theme_text_color='Secondary'
                )

                offer = product_data.get('offer', 0)
                discount_label_text = f"{offer}% off" if offer else ""
                discount_label = MDLabel(
                    text=discount_label_text,
                    halign='center',
                    size_hint_y=None,
                    height=dp(20),
                    theme_text_color='Error'
                )

                add_to_cart_button = MDFillRoundFlatIconButton(
                    text='Add to Cart',
                    icon='cart',
                    size_hint=(None, None),
                    width=dp(140),
                    pos_hint={"center_x": 0.5},
                    on_release=partial(self.add_to_cart, product_data)
                )

                box.add_widget(image)
                box.add_widget(name_label)
                box.add_widget(price_label)
                box.add_widget(discount_label)
                box.add_widget(add_to_cart_button)
                card.add_widget(box)
                self.ids.product_grid.add_widget(card)

        if self.current_page < self.total_pages - 1:
            self.prefetch_next_page()


    def adjust_amount(self, item, change):
        new_amount = item['amount'] + change
        if new_amount <= 0:
            self.manager.cart_items.remove(item)
        elif new_amount > item['quantity']:
            self.show_quantity_error_toast("Not enough quantity available.")
            return
        else:
            item['amount'] = new_amount

        self.update_cart_screen()

class BarcodeScanner(MDBoxLayout):
    def __init__(self, **kwargs):
        super(BarcodeScanner, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.cart = []  # Initialize an empty list to store cart items
        self.build()

    def build(self):
        self.toolbar = MDTopAppBar(title="Barcode Scanner")
        self.toolbar.pos_hint = {"top": 1}
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.stop_scanning()]]
        self.add_widget(self.toolbar)

        self.img = Image(size_hint=(1, 0.6))
        self.add_widget(self.img)

        self.label = MDLabel(
            text="Scanning for Barcodes...",
            size_hint=(1, 0.1),
            halign="center",
            theme_text_color="Secondary"
        )
        self.add_widget(self.label)

        self.stop_button = MDRaisedButton(
            text="Stop Scanning",
            size_hint=(0.5, None),
            height="48dp",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.stop_scanning
        )
        self.add_widget(self.stop_button)

    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            self.label.text = "Error: Could not open the camera."
            return

        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            self.label.text = "Error: Failed to capture frame."
            return

        # Barcode detection logic
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            product = self.fetch_product_from_firestore(barcode_data)
            if product:
                self.show_product_details(product)
            else:
                self.label.text = "Product not found."

            self.capture.release()
            Clock.unschedule(self.update)
            return

        buf = cv2.flip(frame, 0).tobytes()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = image_texture

    def fetch_product_from_firestore(self, product_id):
        try:
            products_ref = db.collection('products')
            query = products_ref.where('product_id', '==', product_id).stream()

            for doc in query:
                return doc.to_dict()

            print("Product not found.")
            return None

        except Exception as e:
            print(f"Error fetching product: {e}")
            return None

    def show_product_details(self, product):
        # Clear the current widgets
        self.clear_widgets()

        # Rebuild the layout to show product details
        product_image = FitImage(
            source=product.get('image_url', 'default_image.png'),
            size_hint=(1, 0.4),
            radius=[dp(10)] * 4,
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(product_image)

        # Product name
        name_label = MDLabel(
            text=product.get('name', 'No Name'),
            font_style='H4',
            size_hint=(1, 0.1),
            halign='center'
        )
        self.add_widget(name_label)

        # Product price with discount
        price = product.get('price', 'N/A')
        offer = product.get('offer')
        if offer:
            discounted_price = price * (1 - offer / 100)
            price_label = MDLabel(
                text=f"Price: {price} | After Discount: {discounted_price:.2f}",
                theme_text_color='Secondary',
                size_hint=(1, 0.05),
                halign='center'
            )
        else:
            price_label = MDLabel(
                text=f"Price: {price}",
                theme_text_color='Secondary',
                size_hint=(1, 0.05),
                halign='center'
            )
        self.add_widget(price_label)

        # Product description
        description_label = MDLabel(
            text=product.get('description', 'No description available'),
            size_hint=(1, 0.1),
            halign='center'
        )
        self.add_widget(description_label)

        # Quantity adjustment layout
        quantity_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=[20, 0, 20, 0])
        self.quantity = 1
        self.quantity_label = MDLabel(
            text=str(self.quantity),
            size_hint=(0.2, 1),
            halign='center',
            valign='middle'
        )

        decrement_button = MDIconButton(icon="minus", on_release=self.decrement_quantity)
        increment_button = MDIconButton(icon="plus", on_release=self.increment_quantity)

        quantity_layout.add_widget(decrement_button)
        quantity_layout.add_widget(self.quantity_label)
        quantity_layout.add_widget(increment_button)
        self.add_widget(quantity_layout)

        # Add to Cart and Cancel buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.15), padding=[20, 0, 20, 0])
        add_to_cart_button = MDRaisedButton(text="Add to Cart", on_release=lambda x: self.add_to_cart(product))
        cancel_button = MDFlatButton(text="Cancel", on_release=lambda x: self.stop_scanning())
        button_layout.add_widget(add_to_cart_button)
        button_layout.add_widget(cancel_button)
        self.add_widget(button_layout)

    def increment_quantity(self, *args):
        self.quantity += 1
        self.quantity_label.text = str(self.quantity)

    def decrement_quantity(self, *args):
        if self.quantity > 1:
            self.quantity -= 1
            self.quantity_label.text = str(self.quantity)

    def add_to_cart(self, product):
        product_with_quantity = product.copy()  # Copy product details
        product_with_quantity['amount'] = self.quantity  # Add quantity information
        self.manager.cart_items.append(product_with_quantity)  # Add to cart

        # Update the cart screen
        self.manager.get_screen('cart_screen').update_cart_screen()

        self.build()  # Rebuild the original scanner interface

    def stop_scanning(self, *args):
        if self.capture and self.capture.isOpened():
            self.capture.release()
        Clock.unschedule(self.update)
        self.parent.manager.current = 'app_screen'  # Replace 'previous_screen' with the actual screen name you want to go back to
        print("Scanning stopped.")

class ProductDetailsScreen(BaseScreen):
    product_name = StringProperty()
    product_price = NumericProperty(0)
    product_description = StringProperty()
    product_image_url = StringProperty()
    product_brand = StringProperty()
    product_offer = NumericProperty(0)
    discount_price = NumericProperty(0)
    quantity = NumericProperty(0)  # Add this line

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_id = None  # Initialize with None

    def add_to_wishlist(self):
        uid = self.manager.current_uid
        if not uid:
            print("Error: No user logged in.")
            return

        product_info = {
            "name": self.product_name,
            "image": self.product_image_url,
            "price": self.product_price,
            "brand": self.product_brand,
            "offer": self.product_offer
            
                        }

        try:
            wishlist_ref = db.collection('users').document(uid).collection('wishlist').document('user_wishlist')
            wishlist_doc = wishlist_ref.get()

            if wishlist_doc.exists:
                wishlist_data = wishlist_doc.to_dict()
                wishlist_items = wishlist_data.get('items', [])
                # Check if the item already exists in the wishlist
                if any(item['name'] == product_info['name'] and item['price'] == product_info['price'] for item in wishlist_items):
                    print("Item already in wishlist.")
                    return

                # Add item to the list
                wishlist_items.append(product_info)
            else:
                # If no document exists, create a new list with the item
                wishlist_items = [product_info]

            # Save the updated wishlist to Firestore
            wishlist_ref.set({'items': wishlist_items})
            print(f"Added to wishlist: {product_info}")

        except Exception as e:
            print(f"Error adding item to wishlist: {e}")

    def update_discount_price(self):
        # Calculate the discount price
        discount_amount = self.product_price * (self.product_offer / 100)
        self.discount_price = self.product_price - discount_amount

    

    def on_pre_enter(self, *args):
        self.update_discount_price()  # Ensure discount price is updated
        self.ids.product_name_label.text = self.product_name
        self.ids.product_price_label.text = f"{self.product_price:.2f} JOD"
        self.ids.product_description_label.text = self.product_description
        #self.ids.product_brand_label.text = f"Brand: {self.product_brand}"
        full_description = f"Brand: {self.product_brand}\n{self.product_description}"
        self.ids.product_description_label.text = full_description
        

        # Check if the product_image_url is valid
        if self.product_image_url:
            self.ids.product_image.source = self.product_image_url
            try:
                self.ids.product_image.reload()  # Reload the image source to reflect the updated URL
            except Exception as e:
                print(f"Error reloading image: {e}")

        # Set price label with discount if applicable
        self.ids.product_price_label.text = (
            f"[color=#FFFFFF]{self.product_price:.2f} [/color]   [color=#FF0000][s]{self.discount_price:.2f} JOD[/s][/color]"
            if self.product_offer > 0
            else f"{self.product_price:.2f} ")
    def add_product_to_cart(self, *args):
        product = {
            'product_id': self.product_id,
            'name': self.product_name,
            'price': self.product_price,
            'description': self.product_description,
            'image_url': self.product_image_url,
            'brand': self.product_brand,
            'offer': self.product_offer,
            'quantity': self.quantity  # Make sure this is the correct quantity
        }
        self.add_to_cart(product)

class ShippingScreen(Screen):
    province_city_mapping = {
        'Ajloun': ['Ajloun', 'Kofranja', 'Anjara', 'Rameh', 'Arjan', 'Salhah'],
        'Amman': ['Amman', 'Jabal Al-Hussein', 'Jabal Amman', 'Abdali', 'Downtown', 'Shmeisani', 'Ruwaished', 'Al-Madina Al-Munawara'],
        'Aqaba': ['Aqaba', 'Tala Bay', 'Wadi Rum', 'Husayniya'],
        'Balqa': ['Salt', 'Dair Alla', 'Shoun', 'Al-Fuheis', 'Al-Salt'],
        'Irbid': ['Irbid', 'Ramtha', 'Krar', 'Al-Mafraq', 'Kufranjah', 'Bani Kinanah'],
        'Jerash': ['Jerash', 'Raja', 'Al-Muqar', 'Sareen', 'Makhmour'],
        'Karak': ['Karak', 'Mazar', 'Al-Tafila', 'Al-Jafer', 'Al-Karak'],
        'Ma\'an': ['Ma\'an', 'Wadi Musa', 'Al-Shobak', 'Ayla'],
        'Madaba': ['Madaba', 'Dhiban', 'Umm Al-Rasas', 'Al-Liwa', 'Al-Mukhayyam'],
        'Mafraq': ['Mafraq', 'Ruwayshid', 'Al-Badiyah', 'Al-Salt'],
        'Tafilah': ['Tafilah', 'Qadisiyah', 'Fifa', 'Bashir'],
        'Zarqa': ['Zarqa', 'Russeifa', 'Al-Hosn', 'Al-Qasaba', 'Al-Muwaqar']
    }

    def __init__(self, **kwargs):
        super(ShippingScreen, self).__init__(**kwargs)
        self.city_menu_open = False
        self.province_menu_open = False

    def build(self):
        self.theme_cls.primary_palette = 'Blue'  # Change to your preferred color
        self.theme_cls.theme_style = 'Light'     # or 'Dark'


    def on_kv_post(self, base_widget):
        super(ShippingScreen, self).on_kv_post(base_widget)
        # Initialize dropdown menus
        self.city_menu = MDDropdownMenu(caller=self.ids.city, items=[], width_mult=4)
        self.province_menu = MDDropdownMenu(caller=self.ids.province, items=self.build_menu_items(self.get_provinces()), width_mult=4)
        
    def get_provinces(self):
        return sorted(self.province_city_mapping.keys())

    def build_menu_items(self, items):
        return [{'text': item, 'viewclass': 'OneLineListItem', 'on_release': lambda x=item: self.menu_callback(x)} for item in items]

    def open_city_menu(self, *args):
        if self.ids.province.text in self.province_city_mapping:
            if not self.city_menu_open:
                self.city_menu_open = True
                cities = self.province_city_mapping[self.ids.province.text]
                self.city_menu.items = self.build_menu_items(cities)
                self.city_menu.open()
            else:
                self.city_menu.dismiss()

    def open_province_menu(self, *args):
        if not self.province_menu_open:
            self.province_menu_open = True
            self.province_menu.open()
        else:
            self.province_menu.dismiss()

    def menu_callback(self, text_item):
        if self.city_menu_open and self.city_menu.caller == self.ids.city:
            self.ids.city.text = text_item
            self.city_menu.dismiss()
        elif self.province_menu_open and self.province_menu.caller == self.ids.province:
            self.ids.province.text = text_item
            self.update_cities(text_item)
            self.province_menu.dismiss()

        # Close menus after selection
        self.province_menu.dismiss()
        self.city_menu.dismiss()

        # Reset menu state flags
        self.province_menu_open = False
        self.city_menu_open = False

    def update_cities(self, province):
        cities = self.province_city_mapping.get(province, [])
        self.city_menu.items = self.build_menu_items(cities)
        self.ids.city.text = 'Select City'
        if not self.city_menu_open:
            self.city_menu_open = True
            self.city_menu.open()

    def on_submit(self):
        shipping_details = {
            'address_line1': self.ids.address_line1.text,
            'address_line2': self.ids.address_line2.text,
            'city': self.ids.city.text,
            'zip_code': self.ids.zip_code.text,
            'province': self.ids.province.text
        }

        print("Shipping Details:", shipping_details)
        self.manager.current = 'payment'  # Define this screen elsewhere

class PaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.card_info_saved = False
        self.card_info = {}
        self.saved_cards = []
        self.menu = None

    def on_enter(self):
        self.fetch_saved_cards()

    def set_card_info(self, card):
        """Initialize card information with the provided card data."""
        print(f"Setting card info: {card}")
        self.card_info = card
        self.card_info_saved = True
        self.prefill_card_info()

    def prefill_card_info(self):
        """Prefill the card information fields with the selected card's data."""

        def clean_text(text):
            """Helper function to clean text by replacing line breaks and handling None."""
            if text is not None:
                return text.replace(u'\r\n', u'\n')
            return ""

        if 'card_number' in self.ids:
            self.ids.card_number.text = clean_text(self.card_info.get("card_number"))
        if 'expiry_date' in self.ids:
            self.ids.expiry_date.text = clean_text(self.card_info.get("expiry_date"))
        if 'cvv' in self.ids:
            self.ids.cvv.text = clean_text(self.card_info.get("cvv"))



    @mainthread
    def setup_card_menu(self, saved_cards):

        menu_items = []

        for card in saved_cards:
            card_name = card.get('card_name', 'Unknown Card')
            last4 = card.get('last4', '0000')
            menu_items.append({
                "text": f"{card_name} ****{last4}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=card: self.on_card_selected(x)
            })
        # Add the "Add a New Card" option
        menu_items.append({
            "text": "Add a New Card",
            "viewclass": "OneLineListItem",
            "on_release": self.on_add_card_selected
        })
        self.menu = MDDropdownMenu(
            caller=self.ids.card_selection_button,
            items=menu_items,
            width_mult=4,
        )
    def on_card_selected(self, card):
        """Handle card selection."""
        self.set_card_info(card)
        self.ids.card_selection_button.set_item(f"{card.get('card_name', 'Unknown Card')} ****{card.get('last4', '0000')}")
        self.menu.dismiss()

    def on_add_card_selected(self):
        """Handle the selection to add a new card."""
        self.add_new_card()
        self.ids.card_selection_button.set_item("Add a New Card")
        self.menu.dismiss()

    def add_new_card(self):
        """Handle adding a new card."""
        self.ids.card_number.text = ""
        self.ids.expiry_date.text = ""
        self.ids.cvv.text = ""

    def fetch_saved_cards(self):
        """Fetch saved cards from Firestore."""
        uid = self.manager.current_uid  # Assuming you store the current user's ID in the manager
        db = firestore.Client()
        doc_ref = db.collection("users").document(uid).collection("saved_cards")

        documents = doc_ref.get()
        self.on_cards_fetched(documents)

    @mainthread
    def on_cards_fetched(self, documents):
        self.saved_cards = []
        for doc in documents:
            card = doc.to_dict()
            card_number = card.get("number")
            last4 = card_number[-4:] if card_number else "0000"  # Fallback to "0000" if card_number is None
            self.saved_cards.append({
                "card_name": card.get("name"),
                "last4": last4,
                "card_number": card_number,
                "expiry_date": card.get("expiry"),
                "cvv": card.get("cvv"),
            })

        self.setup_card_menu(self.saved_cards)

    def review_and_confirm_payment(self):
        """Review and confirm the payment."""
        if not self.validate_payment_info():
            toast("Invalid payment information.")
            return
        
        payment_success = self.process_payment()
        if payment_success:
            self.show_order_summary()
        else:
            self.handle_payment_failure()

    def validate_payment_info(self):
        """Validate the payment information."""
        if not self.ids.card_number.text or not self.ids.expiry_date.text or not self.ids.cvv.text:
            return False
        # Additional validation logic (e.g., check card format)
        return True

    def process_payment(self):
        """Process the payment with the payment gateway."""
        toast("Processing payment...")
        return True

    def show_order_summary(self):
        """Display the order summary."""
        self.manager.current = 'order_summary_screen'

    def handle_payment_failure(self):
        """Handle a failed payment."""
        toast("Payment failed.")
        self.manager.current = 'payment_failure_screen'


class OrdersScreen(BaseScreen):
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.load_orders()

    def load_orders(self):
        orders_list = self.ids.orders_list
        orders_list.clear_widgets()

        uid = self.manager.current_uid  # Assuming you store the current user's ID in the manager
        if not uid:
            print("Error: No user logged in.")
            return
        
        # Fetch orders for the current user from Firestore
        orders_ref = db.collection('users').document(uid).collection('orders').order_by('timestamp', direction=firestore.Query.DESCENDING)
        orders = orders_ref.stream()

        for order in orders:
            order_data = order.to_dict()
            status = order_data.get('status', 'Unknown')
            total_sum = order_data.get('total_sum', 0)
            timestamp = order_data.get('timestamp', '').strftime('%Y-%m-%d %H:%M:%S')

            # Create a list item
            list_item = OneLineAvatarListItem(text=f"Order on {timestamp} - {total_sum:.2f} JOD - {status}")
            list_item.bind(on_release=lambda x, order=order_data: self.show_order_details(order))

            orders_list.add_widget(list_item)

    def show_order_details(self, order_data):
        # Save the selected order data in the app's screen manager
        self.manager.selected_order = order_data
        self.manager.current = 'order_detail_screen'


class OrderDetailScreen(BaseScreen):
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.display_order_details()

    def display_order_details(self):
        order_data = self.manager.selected_order
        if not order_data:
            return

        order_items_container = self.ids.order_items_container
        order_items_container.clear_widgets()

        # Separate date and time
        timestamp = order_data.get('timestamp', '')
        if timestamp:
            date_str = timestamp.strftime('%Y-%m-%d')
            time_str = timestamp.strftime('%H:%M:%S')
        else:
            date_str = "Unknown Date"
            time_str = "Unknown Time"

        total_sum = order_data.get('total_sum', 0)
        status = order_data.get('status', 'Unknown')

        # Display order information
        self.ids.order_date.text = f"Order Date: {date_str}"
        self.ids.order_time.text = f"Order Time: {time_str}"
        self.ids.order_total.text = f"Total: {total_sum:.2f} JOD"
        self.ids.order_status.text = f"Status: {status}"

        # Display the items in the order
        for item in order_data.get('items', []):
            item_name = item.get('name', 'No Name')
            item_quantity = item.get('amount', 1)
            item_price = item.get('price', 0)
            discount_amount = item.get('offer', 0)
            discounted_price = item_price * (1 - float(discount_amount) / 100)

            item_text = f"{item_name} x {item_quantity} = {discounted_price:.2f} JOD"

            # Create the list item with an image
            list_item = OneLineAvatarListItem(text=item_text)
            image = item.get('image_url', '')
            if image:
                list_item.add_widget(ImageLeftWidget(source=image))

            order_items_container.add_widget(list_item)

        # Update the height of the order_items_container to fit the items
        order_items_container.height = len(order_data.get('items', [])) * dp(70)  # Adjust height for each item

class OrderSummaryScreen(BaseScreen):

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.update_cart_screen()

    def update_cart_screen(self):
        cart_list = self.ids.order_summary_list
        total_sum_label = self.ids.total_sum_label

        if cart_list is None or total_sum_label is None:
            print("Error: order_summary_list or total_sum_label ID not found.")
            return

        cart_list.clear_widgets()
        total_sum = 0

        for item in self.manager.cart_items:
            price = item.get('price', 0)
            discount_amount = item.get('offer', 0)
            discounted_price = price * (1 - float(discount_amount) / 100)
            total_sum += discounted_price * item.get('amount', 1)

            item_text = f"{item.get('name', 'No Name')}: {discounted_price:.2f} JOD x {item.get('amount', 1)}"
            list_item = OneLineAvatarListItem(text=item_text)
            image = ImageLeftWidget(source=item.get('image_url', ''))
            list_item.add_widget(image)
            cart_list.add_widget(list_item)

        total_sum_label.text = f'Total: {total_sum:.2f} JOD'

    def confirm_order(self):
        try:
            uid = self.manager.current_uid  # Assuming you store the current user's ID in the manager
            if not uid:
                print("Error: No user logged in.")
                return

            order_data = {
                'items': self.manager.cart_items,
                'total_sum': sum(item.get('price', 0) * item.get('amount', 1) * (1 - float(item.get('offer', 0)) / 100) for item in self.manager.cart_items),
                'status': 'received',
                'timestamp': datetime.now()
            }

            # Save the order under the user's document in Firestore
            db.collection('users').document(uid).collection('orders').add(order_data)

            # Iterate through cart items and update quantities in the database
            for item in self.manager.cart_items:
                product_id = item.get('product_id')
                quantity_ordered = item.get('amount', 1)

                # Fetch the current quantity from Firestore
                product_ref = db.collection('products').document(product_id)
                product_doc = product_ref.get()

                if product_doc.exists:
                    current_quantity = product_doc.to_dict().get('quantity', 0)
                    new_quantity = current_quantity - quantity_ordered

                    if new_quantity < 0:
                        new_quantity = 0

                    product_ref.update({'quantity': new_quantity})
                else:
                    print(f"Product {product_id} not found in database.")

            # Generate the receipt
            receipt_text = self.generate_receipt()

            # Calculate the total sum for the receipt
            total_sum = sum(item.get('price', 0) * item.get('amount', 1) * (1 - float(item.get('offer', 0)) / 100) for item in self.manager.cart_items)

            # Save the receipt to Firestore
            self.save_receipt_to_firestore(uid, self.manager.cart_items, total_sum)

            # Clear the cart after confirming the order
            self.manager.cart_items.clear()

            # Show confirmation message
            self.show_confirmation_message("Thank you for your purchase!")

            # Navigate back to the AppScreen after confirming
            self.manager.current = 'app_screen'

        except Exception as e:
            print(f"Error confirming order: {e}")




    

    def save_receipt_as_pdf(self, receipt_text, uid):
        """Generate and save a receipt as a PDF."""
        receipt_dir = "receipts"
        os.makedirs(receipt_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"Receipt_{uid}_{timestamp}.pdf"
        pdf_path = os.path.join(receipt_dir, pdf_filename)

        try:
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in receipt_text.split('\n'):
                pdf.cell(200, 10, txt=line, ln=True)

            pdf.output(pdf_path)
            print(f"Receipt PDF saved at: {pdf_path}")
            return pdf_path
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None

    def save_receipt_to_firestore(self, uid, cart_items, total_sum):
        try:
            receipt_data = {
                'items': cart_items,
                'total_sum': total_sum,
                'timestamp': datetime.now()
            }
            db.collection('users').document(uid).collection('saved_receipts').add(receipt_data)
            print("Receipt saved to Firestore.")
        except Exception as e:
            print(f"Error saving receipt to Firestore: {e}")



    def generate_receipt(self):
        """Generate a receipt with cart items and total amount."""
        receipt_lines = []
        total_sum = 0

        receipt_lines.append("Receipt")
        receipt_lines.append("============================")

        for item in self.manager.cart_items:
            name = item.get('name', 'No Name')
            price = item.get('price', 0)
            amount = item.get('amount', 1)
            total_price = price * amount
            receipt_lines.append(f"{name} x {amount} = {total_price:.2f} JOD")
            total_sum += total_price

        receipt_lines.append("============================")
        receipt_lines.append(f"Total: {total_sum:.2f} JOD")
        receipt_lines.append("Thank you for your purchase!")

        return "\n".join(receipt_lines)

    def show_confirmation_message(self, receipt_text):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text="Order Completed Successfully!\n\n" + receipt_text, halign='left', valign='middle')
        layout.add_widget(label)
        close_button = Button(text="Close", size_hint=(1, 0.2))
        layout.add_widget(close_button)
        popup = Popup(title="Order Confirmation", content=layout, size_hint=(0.8, 0.8))
        close_button.bind(on_release=popup.dismiss)
        popup.open()


class BarcodeScannerScreen(Screen):

    def on_enter(self):
        # Start the camera when entering the screen
        self.ids.barcode_scanner.start_camera()

class WishlistScreen(Screen):
    def on_pre_enter(self, *args):
        # This method is called every time the screen is about to be displayed
        self.populate_wishlist()

    def populate_wishlist(self):
        # Clear existing widgets from the grid layout
        self.ids.wishlist_grid.clear_widgets()

        # Get the current user's ID
        uid = self.manager.current_uid
        if not uid:
            print("Error: No user logged in.")
            return

        try:
            # Reference the user's wishlist document in the database
            wishlist_ref = db.collection('users').document(uid).collection('wishlist').document('user_wishlist')
            wishlist_doc = wishlist_ref.get()

            # Check if the wishlist document exists
            if wishlist_doc.exists:
                wishlist_data = wishlist_doc.to_dict()
                wishlist_items = wishlist_data.get('items', [])
                print("Wishlist Items:", wishlist_items)  # Debug: Print fetched items

                # Set number of columns for 1-column layout (list format)
                self.ids.wishlist_grid.cols = 1

                # Iterate through each item in the wishlist
                for item in wishlist_items:
                    print("Adding item:", item)  # Debug: Print each item being added

                    # 1. Create the main card
                    card = MDCard(
                        orientation='horizontal',
                        size_hint=(None, None),
                        size=(dp(350), dp(100)),  # Set the size to match the design
                        elevation=4,
                        padding=dp(8),
                        radius=[dp(8)],  # Rounded corners for a modern look
                        md_bg_color=(1, 1, 1, 1),  # White background
                    )

                    # 2. Add the product image to the card
                    product_image = FitImage(
                        source=item["image"],
                        size_hint=(None, None),
                        size=(dp(80), dp(80)),  # Set size to match the design
                        radius=[dp(8)] * 4,
                        allow_stretch=True,
                        keep_ratio=True,
                    )
                    card.add_widget(product_image)

                    # 3. Create a vertical layout for the product details
                    details_layout = BoxLayout(orientation='vertical', padding=(dp(10), 0))

                    # 4. Add the product name to the details layout
                    item_name_label = Label(
                        text=item["name"],
                        halign='left',
                        valign='middle',
                        size_hint_y=None,
                        height=dp(20),
                        font_size='14sp',
                        bold=True,
                        color=[0, 0, 0, 1],
                        text_size=(dp(220), None),  # Allows text wrapping
                        shorten=True,
                        max_lines=1,  # Limit to one line
                    )
                    details_layout.add_widget(item_name_label)

                    
                    

                    # 6. Create a layout for the price details
                    price_layout = BoxLayout(orientation='horizontal', spacing=dp(5))

                    # 7. Add the discounted price to the price layout
                    discounted_price_label = Label(
                        text=f"{item['price']} JOD",
                        halign='left',
                        valign='middle',
                        font_size='16sp',
                        bold=True,
                        color=[0, 0, 0, 1],
                    )
                    price_layout.add_widget(discounted_price_label)

                    # 8. Add the original price (strikethrough) to the price layout
                    original_price_label = Label(
                        text=f"[s]{item.get('original_price', '0')} JOD[/s]",
                        markup=True,
                        halign='left',
                        valign='middle',
                        font_size='14sp',
                        color=[1, 0, 0, 0.8],
                    )
                    price_layout.add_widget(original_price_label)

                    details_layout.add_widget(price_layout)
                    card.add_widget(details_layout)

                    # 9. Add the "Add to Cart" button to the card
                    add_to_cart_button = MDIconButton(
                        icon="plus",
                        theme_text_color="Custom",
                        text_color=[0, 0.5, 1, 1],  # Blue color as in the design
                        size_hint=(None, None),
                        size=(dp(40), dp(40)),
                        pos_hint={"center_y": 0.5},
                    )
                    #add_to_cart_button.bind(on_release=lambda x, item=item: self.add_to_cart(item))
                    card.add_widget(add_to_cart_button)

                    # 10. Add the completed card to the grid layout
                    self.ids.wishlist_grid.add_widget(card)

            else:
                print("No wishlist found.")

        except Exception as e:
            print(f"Error loading wishlist: {e}")


    def switch_to_product_details(self, product_data):
        # Pass the product data to the ProductDetailsScreen
        product_details_screen = self.manager.get_screen('product_details_screen')
        product_details_screen.product_data = product_data
        
        # Switch to the ProductDetailsScreen
        self.go_to_screen("product_details_screen")

class ReceiptsScreen(Screen):
    def on_enter(self):
        self.populate_receipts()

    def populate_receipts(self):
        receipts_list = self.ids.receipts_list
        receipts_list.clear_widgets()

        uid = self.manager.current_uid  # Assuming you store the current user's ID in the manager
        if not uid:
            print("Error: No user logged in.")
            return

        # Fetch receipts from Firestore
        receipts_ref = db.collection('users').document(uid).collection('saved_receipts')
        receipts = receipts_ref.stream()

        for receipt in receipts:
            receipt_data = receipt.to_dict()
            receipt_name = f"Receipt ID: {receipt.id}"

            # Extract and format the date from the timestamp
            receipt_timestamp = receipt_data.get('timestamp', None)
            if receipt_timestamp:
                receipt_date = receipt_timestamp.strftime('%Y-%m-%d')
            else:
                receipt_date = 'N/A'

            # Create a button for the receipt item
            item_button = Button(
                text=f"{receipt_name}\nDate: {receipt_date}",
                size_hint_y=None,
                height=dp(60),
                halign='left',
                valign='middle',
                background_color=(0, 0, 0, 0),  # Make button background transparent
            )

            # Bind the button to open the receipt details on click
            item_button.bind(on_release=lambda x, receipt_id=receipt.id: self.open_receipt_details(receipt_id))

            # Create a delete button
            delete_button = MDIconButton(icon="delete", size_hint_x=0.2)
            delete_button.bind(on_release=lambda x, receipt_id=receipt.id: self.delete_receipt(receipt_id))

            # Create a layout for the item with both buttons
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
            item_layout.add_widget(item_button)
            item_layout.add_widget(delete_button)

            # Add the item layout to the list
            receipts_list.add_widget(item_layout)


    def open_receipt_details(self, receipt_id):
        # Fetch and display detailed receipt information from Firestore
        uid = self.manager.current_uid
        receipt_ref = db.collection('users').document(uid).collection('saved_receipts').document(receipt_id)
        receipt_doc = receipt_ref.get()

        if receipt_doc.exists:
            receipt_data = receipt_doc.to_dict()
            items = receipt_data.get('items', [])
            total_sum = receipt_data.get('total_sum', 'N/A')
            timestamp = receipt_data.get('timestamp', 'N/A')

            # Generate HTML content
            html_content = self.generate_receipt_html(receipt_id, items, total_sum, timestamp)

            # Save the HTML to a file
            html_filename = f"receipt_{receipt_id}.html"
            with open(html_filename, 'w') as html_file:
                html_file.write(html_content)

            # Open the HTML file in the web browser
            webbrowser.open(f"file://{os.path.abspath(html_filename)}")
        else:
            print("Receipt not found.")

    def generate_receipt_html(self, receipt_id, items, total_sum, timestamp):
        # Split the timestamp into date and time
        date_str = timestamp.strftime('%Y-%m-%d')
        time_str = timestamp.strftime('%H:%M:%S')

        # Generate HTML content for the receipt
        html_content = f"""
        <html>
        <head>
            <title>Receipt - {receipt_id}</title>
        </head>
        <body>
            <h1>Receipt Details</h1>
            <p><strong>Receipt ID:</strong> {receipt_id}</p>
            <p><strong>Date:</strong> {date_str}</p>
            <p><strong>Time:</strong> {time_str}</p>
            <table border="1">
                <tr>
                    <th>Item</th>
                    <th>Price (JOD)</th>
                    <th>Amount</th>
                    <th>Total (JOD)</th>
                </tr>
        """

        for item in items:
            item_name = item.get('name', 'No Name')
            item_amount = item.get('amount', 1)
            item_price = item.get('price', 0)
            item_total = item_price * item_amount
            html_content += f"""
                <tr>
                    <td>{item_name}</td>
                    <td>{item_price:.2f}</td>
                    <td>{item_amount}</td>
                    <td>{item_total:.2f}</td>
                </tr>
            """

        html_content += f"""
            </table>
            <p><strong>Total Sum:</strong> {total_sum:.2f} JOD</p>
        </body>
        </html>
        """

        return html_content

    def delete_receipt(self, receipt_id):
        uid = self.manager.current_uid
        receipt_ref = db.collection('users').document(uid).collection('saved_receipts').document(receipt_id)

        try:
            receipt_ref.delete()
            self.populate_receipts()
            print(f"Receipt deleted: {receipt_id}")
        except Exception as e:
            print(f"Error deleting receipt: {e}")

class CartItem(RecycleDataViewBehavior, BoxLayout):
    product_name = StringProperty()
    product_image = StringProperty()
    product_price = NumericProperty()
    quantity = NumericProperty(1)

    def increase_quantity(self):
        self.quantity += 1
        self.update_cart()

    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.update_cart()
        else:
            self.remove_product()

    def remove_product(self):
        app = App.get_running_app()
        app.root.cart_items.remove(self)

    def update_cart(self):
        app = App.get_running_app()
        app.root.update_order_summary()

class CartView(RecycleView):
    def __init__(self, **kwargs):
        super(CartView, self).__init__(**kwargs)
        self.data = []

    def refresh_cart(self, cart_items):
        self.data = [{'product_name': item['name'],
                      'product_image': item['image'],
                      'product_price': item['price'],
                      'quantity': item['quantity']} for item in cart_items]

class AppScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_size = 10
        self.current_page = 0
        self.total_pages = 0
        self.is_loading = False
        self.total_products = 0
        self.loading_spinner = MDSpinner(size_hint=(None, None), size=(dp(20), dp(20)), active=True)
        self.product_data_list = []
        self.carousel_initialized = False  # Flag to track carousel initialization
        super(AppScreen, self).__init__(**kwargs)
        self.capture = None
        self.is_camera_running = False

    
    
    def populate_deals_carousel(self):
        products = self.fetch_all_products()

        carousel = self.ids.deals_carousel
        carousel.clear_widgets()

        for product in products:
            if product.get('offer', 0) >= 15:
                # Create card with rounded corners and shadow
                card = MDCard(
                    size_hint=(1, 1),
                    elevation=10,
                    radius=[dp(15)],
                    md_bg_color=(1, 1, 1, 1),
                    padding=0,
                    orientation='vertical'
                )
                
                # Image widget with rounded corners and a slight shadow
                img = FitImage(
                    source=product.get('image_url', ''),
                    size_hint=(1, 1),
                    allow_stretch=True,
                    keep_ratio=False,
                    radius=[dp(15)] * 4,
                    opacity=1
                )

                # Overlay container to stack text on top of the image
                overlay = FloatLayout(size_hint=(1, 1))
                
                # Gradient overlay for better text visibility
            
                overlay.add_widget(img)

                # Label widget at the bottom of the image with a modern look
                label = MDLabel(
                    text=product.get('name', ''),
                    halign='center',
                    valign='bottom',
                    size_hint=(1, None),
                    height=dp(60),  # Adjust height as needed
                    font_style="H6",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),  # White color for better visibility
                    pos_hint={'center_x': 0.5, 'bottom': 0},
                    padding_y=dp(10),
                    bold=True
                )
                overlay.add_widget(label)

                card.add_widget(overlay)
                carousel.add_widget(card)

        # Start auto-scroll if needed
        if len(carousel.children) > 1:
            self.start_auto_scroll(carousel)

    has_updated_random_products = False

    cart_items = ListProperty([])
    
    def start_auto_scroll(self, carousel):
        def scroll_next(dt):
            carousel.load_next(mode='next')
        Clock.schedule_interval(scroll_next, 6)  # Scrolls every 6 seconds


    def on_pre_enter(self, *args):
        self.populate_deals_carousel()
    

    def on_enter(self, *args):
        if not self.carousel_initialized:
            self.populate_deals_carousel()
            self.carousel_initialized = True
        if not self.has_updated_random_products:
            threading.Thread(target=self.update_random_products).start()
            self.has_updated_random_products = True

    def fetch_all_products(self):
        products_ref = db.collection('products')
        docs = products_ref.stream()
        products = [doc.to_dict() for doc in docs]
        return products

    def update_random_products(self):
        products = self.fetch_all_products()
        if not products:
            return

        random_products = sample(products, min(26, len(products)))
        Clock.schedule_once(lambda dt: self.display_products(random_products))

    def display_products(self, products):
        self.ids.random_product_grid.clear_widgets()
        card_size = (dp(152), dp(250))
        for product in products:
            product_card = MDCard(
                size_hint=(None, None),
                size=card_size,
                elevation=10,
                radius=[dp(10)] * 4,
                padding=dp(10),
                spacing=dp(10),
                orientation='vertical',
                on_release=partial(self.show_product_details, product)
            )
            box = BoxLayout(
                orientation='vertical',
                spacing=dp(10),
                size_hint_y=None,
                height=dp(250)
            )
            product_image = FitImage(
                source=product.get('image_url', ''),
                size_hint=(None, None),
                size=(dp(90), dp(90)),
                radius=[dp(10)] * 4,
                pos_hint={"center_x": 0.5}
            )
            # Name and price container
            name_price_box = BoxLayout(
                orientation='vertical',
                spacing=dp(2),
                size_hint_y=None,
                height=dp(60)
            )
            # Truncate product name if it's too long
            product_name_text = product.get('name', 'No Name')
            max_name_length = 20  # Maximum characters before truncation
            if len(product_name_text) > max_name_length:
                product_name_text = product_name_text[:max_name_length] + "..."

            product_name = MDLabel(
                text=product_name_text,
                halign='center',
                size_hint_y=None,
                height=dp(40),
                theme_text_color='Primary',
                font_style='Subtitle1',
                text_size=(dp(70), None),
    
                shorten=False,
                valign='middle'
            )

            # Adjust price based on discount offer
            original_price = float(product.get('price', 0))
            offer = product.get('offer', 0)

            product_price = MDLabel(
                text=f"{original_price:.2f} JOD",
                halign='center',
                size_hint_y=None,
                height=dp(20),
                theme_text_color='Primary',
                font_style='Subtitle1',
                bold=True

                )

            discount_label_text = f"{offer}% off" if offer else ""
            discount_label = MDLabel(
                text=discount_label_text,
                halign='center',
                size_hint_y=None,
                height=dp(20),
                theme_text_color='Error'
            )

            add_to_cart_button = MDFillRoundFlatIconButton(
                text='Add to Cart',
                icon='cart',
                size_hint=(None, None),
                width=dp(140),
                pos_hint={"center_x": 0.5},
                on_release=partial(self.add_to_cart, product)
            )

            # Add widgets to name_price_box
            name_price_box.add_widget(product_name)
            name_price_box.add_widget(product_price)

            # Add widgets to the main box
            box.add_widget(product_image)
            box.add_widget(name_price_box)
            box.add_widget(discount_label)
            box.add_widget(add_to_cart_button)
            product_card.add_widget(box)

            self.ids.random_product_grid.add_widget(product_card)

    def load_products(self):
        self.current_page = 0
        self.product_data_list = []
        self.ids.random_product_grid.clear_widgets()
        self.ids.random_product_grid.add_widget(self.loading_spinner)
        Thread(target=self.load_products_from_firestore).start()

    def load_products_from_firestore(self):
        products_ref = db.collection('products')
        all_products = products_ref.get()
        self.total_products = len(all_products)
        self.total_pages = (self.total_products + self.page_size - 1) // self.page_size
        self.current_page = 0
        self.load_page(self.current_page)

    def load_page(self, page):
        if self.is_loading or page >= self.total_pages:
            return
        self.is_loading = True
        start_index = page * self.page_size
        
        products_ref = db.collection('products').offset(start_index).limit(self.page_size)
        
        docs = products_ref.stream()
        
        new_product_data_list = [doc.to_dict() for doc in docs]
        self.add_product_cards(new_product_data_list)
        
        self.is_loading = False

    
    def on_scroll(self, *args):
        if self.is_scroll_at_bottom() and not self.is_loading:
            if self.current_page < self.total_pages - 1:
                self.current_page += 1
                self.load_page(self.current_page)
                # Do not manually set scroll_y here

    def is_scroll_at_bottom(self):
        scroll_view = self.ids.random_product_scroll
        return scroll_view.scroll_y <= 0.05  

    def prefetch_next_page(self):
        if not self.is_loading and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_page(self.current_page)


class ProductScreen(BaseScreen):
    
    has_loaded_products = False  # Flag to check if products have been loaded

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_size = 10
        self.current_page = 0
        self.total_pages = 0
        self.is_loading = False
        self.total_products = 0
        self.loading_spinner = MDSpinner(size_hint=(None, None), size=(dp(20), dp(20)), active=True)
        self.category_name = None
        self.product_data_list = []


    def on_enter(self, *args):
        # Load products or category products only if not already loaded
        if not self.has_loaded_products:
            if self.category_name:
                self.display_category_products(self.category_name)
            else:
                self.load_products()
            self.has_loaded_products = True


    def display_brand_products(self, brand_name):
        # Clear any existing product display
        product_box = self.ids.product_grid
        product_box.clear_widgets()
        print(f"Displaying products for brand: {brand_name}")

        # Fetch products associated with the selected brand from Firestore
        products_ref = db.collection('products').where('brand', '==', brand_name)
        try:
            products = products_ref.stream()
            print(f"Products query executed for brand: {brand_name}")
        except Exception as e:
            print(f"Error retrieving products for brand {brand_name}: {e}")
            return

        products_found = False
        for product in products:
            products_found = True
            product_data = product.to_dict()
            product_name = product_data.get('name', 'No Name')
            product_price = product_data.get('price', 'N/A')
            product_image_url = product_data.get('image_url', '')
            product_discount = product_data.get('offer', '0')

            # Create a card for each product
            item_box = MDCard(
                orientation='vertical',
                spacing=dp(9),
                size_hint=(None, None),
                size=(dp(170), dp(220)),  # Slightly increased width and height
                elevation=4,  # Maintain card effect
                padding=dp(8),
                md_bg_color=(1, 1, 1, 1),  # White background for card
            )

            product_image = FitImage(
                source=product_image_url,
                size_hint=(1, None),  # Image takes full width of the card
                height=dp(70),  # Slightly increased image height
                pos_hint={"center_x": 0.5},
                radius=[dp(10)] * 4,
                keep_ratio=True,  # Maintain aspect ratio
                allow_stretch=True  # Allow stretching to fit the size
            )

            product_name_label = MDLabel(
                text=product_name,
                halign='center',
                theme_text_color='Primary',
                bold=True,
                font_style='Body1',
                size_hint_y=None,
                height=dp(35),  # Slightly increased height for text
                text_size=(dp(140), None),  # Allow wrapping within the card
                shorten=True,
                max_lines=2,  # Limit to two lines
            )

            product_price_label = MDLabel(
                text=f"{product_price} JOD",
                halign='center',
                theme_text_color='Secondary'
            )

            discount_label_text = f"{product_discount}% off" if product_discount else ""
            discount_label = MDLabel(
                text=discount_label_text,
                halign='center',
                size_hint_y=None,
                height=dp(20),  # Slightly increased height for label
                theme_text_color='Error'
            )

            # Add the widgets to the card
            item_box.add_widget(product_image)
            item_box.add_widget(product_name_label)
            item_box.add_widget(product_price_label)
            item_box.add_widget(discount_label)
            product_box.add_widget(item_box)

        
        if not products_found:
            print(f"No products found for brand: {brand_name}")


    def load_products(self):
        self.category_name = None
        self.current_page = 0
        self.product_data_list = []
        self.ids.product_grid.clear_widgets()
        self.ids.product_grid.add_widget(self.loading_spinner)
        Thread(target=self.load_products_from_firestore).start()

    def load_products_from_firestore(self):
        products_ref = db.collection('products')
        all_products = products_ref.get()
        self.total_products = len(all_products)
        self.total_pages = (self.total_products + self.page_size - 1) // self.page_size
        self.current_page = 0
        self.load_page(self.current_page)

    def load_page(self, page):
        if self.is_loading or page >= self.total_pages:
            return
        self.is_loading = True
        start_index = page * self.page_size
        if self.category_name:
            products_ref = db.collection('products').where('category', '==', self.category_name).offset(start_index).limit(self.page_size)
        else:
            products_ref = db.collection('products').offset(start_index).limit(self.page_size)
        
        docs = products_ref.stream()
        
        new_product_data_list = [doc.to_dict() for doc in docs]
        self.add_product_cards(new_product_data_list)
        
        self.is_loading = False

    cart_items = ListProperty([])

    


    def on_scroll(self, *args):
        if self.is_scroll_at_bottom() and not self.is_loading:
            if self.current_page < self.total_pages - 1:
                self.current_page += 1
                self.load_page(self.current_page)

    def is_scroll_at_bottom(self):
        scroll_view = self.ids.product_scroll
        return scroll_view.scroll_y <= 0.1 

    #def refresh_products(self):
        self.current_page = 0
        self.load_products()

    def prefetch_next_page(self):
        if not self.is_loading and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_page(self.current_page)

    def display_category_products(self, category_name):
        self.category_name = category_name
        self.current_page = 0
        self.product_data_list = []
        self.ids.product_grid.clear_widgets()
        self.ids.product_grid.add_widget(self.loading_spinner)
        Thread(target=self.load_category_products_from_firestore, args=(category_name,)).start()

    def load_category_products_from_firestore(self, category_name):
        products_ref = db.collection("products")
        query = products_ref.where("category", "==", category_name)
        docs = query.stream()

        product_data_list = [doc.to_dict() for doc in docs]
        self.total_products = len(product_data_list)
        self.total_pages = (self.total_products + self.page_size - 1) // self.page_size
        self.current_page = 0

        self.add_product_cards(product_data_list)


    
class CartScreen(Screen):
    def go_to_order_summary(self):
        order_summary_screen = self.manager.get_screen('order_summary_screen')
        print(self.manager.cart_items)  # Debug: Check what items are being passed
        order_summary_screen.populate_order_summary(self.manager.cart_items)
        self.manager.current = 'order_summary_screen'

class HomeScreen(Screen):
    pass

class More_Option(Screen):

    def open_mall_location(self):
        # URL to the mall location on Google Maps
        mall_location_url = "https://maps.app.goo.gl/RviP6i8M3pLJetC86"
        # Open the URL in the default web browser
        webbrowser.open(mall_location_url)

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history_stack = []
        self.cart_items = []  # Initialize an empty list to hold cart items

    def add_to_history(self, screen_name):
        if self.current not in self.history_stack:
            self.history_stack.append(self.current)

    def back_button(self):
        if len(self.history_stack) > 0:
            previous_screen = self.history_stack.pop()
            self.current = previous_screen

    cart_items = ListProperty([])

    

class SearchScreen(Screen):
    def on_text(self, text):
        app = MDApp.get_running_app()
        print(f"Text changed: {text}")  # Debug statement
        app.search_products(text)

class MyMainApp(MDApp):
    
    def build(self):
        self.scanner = BarcodeScanner()
        self.previous_screen = None
        self.window_manager = WindowManager()
        self.db = db
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.store = JsonStore('user_data.json')
        root_widget = Builder.load_file('my.kv')
        self.root = root_widget

        
        if self.store.exists('credentials'):
            token = self.store.get('credentials')['token']
            if self.validate_token(token):
                self.root.current = "app_screen"
            else:
                self.root.current = "login"
        else:
            self.root.current = "login"
        
        return self.root

    cart_items = ListProperty([])


    def on_start(self):
        # Schedule populate_brands to run after the UI has been initialized
        Clock.schedule_once(self.populate_brands, 0.1)

    def populate_brands(self, *args):
        app_screen = self.root.get_screen('app_screen')
        if app_screen is None:
            print("App screen not found!")
            return
        
        brand_box = app_screen.ids.get('brand_box')
        if brand_box is None:
            print("brand_box not found in AppScreen.")
            return

        brand_box.clear_widgets()
        print("brand_box cleared.")

        products_ref = db.collection('products')
        try:
            products = products_ref.stream()
            print("Firestore query executed.")
        except Exception as e:
            print(f"Error retrieving products: {e}")
            return

        brands_set = set()
        for product in products:
            product_data = product.to_dict()
            brand_name = product_data.get('brand')
            if brand_name:
                brands_set.add(brand_name)
        
        brands_list = list(brands_set)
        print(f"Unique brands found: {brands_list}")

        if not brands_list:
            print("No brands found in Firestore.")
            return

        for brand_name in brands_list:
            card = MDCard(
                size_hint=(None, None),
                size=(dp(150), dp(150)),
                elevation=10,
                radius=[dp(10), dp(10), dp(10), dp(10)],
                on_release=self.create_card_click_callback(brand_name)
            )

            card_label = MDLabel(
                text=brand_name,
                halign="center",
                valign="center"
            )

            card.add_widget(card_label)
            brand_box.add_widget(card)

    def create_card_click_callback(self, brand_name):
        def callback(instance):
            print(f"Brand card clicked: {brand_name}")
            product_screen = self.root.get_screen('product_screen')
            if product_screen:
                product_screen.display_brand_products(brand_name)
            else:
                print("Product screen not found!")
            self.root.current = 'product_screen'  # Navigate to ProductScreen
        return callback


    '''def on_card_click(self, brand_name):
        self.selected_brand = brand_name
        print(f"Brand selected: {brand_name}")
        self.go_to_screen("product_screen")
        self.root.get_screen("product_screen").display_brand_products(brand_name)'''

    def add_to_cart(self, product):
        self.cart_items.append(product)

    
    def start_camera(self):
        self.scanner.start_camera()
    def logout(self):
        # Sign out from Firebase
        self.firebase_logout()

        # Navigate back to the login screen
        self.go_to_screen("login")

    def firebase_logout(self):
        try:
            # Assuming you're using Firebase's Admin SDK for logout
            # This will clear the session on the client-side
            auth.revoke_refresh_tokens(self.get_user_id())
            print("User logged out successfully")
        except Exception as e:
            print(f"Error logging out: {e}")

    def get_user_id(self):
        # Example method to retrieve the current user's ID
        # You might need to adjust this based on how you store user data
        return auth.get_user().uid  # Example, adjust to your setup

    
    
    def validate_token(self, token):
        try:
            decoded_token = auth.verify_id_token(token)
            return True
        except:
            return False
        
    def go_to_screen(self, screen_name):
        screen_manager = self.root
        if screen_manager.current != screen_name:
            screen_manager.add_to_history(screen_manager.current)
            screen_manager.current = screen_name

    def back_button(self):
        screen_manager = self.root
        screen_manager.back_button()

    def search_products(self, search_text):
        # Remove leading and trailing spaces from the search text
        search_text = search_text.strip()

        # Clear the product list if the search text is empty
        if not search_text:
            self.update_product_list([])
            return

        # Convert the search text to uppercase for querying
        search_text_upper = search_text.upper()

        # Query products where 'name' contains the search text
        products_ref = db.collection('products')
        query = products_ref.stream()

        products = []
        for doc in query:
            product_data = doc.to_dict()
            
            # Convert the name from Firestore to uppercase for comparison
            product_name_upper = product_data['name'].upper()
            
            # Check if the product name contains the search text
            if search_text_upper in product_name_upper:
                # Convert the name from Firestore to lowercase for display
                product_data['name'] = product_data['name'].lower()
                products.append(product_data)

        # Update the product list with the filtered results
        self.update_product_list(products)
    
    def update_product_list(self, products):
        search_screen = self.root.get_screen('search_screen')
        product_list = search_screen.ids.product_list

        product_list.clear_widgets()

        for product in products:
            # Create a new product_card that references the current product data
            card = MDCard(
                orientation='vertical',
                size_hint=(1, None),
                height=dp(100),
                padding=dp(10),
                spacing=dp(10),
                pos_hint={"center_x": 0.5}
            )

            card_layout = BoxLayout(orientation='horizontal', spacing=dp(10))

            image_size = dp(80)
            image_source = product['image_url']
            try:
                product_image = FitImage(
                    source=image_source,
                    size_hint=(None, None),
                    size=(image_size, image_size),
                    allow_stretch=True,
                    keep_ratio=True
                )
            except Exception as e:
                fallback_image_url = 'https://via.placeholder.com/80'
                product_image = KivyImage(
                    source=fallback_image_url,
                    radius=[dp(10)] * 4,
                    size_hint=(None, None),
                    size=(image_size, image_size),
                    allow_stretch=True,
                    keep_ratio=True
                )

            card_layout.add_widget(product_image)

            text_layout = BoxLayout(orientation='vertical', spacing=dp(5))
            text_layout.add_widget(MDLabel(
                text=product['name'],
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(20)
            ))

            text_layout.add_widget(MDLabel(
                text=f"${product['price']:.2f}",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(20)
            ))

            card_layout.add_widget(text_layout)
            card.add_widget(card_layout)

            # Correct lambda function to pass product data to show_product_details
            card.bind(on_release=lambda instance, product=product: self.root.get_screen('product_details_screen').show_product_details(product))

            product_list.add_widget(card)

    def on_card_click(self, category_name):
        self.selected_category = category_name
        self.go_to_screen("product_screen")
        self.root.get_screen("product_screen").display_category_products(category_name)

if __name__ == "__main__":
    Window.size = (360, 640)

    MyMainApp().run()