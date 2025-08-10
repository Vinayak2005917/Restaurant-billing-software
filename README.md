
# Restaurant Billing Software

A modern, user-friendly restaurant billing system built with Streamlit. Supports dine-in and take-away orders, robust cart and checkout logic, payment workflow, PDF receipt download, and sales reporting.

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🛒 **Order Management**
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
