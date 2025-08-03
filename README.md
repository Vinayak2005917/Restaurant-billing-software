# 🍽️ Restaurant Billing Software

A comprehensive restaurant management system built with Streamlit, designed to handle orders, billing, and sales reporting for restaurants.

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
- **Dine-in Orders**: Table-based ordering system
- **Take-away Orders**: Quick service orders
- **Real-time Cart**: Live cart updates with item quantities
- **Menu Search**: Search items by name or description
- **Order Checkout**: Complete order processing with bill generation

### 💳 **Billing System**
- **Automatic Bill Generation**: Creates detailed receipts
- **Order Numbering**: Unique order IDs (ORD12345 format)
- **Price Calculation**: Automatic totals with item breakdown
- **Sales Tracking**: All orders saved to CSV for reporting

### 📊 **Reports & Analytics**
- **Sales Dashboard**: Total orders, revenue, and items sold
- **Order History**: Complete transaction records
- **Analytics Charts**: Order type distribution and revenue analysis
- **Data Export**: CSV format for external analysis

### 🎨 **User Interface**
- **Clean Design**: Modern, intuitive interface
- **Responsive Layout**: Works on different screen sizes
- **Staff Information**: Display staff details in sidebar
- **Easy Navigation**: Consistent sidebar navigation across pages

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vinayak2005917/Restaurant-billing-software.git
   cd Restaurant-billing-software
   ```

2. **Install dependencies**
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
cd ui
streamlit run main_ui.py
```

The application will open in your default web browser at `http://localhost:8501`

### Basic Workflow

1. **Select Order Type**: Choose between Dine-in or Take-away
2. **Enter Details**: For dine-in, enter table number
3. **Browse Menu**: Search and select items
4. **Add to Cart**: Use +/- buttons to adjust quantities
5. **Review Order**: Check cart in sidebar
6. **Checkout**: Complete the order and generate bill
7. **View Reports**: Access sales data and analytics

### Navigation
- **Main Menu**: Order selection (Dine-in/Take-away)
- **Order Pages**: Menu browsing and cart management
- **Reports**: Sales analytics and order history
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
│   ├── main_ui.py              # Main application entry point
│   └── pages/
│       ├── dine_in.py          # Dine-in ordering interface
│       ├── take_away.py        # Take-away ordering interface
│       └── reports.py          # Sales reports and analytics
└── utils/
    └── keyboard.py             # Utility functions
```

## ⚙️ Configuration

### Menu Configuration
Edit `data/menu.csv` to customize your menu:
- `item_id`: Unique identifier
- `item_name`: Display name
- `stock`: Available quantity
- `short_description`: Item description
- `price`: Item price (optional, defaults to ₹100)


## 📸 Screenshots

### Main Menu
- Clean interface with Dine-in and Take-away options
- Staff information sidebar
- Navigation controls

### Order Interface
- Menu display with search functionality
- Real-time cart updates
- Item quantity controls
- Checkout process

### Reports Dashboard
- Sales summary metrics
- Complete order history
- Analytics charts
- Data visualization

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Python**: Core programming language
- **CSV**: Data storage format

### Key Components
- **Session State Management**: Maintains cart data across interactions
- **File Path Handling**: Cross-platform compatibility
- **Error Handling**: Graceful error management
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
