from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from sarbottam.models import Company, CompanyNews, CompanyFinancial, CompanyAchievement


class Command(BaseCommand):
    help = 'Add sample data for Sarbottam Cement Limited'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding sample data for Sarbottam Cement Limited...'))

        # Create or update company profile
        company, created = Company.objects.get_or_create(
            symbol='SARBTM',
            defaults={
                'name': 'Sarbottam Cement Limited',
                'sector': 'Manufacturing and Processing',
                'founded_year': 2010,
                'headquarters': 'Sunwal, Nawalparasi, State-5, Nepal',
                'company_type': 'Public Company',
                'employees': '501-1,000 employees',
                'description': 'Sarbottam Cement Limited is an innovator and pioneer of the cement industry of Nepal, being the first and only cement manufacturer to use a completely European production line. The company operates with state-of-the-art technology and sustainable practices.',
                'website': 'https://sarbottamcement.com.np',
                'email': 'info@sarbottamcement.com.np',
                'phone': '+977-78-520012',
                'market_price': 265.00,
                'market_cap': '2.12B',
                'pe_ratio': 15.2,
                'dividend_yield': 3.5,
                'book_value': 180.0,
                'roe': 12.8,
                'production_capacity': '500,000 tonnes per year',
                'annual_revenue': '1.8 billion NPR',
                'net_profit': '180 million NPR',
                'total_assets': '2.5 billion NPR'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created company profile for {company.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Company profile already exists for {company.name}'))

        # Add sample news
        sample_news = [
            {
                'news_title': 'Sarbottam Cement Reports Strong Q3 Financial Results with 15% Revenue Growth',
                'news_date': timezone.now() - timedelta(days=5),
                'summary': 'Sarbottam Cement Limited announced exceptional third-quarter results, showing a 15% increase in revenue compared to the same period last year, driven by increased domestic demand and strategic market expansion.',
                'news_body': '''Sarbottam Cement Limited today announced its financial results for the third quarter ended December 2024, reporting a robust 15% year-over-year revenue growth to NPR 450 million. The company's strong performance was driven by increased domestic demand for construction materials and successful market penetration strategies.

Key Financial Highlights:
• Revenue increased to NPR 450 million (15% YoY growth)
• Net profit margin improved to 12.5%
• EBITDA grew by 18% to NPR 85 million
• Production volume reached 125,000 tonnes

Managing Director stated: "These results reflect our commitment to quality and innovation in the cement industry. Our European production line continues to deliver superior products that meet the highest international standards."

The company has maintained its position as Nepal's premium cement manufacturer, with its products being used in major infrastructure projects across the country. The management remains optimistic about continued growth in the upcoming quarters, supported by government infrastructure initiatives and private sector construction activities.

Sarbottam Cement's stock (SARBTM) has shown strong performance on NEPSE, reflecting investor confidence in the company's strategic direction and operational efficiency.''',
                'category': 'Financial Results',
                'is_featured': True,
                'is_published': True
            },
            {
                'news_title': 'Sarbottam Cement Launches Environmental Sustainability Initiative',
                'news_date': timezone.now() - timedelta(days=12),
                'summary': 'The company announces a comprehensive environmental sustainability program aimed at reducing carbon emissions by 25% over the next three years while maintaining production efficiency.',
                'news_body': '''Sarbottam Cement Limited has launched an ambitious environmental sustainability initiative as part of its commitment to responsible manufacturing and environmental stewardship. The program aims to reduce the company's carbon footprint by 25% over the next three years.

Key Environmental Initiatives:

1. Carbon Emission Reduction
   • Implementation of energy-efficient technologies
   • Transition to renewable energy sources
   • Optimization of production processes

2. Waste Management Program
   • Zero waste to landfill policy
   • Recycling of industrial by-products
   • Water conservation measures

3. Green Technology Investment
   • Upgrading to latest European eco-friendly equipment
   • Investment in clean technology research
   • Partnership with environmental organizations

The Chairman emphasized: "As Nepal's leading cement manufacturer, we recognize our responsibility towards environmental protection. This initiative reflects our commitment to sustainable development and our vision for a greener future."

The program has received support from international environmental agencies and aligns with Nepal's climate change mitigation goals. The company expects this initiative to enhance its competitive position while contributing to national environmental objectives.

Implementation will begin in Q1 2025, with quarterly progress reports to be published for stakeholder transparency.''',
                'category': 'Sustainability',
                'is_featured': True,
                'is_published': True
            },
            {
                'news_title': 'Board of Directors Approves Dividend Distribution for Shareholders',
                'news_date': timezone.now() - timedelta(days=18),
                'summary': 'The Board has approved a dividend payment of NPR 12 per share, representing a 20% increase from the previous year, reflecting the company\'s strong financial performance.',
                'news_body': '''The Board of Directors of Sarbottam Cement Limited has approved the distribution of dividend to shareholders at the rate of NPR 12 per share for the fiscal year 2023/24. This represents a significant 20% increase from the previous year's dividend of NPR 10 per share.

Dividend Details:
• Dividend Rate: NPR 12 per share
• Total Distribution: NPR 96 million
• Record Date: To be announced
• Payment Date: Within 45 days of AGM approval

The dividend decision reflects the company's strong financial performance and commitment to delivering value to shareholders. The increased payout ratio demonstrates management's confidence in the company's future prospects and cash flow generation capabilities.

Key Performance Metrics Supporting Dividend:
• Annual revenue growth of 18%
• Net profit margin of 10.2%
• Strong cash position of NPR 200 million
• Consistent operational performance

The Company Secretary noted: "This dividend increase underscores our commitment to shareholders and reflects the Board's confidence in our sustainable business model and growth trajectory."

Shareholders will need to attend the upcoming Annual General Meeting to formally approve the dividend proposal. The company maintains its progressive dividend policy, aiming to provide consistent returns while retaining adequate capital for growth investments.

The announcement has been positively received by market analysts, with several upgrading their price targets for SARBTM shares.''',
                'category': 'Corporate Announcement',
                'is_featured': False,
                'is_published': True
            }
        ]

        for news_data in sample_news:
            news, created = CompanyNews.objects.get_or_create(
                company=company,
                news_title=news_data['news_title'],
                defaults=news_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Added news: {news.news_title[:50]}...'))
            else:
                self.stdout.write(self.style.WARNING(f'News already exists: {news.news_title[:50]}...'))

        # Add sample financial data
        financial_data = [
            {
                'report_period': 'Q3 2024',
                'total_revenue': 450.0,
                'net_income': 45.0,
                'earnings_per_share': 5.62,
                'total_assets': 2500.0,
                'total_liabilities': 800.0,
                'shareholders_equity': 1700.0,
                'report_date': timezone.now() - timedelta(days=30)
            },
            {
                'report_period': 'Q2 2024',
                'total_revenue': 420.0,
                'net_income': 38.0,
                'earnings_per_share': 4.75,
                'total_assets': 2450.0,
                'total_liabilities': 750.0,
                'shareholders_equity': 1700.0,
                'report_date': timezone.now() - timedelta(days=120)
            },
            {
                'report_period': 'Q1 2024',
                'total_revenue': 380.0,
                'net_income': 32.0,
                'earnings_per_share': 4.00,
                'total_assets': 2400.0,
                'total_liabilities': 720.0,
                'shareholders_equity': 1680.0,
                'report_date': timezone.now() - timedelta(days=210)
            }
        ]

        for fin_data in financial_data:
            financial, created = CompanyFinancial.objects.get_or_create(
                company=company,
                report_period=fin_data['report_period'],
                defaults=fin_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Added financial data for {financial.report_period}'))
            else:
                self.stdout.write(self.style.WARNING(f'Financial data already exists for {financial.report_period}'))

        # Add sample achievements
        achievements_data = [
            {
                'title': 'First European Production Line in Nepal',
                'description': 'Sarbottam Cement became the first and only cement manufacturer in Nepal to implement a completely European production line, setting new industry standards.',
                'achievement_date': datetime(2012, 6, 15).date(),
                'category': 'Technology Innovation'
            },
            {
                'title': 'ISO 9001:2015 Quality Certification',
                'description': 'Successfully obtained international quality management certification, demonstrating commitment to product quality and customer satisfaction.',
                'achievement_date': datetime(2018, 3, 20).date(),
                'category': 'Quality Certification'
            },
            {
                'title': 'Best Cement Company Award 2023',
                'description': 'Recognized as the Best Cement Company by Nepal Chamber of Commerce for outstanding contribution to the construction industry.',
                'achievement_date': datetime(2023, 11, 10).date(),
                'category': 'Industry Recognition'
            },
            {
                'title': 'Environmental Excellence Award',
                'description': 'Received recognition for environmental sustainability initiatives and commitment to eco-friendly manufacturing practices.',
                'achievement_date': datetime(2023, 8, 5).date(),
                'category': 'Environmental'
            }
        ]

        for ach_data in achievements_data:
            achievement, created = CompanyAchievement.objects.get_or_create(
                company=company,
                title=ach_data['title'],
                defaults=ach_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Added achievement: {achievement.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Achievement already exists: {achievement.title}'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Sample data addition completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Company: {company.name} ({company.symbol})'))
        self.stdout.write(self.style.SUCCESS(f'News Articles: {CompanyNews.objects.filter(company=company).count()}'))
        self.stdout.write(self.style.SUCCESS(f'Financial Reports: {CompanyFinancial.objects.filter(company=company).count()}'))
        self.stdout.write(self.style.SUCCESS(f'Achievements: {CompanyAchievement.objects.filter(company=company).count()}'))
