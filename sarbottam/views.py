from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Company, CompanyNews, CompanyFinancial, CompanyAchievement, PriceHistory
from .ml_services import StockPricePredictor


def company_profile(request):
    """Main company profile view"""
    try:
        company = Company.objects.first()  # Get the first company (Sarbottam Cement)
        if not company:
            # Create default company if none exists
            company = Company.objects.create()

        # Get latest news (featured and recent) - Fixed for MySQL compatibility
        featured_news = CompanyNews.objects.filter(
            company=company,
            is_featured=True,
            is_published=True
        ).order_by('-news_date')[:3]

        recent_news = CompanyNews.objects.filter(
            company=company,
            is_published=True
        ).order_by('-news_date')[:6]

        # Get latest financial data - Fixed for MySQL compatibility
        latest_financial = CompanyFinancial.objects.filter(
            company=company
        ).order_by('-report_date').first()

        # Get recent achievements - Fixed for MySQL compatibility
        recent_achievements = CompanyAchievement.objects.filter(
            company=company
        ).order_by('-achievement_date')[:4]

        context = {
            'company': company,
            'featured_news': featured_news,
            'recent_news': recent_news,
            'latest_financial': latest_financial,
            'recent_achievements': recent_achievements,
        }

        return render(request, 'sarbottam/company_profile.html', context)

    except Exception as e:
        return render(request, 'sarbottam/error.html', {'error': str(e)})


def news_list(request):
    """News listing view with search and pagination"""
    try:
        company = Company.objects.first()
        if not company:
            company = Company.objects.create()

        # Get search query
        search_query = request.GET.get('search', '')

        # Filter news - Fixed for MySQL compatibility
        news_queryset = CompanyNews.objects.filter(
            company=company,
            is_published=True
        )

        if search_query:
            news_queryset = news_queryset.filter(
                Q(news_title__icontains=search_query) |
                Q(news_body__icontains=search_query) |
                Q(summary__icontains=search_query)
            )

        news_queryset = news_queryset.order_by('-news_date')

        # Pagination
        paginator = Paginator(news_queryset, 9)  # 9 news per page
        page_number = request.GET.get('page')
        news = paginator.get_page(page_number)

        context = {
            'company': company,
            'news': news,
            'search_query': search_query,
        }

        return render(request, 'sarbottam/news_list.html', context)

    except Exception as e:
        return render(request, 'sarbottam/error.html', {'error': str(e)})


def news_detail(request, slug):
    """Individual news article view"""
    try:
        company = Company.objects.first()
        if not company:
            company = Company.objects.create()

        news = get_object_or_404(CompanyNews, slug=slug, company=company, is_published=True)

        # Get related news - Fixed for MySQL compatibility
        related_news = CompanyNews.objects.filter(
            company=company,
            is_published=True
        ).exclude(id=news.id).order_by('-news_date')[:3]

        context = {
            'company': company,
            'news': news,
            'related_news': related_news,
        }

        return render(request, 'sarbottam/news_detail.html', context)

    except Exception as e:
        return render(request, 'sarbottam/error.html', {'error': str(e)})


def financial_data(request):
    """Financial information view"""
    try:
        company = Company.objects.first()
        if not company:
            company = Company.objects.create()

        # Get financial data - Fixed for MySQL compatibility
        financial_data = CompanyFinancial.objects.filter(
            company=company
        ).order_by('-report_date')

        context = {
            'company': company,
            'financial_data': financial_data,
        }

        return render(request, 'sarbottam/financial_data.html', context)

    except Exception as e:
        return render(request, 'sarbottam/error.html', {'error': str(e)})


def achievements(request):
    """Company achievements view"""
    try:
        company = Company.objects.first()
        if not company:
            company = Company.objects.create()

        # Get achievements - Fixed for MySQL compatibility
        achievements = CompanyAchievement.objects.filter(
            company=company
        ).order_by('-achievement_date')

        context = {
            'company': company,
            'achievements': achievements,
        }

        return render(request, 'sarbottam/achievements.html', context)

    except Exception as e:
        return render(request, 'sarbottam/error.html', {'error': str(e)})


def api_company_data(request):
    """API endpoint for company data"""
    try:
        company = Company.objects.first()
        if not company:
            return JsonResponse({'error': 'Company not found'}, status=404)

        data = {
            'name': company.name,
            'symbol': company.symbol,
            'sector': company.sector,
            'market_price': str(company.market_price),
            'market_cap': company.market_cap,
            'headquarters': company.headquarters,
            'website': company.website,
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def price_history(request):
    """Price history view"""
    try:
        company = Company.objects.first()
        if not company:
            company = Company.objects.create()

        # Get price history data - Fixed for MySQL compatibility
        price_data = PriceHistory.objects.filter(
            company=company
        ).order_by('-date')[:30]  # Last 30 days

        # Get latest price for current info
        latest_price = price_data.first() if price_data else None

        context = {
            'company': company,
            'price_data': price_data,
            'latest_price': latest_price,
        }

        return render(request, 'sarbottam/price_history.html', context)

    except Exception as e:
        return render(request, 'sarbottam/error.html', {'error': str(e)})


def api_latest_news(request):
    """API endpoint for latest news"""
    try:
        company = Company.objects.first()
        if not company:
            return JsonResponse({'error': 'Company not found'}, status=404)

        # Get latest news - Fixed for MySQL compatibility
        latest_news = CompanyNews.objects.filter(
            company=company,
            is_published=True
        ).order_by('-news_date')[:5]

        news_data = []
        for news in latest_news:
            news_data.append({
                'title': news.news_title,
                'date': news.news_date.strftime('%Y-%m-%d'),
                'summary': news.summary,
                'slug': news.slug,
                'category': news.category,
            })

        return JsonResponse({'news': news_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def api_price_history(request):
    """API endpoint for price history data"""
    try:
        company = Company.objects.first()
        if not company:
            return JsonResponse({'error': 'Company not found'}, status=404)

        # Get latest price history
        price_data = PriceHistory.objects.filter(
            company=company
        ).order_by('-date')[:20]

        price_list = []
        for price in price_data:
            price_list.append({
                'date': price.date.strftime('%Y-%m-%d'),
                'open': str(price.open_price),
                'high': str(price.high_price),
                'low': str(price.low_price),
                'close': str(price.close_price),
                'change': str(price.percentage_change) if price.percentage_change else '0.00',
                'volume': price.volume,
                'turnover': str(price.turnover) if price.turnover else '0.00',
            })

        return JsonResponse({'price_history': price_list})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def price_predictions(request):
    """Price predictions view"""
    try:
        company = Company.objects.first()
        if not company:
            company = Company.objects.create()

        # Get prediction data
        predictor = StockPricePredictor()
        predictions = predictor.predict_next_days(days=5, company_symbol=company.symbol)

        # Calculate changes for template
        if predictions['success'] and predictions.get('predictions'):
            for i, pred in enumerate(predictions['predictions']):
                if i == 0:
                    # First prediction vs current price
                    change = pred['predicted_price'] - predictions['last_actual_price']
                    pred['change'] = change
                    pred['change_percent'] = (change / predictions['last_actual_price']) * 100
                else:
                    # Subsequent predictions vs previous prediction
                    prev_price = predictions['predictions'][i-1]['predicted_price']
                    change = pred['predicted_price'] - prev_price
                    pred['change'] = change
                    pred['change_percent'] = (change / prev_price) * 100

            # Calculate total 5-day change for the last prediction
            if len(predictions['predictions']) > 0:
                last_pred = predictions['predictions'][-1]
                total_change = last_pred['predicted_price'] - predictions['last_actual_price']
                total_change_percent = (total_change / predictions['last_actual_price']) * 100
                last_pred['total_change'] = total_change
                last_pred['total_change_percent'] = total_change_percent

        # Get latest price data for context
        latest_prices = PriceHistory.objects.filter(
            company=company
        ).order_by('-date')[:10]

        context = {
            'company': company,
            'predictions': predictions,
            'latest_prices': latest_prices,
        }

        return render(request, 'sarbottam/price_predictions.html', context)

    except Exception as e:
        return render(request, 'sarbottam/error.html', {'error': str(e)})


def api_price_predictions(request):
    """API endpoint for price predictions"""
    try:
        company = Company.objects.first()
        if not company:
            return JsonResponse({'error': 'Company not found'}, status=404)

                # Get prediction data
        predictor = StockPricePredictor()
        days = int(request.GET.get('days', 5))
        predictions = predictor.predict_next_days(days=days, company_symbol=company.symbol)

        # Calculate changes for API
        if predictions['success'] and predictions.get('predictions'):
            for i, pred in enumerate(predictions['predictions']):
                if i == 0:
                    # First prediction vs current price
                    change = pred['predicted_price'] - predictions['last_actual_price']
                    pred['change'] = change
                    pred['change_percent'] = (change / predictions['last_actual_price']) * 100
                else:
                    # Subsequent predictions vs previous prediction
                    prev_price = predictions['predictions'][i-1]['predicted_price']
                    change = pred['predicted_price'] - prev_price
                    pred['change'] = change
                    pred['change_percent'] = (change / prev_price) * 100

            # Calculate total change for the last prediction
            if len(predictions['predictions']) > 0:
                last_pred = predictions['predictions'][-1]
                total_change = last_pred['predicted_price'] - predictions['last_actual_price']
                total_change_percent = (total_change / predictions['last_actual_price']) * 100
                last_pred['total_change'] = total_change
                last_pred['total_change_percent'] = total_change_percent

        # Convert date objects to strings for JSON serialization
        if predictions['success']:
            for pred in predictions['predictions']:
                pred['date'] = pred['date'].strftime('%Y-%m-%d')

        return JsonResponse(predictions)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
