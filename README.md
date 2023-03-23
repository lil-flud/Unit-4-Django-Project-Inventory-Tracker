# Unit-4-Django-Project-Inventory-Tracker

_Roles_
[] website viewable by everyone without an account
[] authenticated users are able to change inventory and edit
_authenticated_users_
[] add, update quantity, delete tires
[] search for tires
[] view tire details for one tire

_unauthenticated_users_
[] search for tires
[] view tire details for one tire

_Models, Forms and Relational Databases_
[] individual users are salespeople, when quantity is updated, the receipt will be created for future purposes
[] receipts cannot be deleted by anyone but superuser

**Models**
[] User -- Django User
[] Invoice -- Date of sale, list of items sold, user that sold items, price of all items, total price
[] Outvoice -- date of sale, list of items bought, user that bought items, price of all items, total price, expected arrival
[] Tire -- brand, line, size, mileage_rating, base_price, tread_pattern, condition, adjusted price, quantity

**Forms**
[] AddTireForm(ModelForm) - Model = Tire
[] UserCreationForm(ModelForm) Model = User
[] UserLoginForm(Form)

**Views**
_views with all permissions_
[] HomePage - view list of all tires, search function can be used
**If user unauthenticated, editing of tire quantity is not allowed
[] TireDetails - view details of one particular tire
** If user unauthenticated, editing of tire quantity is not allowed
[] Register - UserCreationForm, role automatically is normal, fields = username, email, password1, password2
[] Login - UserLoginForm

_authenticated users_
[] AddTire - AddTireForm
[] Tire_Info - extra permission to click "buy" or "sell"
[] HomePage - extra permission to click "buy" or "sell"
[] BuyTires - buy tires, generates OutVoice Model
[] SellTires, sell tires, generates Invoice Model
[] View Invoices - view invoices
[] View OutVoices - view OutVoices
[] DeleteTire
