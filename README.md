
# Restaurant Billing Software

This is a modern Streamlit-based restaurant billing system with role-based authentication, intuitive ordering (Dine-in & Take-away), live stock control, payments with GST, PDF receipts, and sales reports. Includes an Admin panel for stock and cashier management.

**Now fully database-powered:** All data (menu, sales, cashiers, stock) is stored in a robust SQLite database (`db/restaurant.db`). No CSV files required for normal operation.

**Quick Start:**
- Just run `app.py` to launch the entire application:
  ```powershell
  streamlit run app.py
  ```
- The app is also deployed at [https://vinayak2005917-restaurant-billing-software-uilogin-snyxds.streamlit.app/](https://vinayak2005917-restaurant-billing-software-uilogin-snyxds.streamlit.app/) for instant access.

## 📋 Table of Contents
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Model & Storage](#data-model--storage)
- [User Workflows](#user-workflows)
- [Development Notes](#development-notes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🔐 Authentication & Role Management
- Admin shortcut: `admin/admin`
- Cashier login: validated against `data/cashier_list.csv` (columns: `username, full_name, password`)
- Roles: Admin → Admin Panel; Cashier → New Order & Reports
- Optional Quick Access buttons for development
- Session state persists auth across pages

### 🛒 Order Management
- Dine-in: keypad for table numbers with validation
- Take-away: streamlined flow
- Live cart: +/- quantity, totals, clear cart
- Search: by name/description
- Live stock display and caps while ordering

### 💳 Payment & Billing
- Methods: UPI, Cash, Card
- GST: 5% calculation
- Order summary & confirmation
- PDF receipt via FPDF2
- Unique order numbers (ORD#####)
- Sales persisted to `data/sales_report.csv`

### 📊 Reports & Analytics
- KPIs: total orders, revenue, items sold, AOV
- Order history table
- Charts for order/revenue distribution
- Real-time from `sales_report.csv`

### 🔧 Admin Panel
- Manage Stock (per-item +/- with Save button; search items)
- Cashiers (add/remove persisted to `data/cashier_list.csv`)
- File upload & preview (CSV/Excel/JSON/TXT)
- Quick stats

### 🎨 User Interface
- Wide layout, clean styling with custom CSS
- Hidden default menu/sidebar where appropriate
- Focused payment page

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Login Page    │ -> │  Role Routing   │ -> │ Admin / Cashier │
│  (ui/login.py)  │    │                 │    │     Pages       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         v                       v                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  New Order      │ -> │ Dine-in / Take  │ -> │   Payment &     │
│ (new order.py)  │    │    Away Pages   │    │ PDF Receipt     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                v                       v
                     ┌─────────────────┐    ┌─────────────────┐
                     │  Cart Management│    │  Sales Reports  │
                     │ (Session State) │    │ (reports.py)    │
                     └─────────────────┘    └─────────────────┘
```

**Core Technologies:**
- **Frontend**: Streamlit with custom CSS
- **Data Processing**: Pandas for CSV operations
- **PDF Generation**: FPDF2 for receipt creation
- **Session Management**: Streamlit session state
- **File Storage**: CSV files for data persistence
- **Order Numbering**: Unique order IDs (ORD12345 format)
- **Price Calculation**: Automatic totals with item breakdown
- **Sales Tracking**: All orders saved to CSV for reporting
- **Payment Workflow**: Three payment modes (UPI, Cash, Card) with confirmation for each
- **Sales Dashboard**: Total orders, revenue, and items sold
- **Order History**: Complete transaction records
- **Clean Design**: Modern, intuitive interface
- **Responsive Layout**: Works on different screen sizes

### Prerequisites
- Python 3.10+
- pip

### Setup
```powershell
git clone https://github.com/Vinayak2005917/Restaurant-billing-software.git
cd "Restaurant-billing-software"
pip install -r requirements.txt
```

Create `data/` if missing and add menu data:
```csv
item_id,item_name,stock,short_description,price
1,Margherita Pizza,20,Classic cheese and tomato pizza,299
2,Paneer Tikka,15,Grilled cottage cheese with spices,249
```
Optional: seed `data/cashier_list.csv` with:
```csv
username,full_name,password
cashier01,Aarav Sharma,Pass@123
```

## 🖥️ Usage

### Start the app
```powershell
streamlit run app.py
```
The app opens at http://localhost:8501 or visit [xyz.com](https://xyz.com) for the live deployment.

### Basic Workflow

1) **Login**
  - Admin: `admin/admin` → Admin Panel
  - Cashier: any user from the database → New Order

2) **New Order**
  - Choose Dine-in or Take-away, add items with +/- (stock-limited)

3) **Payments**
  - Choose UPI/Cash/Card; confirm to persist sale and decrement stock in the database; download PDF

4) **Reports**
  - View KPIs and sales table

5) **Admin Settings**
  - Manage Stock: search items, adjust with +/- and save per item
  - Cashiers: add/remove users (username, full name, password)

## 📁 Project Structure

```
Restaurant-billing-software/
├── app.py
├── README.md
├── requirements.txt
├── data/
│   ├── menu.csv
│   ├── sales_report.csv
│   └── cashier_list.csv
├── db/
│   └── user_settings.json
├── ui/
│   ├── login.py
│   └── pages/
│       ├── admin.py
│       ├── admin_setting.py
│       ├── user_settings.py
│       ├── new order.py
│       ├── dine_in.py
│       ├── take_away.py
│       ├── payments.py
│       └── reports.py
└── utils/
  └── keyboard.py
```

## ⚙️ Configuration

### Data & Config
- All data is now stored in `db/restaurant.db` (SQLite):
  - `menu` table: item_id, item_name, stock, short_description, price
  - `sales` table: auto-generated sales records
  - `cashiers` table: username, full_name, password (plain text)
  - `user_settings` table: per-user settings (names, etc.)

Stock handling:
- Live stock display and caps on order pages
- Stock decremented on payment confirmation and saved in the database

## 🛠️ Technical Details

### Built With
- Streamlit, Pandas, FPDF2, Python 3.10+
- Session state, multi-page nav via `st.switch_page`
- SQLite database for all data persistence

Security note:
- Cashier passwords are stored in plain text for demo simplicity. Consider hashing for production.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add comments for complex logic
- Test new features thoroughly
- Update documentation for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
