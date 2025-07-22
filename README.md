# Sarbottam Cement Limited - Stock Analysis Platform

A Django-based web application that provides comprehensive company information and stock analysis for Sarbottam Cement Limited (SARBTM). The platform features real-time stock data scraping from NEPSE, AI-powered price predictions, and detailed company information.

## 🌟 Key Features

### Company Information
- Detailed company profile and history
- Financial performance metrics
- Corporate achievements and milestones
- Industry position and market analysis

### Stock Market Data
- Real-time price data from NEPSE
- Historical price trends with OHLC data
- Volume and turnover analysis
- Percentage change tracking

### AI-Powered Analysis
- 5-day price predictions using machine learning
- Multiple prediction models
- Technical indicators and trend analysis
- Confidence intervals for predictions

### News & Updates
- Latest company news and announcements
- Categorized news articles
- Searchable news archive
- Featured news highlights

## 🛠 Technology Stack

### Backend
- Python 3.13
- Django 4.2+
- MySQL Database
- Selenium WebDriver

### Data Science
- scikit-learn 1.7.1
- pandas 2.3.1
- numpy 2.3.1
- joblib 1.3.2

### Frontend
- HTML5
- Tailwind CSS (via CDN)
- JavaScript
- Responsive Design

## 📊 Data Models

### Company (`sarbottam_company`)
```python
- name: Company name (default: "Sarbottam Cement Limited")
- symbol: Stock symbol (default: "SARBTM")
- sector: Industry sector
- founded_year: Establishment date
- headquarters: Company location
- description: Detailed description
- market_cap: Market capitalization
- roe: Return on Equity
- production_capacity: Manufacturing capacity
- annual_revenue: Yearly revenue
- net_profit: Annual profit
- total_assets: Asset value
```

### News (`sarbottam_companynews`)
```python
- news_title: Article headline
- news_date: Publication date
- news_image: Article image URL
- news_body: Main content
- summary: Brief overview
- category: News category
- is_featured: Featured status
- slug: URL-friendly identifier
```

### Financial Data (`sarbottam_companyfinancial`)
```python
- report_period: Financial period
- total_revenue: Period revenue
- net_income: Net profit
- earnings_per_share: EPS
- total_assets: Asset value
- total_liabilities: Total liabilities
- shareholders_equity: Equity value
- report_date: Report date
- report_file: Financial document
```

### Price History (`sarbottam_pricehistory`)
```python
- date: Trading date
- open_price: Opening price
- high_price: Day's high
- low_price: Day's low
- close_price: Closing price
- percentage_change: Daily change
- volume: Trading volume
- turnover: Trading value
```

### Achievements (`sarbottam_companyachievement`)
```python
- title: Achievement title
- description: Detailed description
- achievement_date: Date achieved
- category: Achievement type
```

## 🤖 Machine Learning Pipeline

### Data Collection
- Automated scraping from NEPSE
- Selenium-based data extraction
- Pagination handling
- Daily updates

### Price Prediction
- **Models Used**:
  - Linear Regression
  - Random Forest
  - Simple Moving Average (fallback)
- **Features**:
  - Price trends
  - Moving averages
  - Volume indicators
  - Market sentiment
- **Output**: 5-day price forecasts with confidence intervals

## 🚀 Setup Instructions

### Prerequisites
- Python 3.13+
- MySQL Server
- Chrome WebDriver (for Selenium)
- Git

### Installation Steps

1. **Clone Repository**
```bash
git clone <repository-url>
cd "Python Taskk"
```

2. **Create Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
- Copy `secret.py.example` to `secret.py`
- Update database credentials
- Set Chrome WebDriver path

5. **Database Setup**
```bash
# Option 1: Using SQL Script
mysql -u root -p < database_setup.sql

# Option 2: Using Django Migrations
python manage.py migrate
```


6. **Run Development Server**
```bash
python manage.py runserver
```

## 📁 Project Structure
```
Python Taskk/
├── cement_profile_app/        # Django project
├── sarbottam/                # Main application
│   ├── models.py            # Data models
│   ├── views.py             # View logic
│   ├── ml_services.py       # ML components
│   └── management/
│       └── commands/        # Custom commands
├── templates/                # HTML templates
├── static/                   # Static assets
├── drivers/                  # WebDriver
└── requirements.txt         # Dependencies
```

## 🌐 API Endpoints

### Company Profile
```
GET /api/company/
Response: Company details
```

### News
```
GET /api/news/
Response: Latest news articles
```

### Price History
```
GET /api/price-history/
Response: Historical prices
```

### Price Predictions
```
GET /api/predictions/
Response: 5-day forecasts
```

## 🔧 Management Commands

### Data Collection
```bash
# Scrape price history
python manage.py scrape_price_history --limit 20

# Clear price data
python manage.py clear_price_data

# Generate predictions
python manage.py predict_prices
```

## 🔒 Security Features

- CSRF Protection
- SQL Injection Prevention
- Secure File Uploads
- Environment Variables
- Access Control

## 📈 Performance Optimization

- Database Indexing
- Query Optimization
- Caching Strategy
- Efficient Data Loading

## 🌍 Production Deployment

### Configuration
- Debug Mode: Disabled
- Static Files: CDN/Nginx
- Database: Production MySQL
- HTTPS: Enabled

### Monitoring
- Error Logging
- Performance Metrics
- Database Monitoring
- Scheduled Tasks

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Submit pull request

## 📞 Support

For issues or questions:
1. Check documentation
2. Create GitHub issue
3. Contact development team

---

**Note**: This application demonstrates modern Django development practices, integrating web scraping, machine learning, and financial data analysis. It serves as a comprehensive platform for analyzing Sarbottam Cement Limited's stock performance on the Nepal Stock Exchange (NEPSE).
