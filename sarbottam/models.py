from django.db import models
from django.utils import timezone
from django.urls import reverse


class Company(models.Model):
    # Basic Company Information
    name = models.CharField(max_length=200, default="Sarbottam Cement Limited")
    symbol = models.CharField(max_length=10, default="SARBTM")
    sector = models.CharField(max_length=100, default="Manufacturing and Processing")

    # Company Details
    founded_year = models.IntegerField(null=True, blank=True)
    headquarters = models.CharField(max_length=200, default="Sunwal, Nawalparasi, State-5, Nepal")
    company_type = models.CharField(max_length=50, default="Public Company")
    employees = models.CharField(max_length=50, default="501-1,000 employees")

    # Business Description
    description = models.TextField()

    # Contact Information
    website = models.URLField(default="https://saurabhgroup.com/sarbottam-cement")
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    # Financial Information (based on stock market data)
    market_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    market_cap = models.CharField(max_length=50, null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    book_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    roe = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Business Metrics
    production_capacity = models.CharField(max_length=100, null=True, blank=True)
    annual_revenue = models.CharField(max_length=100, null=True, blank=True)
    net_profit = models.CharField(max_length=100, null=True, blank=True)
    total_assets = models.CharField(max_length=100, null=True, blank=True)



    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class CompanyNews(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='news')
    news_title = models.CharField(max_length=300)
    news_date = models.DateTimeField(default=timezone.now)
    news_image = models.CharField(max_length=100, blank=True, null=True)  # Changed from ImageField
    news_body = models.TextField()
    summary = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    # Additional fields for better news management
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    slug = models.CharField(max_length=100, unique=True, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.news_title} - {self.news_date.strftime('%Y-%m-%d')}"

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Company News"
        verbose_name_plural = "Company News"
        ordering = ['-news_date']


class CompanyFinancial(models.Model):
    """Model to store quarterly/annual financial data"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='financials')

    # Financial Period
    report_period = models.CharField(max_length=20)

    # Financial Metrics
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    earnings_per_share = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    shareholders_equity = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # Date and File
    report_date = models.DateField()
    report_file = models.CharField(max_length=100, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.report_period}"

    class Meta:
        verbose_name = "Financial Data"
        verbose_name_plural = "Financial Data"
        ordering = ['-report_date']


class CompanyAchievement(models.Model):
    """Model to store company achievements and milestones"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='achievements')

    title = models.CharField(max_length=200)
    description = models.TextField()
    achievement_date = models.DateField()
    category = models.CharField(max_length=100, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.achievement_date}"

    class Meta:
        verbose_name = "Company Achievement"
        verbose_name_plural = "Company Achievements"
        ordering = ['-achievement_date']


class PriceHistory(models.Model):
    """Model to store daily stock price history"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='price_history')

    # Price data fields
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)  # LTP (Last Trade Price)

    # Additional trading data
    percentage_change = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)  # Quantity traded
    turnover = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.symbol} - {self.date} - NPR {self.close_price}"

    def get_change_class(self):
        """Return CSS class based on price change"""
        if self.percentage_change > 0:
            return 'text-green-600'
        elif self.percentage_change < 0:
            return 'text-red-600'
        return 'text-gray-600'

    def get_formatted_change(self):
        """Return formatted percentage change with sign"""
        if self.percentage_change:
            sign = '+' if self.percentage_change > 0 else ''
            return f"{sign}{self.percentage_change}%"
        return "0.00%"

    class Meta:
        verbose_name = "Price History"
        verbose_name_plural = "Price History"
        ordering = ['-date']
        unique_together = ('company', 'date')  # Ensure one record per company per date
