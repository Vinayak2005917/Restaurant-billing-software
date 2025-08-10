
# Restaurant Billing Software

A comprehensive Streamlit-based restaurant billing system with role-based authentication, intuitive ordering workflows, payment processing with GST calculation, PDF receipt generation, and detailed sales reporting. Built for restaurants needing both dine-in and take-away management with a professional admin panel.

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

### 🔐 **Authentication & Role Management**
- **Login System**: Role-based access with demo credentials (`admin/admin`, `cashier/cashier`)
- **Admin Role**: Access to admin panel, file uploads, system management
- **Cashier Role**: Access to order management and reports
- **Quick Access**: Bypass login buttons for demo/development purposes
- **Session Management**: Persistent login state across pages

### 🛒 **Order Management**
- **Dine-in Orders**: 
  - Custom numeric keypad for table number entry
  - Table number validation and display
  - Table-specific order tracking
- **Take-away Orders**: Streamlined ordering without table assignment
- **Live Shopping Cart**: 
  - Real-time quantity updates with +/- controls
  - Running totals and item counts
  - Clear cart and trash order functionality
- **Menu Search**: Filter items by name or description
- **Stock Display**: Show available inventory for each item

### 💳 **Payment & Billing System**
- **Payment Methods**: UPI (with QR code), Cash, and Card payments
- **GST Calculation**: Automatic 5% GST calculation and display
- **Order Summary**: Detailed breakdown before payment confirmation
- **PDF Receipt Generation**: Downloadable receipts using FPDF
- **Order Tracking**: Unique order numbers (ORD##### format)
- **Sales Persistence**: All orders saved to CSV for reporting

### 📊 **Reports & Analytics**
- **Sales Dashboard**: 
  - Total orders, revenue, and items sold
  - Average order value calculations
  - Order type distribution charts
- **Order History**: Complete transaction records with search/sort
- **Data Visualization**: Revenue by order type, order distribution
- **Real-time Updates**: Live data from sales_report.csv

### 🔧 **Admin Panel**
- **File Upload System**: Support for CSV, Excel, Text, and JSON files
- **Data Preview**: Preview uploaded files before saving
- **Auto-conversion**: Excel files automatically converted to CSV
- **File Management**: Save uploaded files to data directory
- **System Statistics**: Quick metrics dashboard

### 🎨 **User Interface**
- **Clean Design**: Modern, professional Streamlit interface
- **Responsive Layout**: Wide layout for optimal screen usage
- **Hidden Navigation**: Streamlined interface with hidden default menus
- **Context-Sensitive UI**: Payment page hides sidebar for focus
- **Custom Styling**: CSS customizations for better UX

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

### Setup Instructions
   ```bash
   git clone https://github.com/Vinayak2005917/Restaurant-billing-software.git
   cd Restaurant-billing-software
   ```
   ```bash
   pip install -r requirements.txt
   ```

3. **Create data directory** (if not exists)
   ```bash
   mkdir data
   ```

4. **Add menu data**
   - Create `data/menu.csv` with your menu items
   - Sample format:
     ```csv
     item_id,item_name,stock,short_description,price
     1,Margherita Pizza,20,Classic cheese and tomato pizza,299
     2,Paneer Tikka,15,Grilled cottage cheese with spices,249
     ```

## 🖥️ Usage

### Starting the Application
```bash
pip install -r requirements.txt
streamlit run app.py

Or, for development, run from the `ui` folder:
```bash
cd ui
```

The application will open in your default web browser at `http://localhost:8501`

### Basic Workflow

1. **Select Order Type**: Choose between Dine-in or Take-away
4. **Add to Cart**: Use +/- buttons to adjust quantities
5. **Review Order**: Check cart in sidebar
8. **Download PDF Receipt**: After payment, download your bill
9. **View Reports**: Access sales data and analytics
- **Order Pages**: `dine_in.py`, `take_away.py` — Menu browsing and cart management
- **Payments**: `payments.py` — Payment and PDF receipt
- **Reports**: `reports.py` — Sales analytics and order history
- **Sidebar**: Staff info and navigation controls

## 📁 Project Structure

```
Restaurant-billing-software/
├── README.md
├── requirements.txt
├── data/
│   ├── menu.csv                 # Menu items database
│   └── sales_report.csv         # Sales data (auto-generated)
├── ui/
│   ├── main_ui.py              # Main Streamlit UI (entry point for development)
│   └── pages/
│       ├── dine_in.py          # Dine-in ordering interface
│       ├── take_away.py        # Take-away ordering interface
│       ├── payments.py         # Payment and PDF receipt logic
│       └── reports.py          # Sales reports and analytics
└── utils/
    └── keyboard.py             # (empty placeholder for future utilities)
```

## ⚙️ Configuration

### Menu Configuration
- `price`: Item price (required)


- Menu display with search functionality
- Real-time cart updates
- Item quantity controls

- Payment mode selection (UPI, Cash, Card)
- PDF receipt download after payment
### Reports Dashboard
- Complete order history
- Analytics charts
- Data visualization

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework (UI, navigation, state)
- **Pandas**: Data manipulation and analysis (menu, sales, reporting)
- **FPDF**: PDF receipt generation (downloadable bills)
- **Python**: Core programming language
- **Session State Management**: Maintains cart, navigation, and order state across all pages
- **Dynamic Navigation**: Uses `st.switch_page` and session state for multi-page flow
- **PDF Generation**: Downloadable receipts after payment (with itemized split, total, payment method, order number)
- **Order Type Tracking**: Accurate Dine-in/Take-away reporting in all flows
- **Sales Reporting**: Real-time analytics and CSV export
- **UI/UX**: Custom CSS, sidebar logic, and responsive layout
- **Error Handling**: Graceful error management and user feedback
- **Data Validation**: Input sanitization and validation

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
