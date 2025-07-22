from django.core.management.base import BaseCommand
from sarbottam.ml_services import StockPricePredictor
import json


class Command(BaseCommand):
    help = 'Predict stock prices for the next N days using machine learning'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=5,
            help='Number of days to predict (default: 5)'
        )
        parser.add_argument(
            '--symbol',
            type=str,
            default='SARBTM',
            help='Company symbol to predict (default: SARBTM)'
        )
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed prediction information'
        )

    def handle(self, *args, **options):
        days = options['days']
        symbol = options['symbol']
        detailed = options['detailed']

        self.stdout.write(self.style.SUCCESS(f'🔮 Predicting {symbol} stock prices for the next {days} days...'))
        self.stdout.write('')

        try:
            # Initialize predictor
            predictor = StockPricePredictor()

            # Run prediction
            self.stdout.write('📊 Analyzing historical data and training models...')
            results = predictor.predict_next_days(days=days, company_symbol=symbol)

            if not results['success']:
                self.stdout.write(self.style.ERROR(f'❌ Prediction failed: {results["error"]}'))
                return

            # Display results
            self.stdout.write(self.style.SUCCESS('🎯 Prediction Results:'))
            self.stdout.write('=' * 80)

            # Summary info
            self.stdout.write(f'📈 Company: {symbol}')
            self.stdout.write(f'📅 Last actual price: NPR {results["last_actual_price"]} ({results["last_actual_date"]})')
            self.stdout.write(f'🔢 Data points used: {results["data_points_used"]}')
            self.stdout.write('')

            # Predictions table
            self.stdout.write('📋 PRICE PREDICTIONS:')
            self.stdout.write('-' * 80)
            self.stdout.write(f'{"Date":<12} {"Predicted":<12} {"Confidence Range":<20} {"Model":<15}')
            self.stdout.write('-' * 80)

            for pred in results['predictions']:
                date_str = pred['date'].strftime('%Y-%m-%d')
                price_str = f"NPR {pred['predicted_price']}"
                range_str = f"{pred['confidence_lower']} - {pred['confidence_upper']}"
                model_str = pred['model_used'].replace('_', ' ').title()

                self.stdout.write(f'{date_str:<12} {price_str:<12} {range_str:<20} {model_str:<15}')

            self.stdout.write('-' * 80)

            # Calculate prediction summary
            predictions = [p['predicted_price'] for p in results['predictions']]
            current_price = results['last_actual_price']

            avg_prediction = sum(predictions) / len(predictions)
            min_prediction = min(predictions)
            max_prediction = max(predictions)

            # Price change analysis
            price_change = predictions[-1] - current_price
            price_change_pct = (price_change / current_price) * 100

            self.stdout.write('')
            self.stdout.write('📊 PREDICTION SUMMARY:')
            self.stdout.write(f'   Current Price: NPR {current_price}')
            self.stdout.write(f'   Average Prediction: NPR {avg_prediction:.2f}')
            self.stdout.write(f'   Range: NPR {min_prediction:.2f} - NPR {max_prediction:.2f}')
            self.stdout.write(f'   Expected Change: NPR {price_change:.2f} ({price_change_pct:+.2f}%)')

            # Trend analysis
            if price_change > 0:
                trend = '📈 BULLISH'
                trend_color = self.style.SUCCESS
            elif price_change < 0:
                trend = '📉 BEARISH'
                trend_color = self.style.WARNING
            else:
                trend = '➡️  NEUTRAL'
                trend_color = self.style.HTTP_INFO

            self.stdout.write(f'   Trend: {trend_color(trend)}')

            # Model performance (if available)
            if detailed and results.get('model_metrics'):
                self.stdout.write('')
                self.stdout.write('🔬 MODEL PERFORMANCE:')
                for model_name, metrics in results['model_metrics'].items():
                    if isinstance(metrics, dict):
                        self.stdout.write(f'   {model_name.title()}:')
                        self.stdout.write(f'     MAE: {metrics.get("mae", 0):.2f}')
                        self.stdout.write(f'     RMSE: {metrics.get("rmse", 0):.2f}')

            # Show all model predictions if detailed
            if detailed:
                self.stdout.write('')
                self.stdout.write('🤖 ALL MODEL PREDICTIONS:')
                for i, pred in enumerate(results['predictions']):
                    self.stdout.write(f'   Day {i+1} ({pred["date"]}):')
                    for model, price in pred['all_predictions'].items():
                        self.stdout.write(f'     {model.title()}: NPR {price}')

            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('✨ Prediction completed successfully!'))
            self.stdout.write('')
            self.stdout.write('💡 Note: These are ML-based predictions and should not be used as sole investment advice.')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error during prediction: {str(e)}'))
            import traceback
            if detailed:
                self.stdout.write(traceback.format_exc())
