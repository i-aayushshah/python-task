from django.contrib import admin
from django.utils.html import format_html
from .models import Company, CompanyNews, CompanyFinancial, CompanyAchievement


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'sector', 'market_price', 'company_type', 'created_at']
    list_filter = ['sector', 'company_type', 'created_at']
    search_fields = ['name', 'symbol', 'headquarters']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'symbol', 'sector', 'founded_year', 'company_type')
        }),
        ('Location & Contact', {
            'fields': ('headquarters', 'website', 'email', 'phone')
        }),
        ('Business Details', {
            'fields': ('description', 'employees', 'parent_group', 'industry_position')
        }),
        ('Financial Information', {
            'fields': ('market_price', 'market_cap', 'pe_ratio', 'dividend_yield',
                      'listed_shares', 'paid_up_capital', 'book_value')
        }),
        ('Media', {
            'fields': ('logo',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CompanyNews)
class CompanyNewsAdmin(admin.ModelAdmin):
    list_display = ['news_title', 'company', 'news_date', 'is_featured', 'is_published', 'created_at']
    list_filter = ['company', 'is_featured', 'is_published', 'category', 'news_date', 'created_at']
    search_fields = ['news_title', 'news_body', 'summary']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'news_date'

    fieldsets = (
        ('News Information', {
            'fields': ('company', 'news_title', 'news_date', 'category')
        }),
        ('Content', {
            'fields': ('summary', 'news_body', 'news_image')
        }),
        ('Publishing Options', {
            'fields': ('is_featured', 'is_published', 'slug')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def news_image_preview(self, obj):
        if obj.news_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.news_image.url)
        return "No Image"
    news_image_preview.short_description = "Image Preview"


@admin.register(CompanyFinancial)
class CompanyFinancialAdmin(admin.ModelAdmin):
    list_display = ['company', 'report_period', 'total_revenue', 'net_income', 'earnings_per_share', 'report_date']
    list_filter = ['company', 'report_period', 'report_date']
    search_fields = ['company__name', 'report_period']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'report_date'

    fieldsets = (
        ('Financial Period', {
            'fields': ('company', 'report_period', 'report_date')
        }),
        ('Financial Metrics', {
            'fields': ('total_revenue', 'net_income', 'earnings_per_share', 'total_assets', 'total_liabilities', 'shareholders_equity')
        }),
        ('Report File', {
            'fields': ('report_file',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CompanyAchievement)
class CompanyAchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'category', 'achievement_date', 'created_at']
    list_filter = ['company', 'category', 'achievement_date']
    search_fields = ['title', 'description', 'company__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'achievement_date'

    fieldsets = (
        ('Achievement Information', {
            'fields': ('company', 'title', 'category', 'achievement_date')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
