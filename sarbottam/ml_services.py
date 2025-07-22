import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

from .models import PriceHistory, Company


class StockPricePredictor:
    """Machine Learning service for stock price prediction"""

    def __init__(self):
        self.scaler = MinMaxScaler() if ML_AVAILABLE else None
        self.models = {}
        self.is_trained = False

    def prepare_data(self, company_symbol='SARBTM'):
        """Prepare data for ML training"""
        try:
            company = Company.objects.get(symbol=company_symbol)
            price_data = PriceHistory.objects.filter(
                company=company
            ).order_by('date')

            if price_data.count() < 10:
                raise ValueError(f"Insufficient data: only {price_data.count()} records found. Need at least 10 records.")

            # Convert to DataFrame
            data = []
            for price in price_data:
                data.append({
                    'date': price.date,
                    'open': float(price.open_price),
                    'high': float(price.high_price),
                    'low': float(price.low_price),
                    'close': float(price.close_price),
                    'volume': int(price.volume) if price.volume else 0
                })

            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)

            # Feature engineering
            df['price_change'] = df['close'].pct_change()
            df['volatility'] = (df['high'] - df['low']) / df['close']
            df['volume_ma'] = df['volume'].rolling(window=3, min_periods=1).mean()
            df['price_ma_3'] = df['close'].rolling(window=3, min_periods=1).mean()
            df['price_ma_5'] = df['close'].rolling(window=5, min_periods=1).mean()

            # Technical indicators
            df['rsi'] = self.calculate_rsi(df['close'])
            df['macd'] = self.calculate_macd(df['close'])

            # Fill NaN values
            df = df.fillna(method='bfill').fillna(method='ffill')

            return df

        except Exception as e:
            raise Exception(f"Error preparing data: {str(e)}")

    def calculate_rsi(self, prices, window=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window, min_periods=1).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50)  # Fill NaN with neutral RSI

    def calculate_macd(self, prices, fast=12, slow=26):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        exp1 = prices.ewm(span=fast, min_periods=1).mean()
        exp2 = prices.ewm(span=slow, min_periods=1).mean()
        macd = exp1 - exp2
        return macd.fillna(0)

    def train_models(self, df):
        """Train multiple ML models"""
        if not ML_AVAILABLE:
            raise ImportError("ML libraries not available. Please install: pip install scikit-learn tensorflow numpy")

        # Prepare features and target
        feature_columns = ['open', 'high', 'low', 'volume', 'price_change', 'volatility',
                          'volume_ma', 'price_ma_3', 'price_ma_5', 'rsi', 'macd']

        X = df[feature_columns].values
        y = df['close'].values

        # Split data (use last 20% for testing)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train Linear Regression
        self.models['linear'] = LinearRegression()
        self.models['linear'].fit(X_train_scaled, y_train)

        # Train Random Forest
        self.models['random_forest'] = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        self.models['random_forest'].fit(X_train_scaled, y_train)

        # Train LSTM model
        self.models['lstm'] = self.create_lstm_model(df)

        # Calculate accuracy metrics
        self.evaluate_models(X_test_scaled, y_test)

        self.is_trained = True
        return True

    def create_lstm_model(self, df):
        """Create and train LSTM model for time series prediction"""
        try:
            # Prepare LSTM data
            close_prices = df['close'].values.reshape(-1, 1)
            scaled_data = self.scaler.fit_transform(close_prices)

            # Create sequences for LSTM
            sequence_length = min(5, len(scaled_data) - 1)  # Use 5 days or less if data is limited
            X_lstm, y_lstm = [], []

            for i in range(sequence_length, len(scaled_data)):
                X_lstm.append(scaled_data[i-sequence_length:i, 0])
                y_lstm.append(scaled_data[i, 0])

            if len(X_lstm) == 0:
                return None

            X_lstm = np.array(X_lstm)
            y_lstm = np.array(y_lstm)

            # Reshape for LSTM
            X_lstm = np.reshape(X_lstm, (X_lstm.shape[0], X_lstm.shape[1], 1))

            # Build LSTM model
            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(sequence_length, 1)),
                Dropout(0.2),
                LSTM(50, return_sequences=False),
                Dropout(0.2),
                Dense(25),
                Dense(1)
            ])

            model.compile(optimizer='adam', loss='mean_squared_error')

            # Train model
            model.fit(X_lstm, y_lstm, batch_size=1, epochs=50, verbose=0)

            return model

        except Exception as e:
            print(f"LSTM training error: {str(e)}")
            return None

    def evaluate_models(self, X_test, y_test):
        """Evaluate model performance"""
        self.metrics = {}

        for name, model in self.models.items():
            if model is None:
                continue

            try:
                if name == 'lstm':
                    continue  # LSTM evaluation handled separately

                predictions = model.predict(X_test)
                mae = mean_absolute_error(y_test, predictions)
                mse = mean_squared_error(y_test, predictions)

                self.metrics[name] = {
                    'mae': mae,
                    'mse': mse,
                    'rmse': np.sqrt(mse)
                }
            except Exception as e:
                print(f"Error evaluating {name}: {str(e)}")

    def predict_next_days(self, days=5, company_symbol='SARBTM'):
        """Predict stock prices for the next N days"""
        try:
            if not ML_AVAILABLE:
                return self.simple_prediction(days, company_symbol)

            # Prepare data
            df = self.prepare_data(company_symbol)

            if not self.is_trained:
                self.train_models(df)

            # Get latest data for prediction
            latest_data = df.iloc[-1]
            predictions = {}

            # Linear Regression prediction
            if 'linear' in self.models:
                predictions['linear'] = self.predict_with_linear(latest_data, days)

            # Random Forest prediction
            if 'random_forest' in self.models:
                predictions['random_forest'] = self.predict_with_rf(latest_data, days)

            # LSTM prediction
            if 'lstm' in self.models and self.models['lstm'] is not None:
                predictions['lstm'] = self.predict_with_lstm(df, days)

            # Ensemble prediction (average of all models)
            predictions['ensemble'] = self.create_ensemble_prediction(predictions, days)

            # Generate future dates
            last_date = df['date'].max()
            future_dates = []
            for i in range(1, days + 1):
                next_date = last_date + timedelta(days=i)
                # Skip weekends (assuming stock market is closed)
                while next_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                    next_date += timedelta(days=1)
                future_dates.append(next_date.date())

            # Format results
            results = []
            best_model = self.get_best_model()

            for i, date in enumerate(future_dates):
                if i < len(predictions[best_model]):
                    predicted_price = predictions[best_model][i]

                    # Add confidence interval
                    confidence = self.calculate_confidence(df, predicted_price)

                    results.append({
                        'date': date,
                        'predicted_price': round(predicted_price, 2),
                        'confidence_lower': round(predicted_price - confidence, 2),
                        'confidence_upper': round(predicted_price + confidence, 2),
                        'model_used': best_model,
                        'all_predictions': {k: round(v[i], 2) if i < len(v) else 0
                                          for k, v in predictions.items()}
                    })

            return {
                'success': True,
                'predictions': results,
                'model_metrics': getattr(self, 'metrics', {}),
                'data_points_used': len(df),
                'last_actual_price': float(df['close'].iloc[-1]),
                'last_actual_date': df['date'].iloc[-1].date()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'predictions': []
            }

    def predict_with_linear(self, latest_data, days):
        """Predict using Linear Regression"""
        predictions = []
        current_data = latest_data.copy()

        feature_columns = ['open', 'high', 'low', 'volume', 'price_change', 'volatility',
                          'volume_ma', 'price_ma_3', 'price_ma_5', 'rsi', 'macd']

        for _ in range(days):
            features = current_data[feature_columns].values.reshape(1, -1)
            features_scaled = self.scaler.transform(features)
            prediction = self.models['linear'].predict(features_scaled)[0]
            predictions.append(prediction)

            # Update current_data for next prediction
            current_data['close'] = prediction
            current_data['open'] = prediction * 0.995  # Assume small gap
            current_data['high'] = prediction * 1.005
            current_data['low'] = prediction * 0.995

        return predictions

    def predict_with_rf(self, latest_data, days):
        """Predict using Random Forest"""
        predictions = []
        current_data = latest_data.copy()

        feature_columns = ['open', 'high', 'low', 'volume', 'price_change', 'volatility',
                          'volume_ma', 'price_ma_3', 'price_ma_5', 'rsi', 'macd']

        for _ in range(days):
            features = current_data[feature_columns].values.reshape(1, -1)
            features_scaled = self.scaler.transform(features)
            prediction = self.models['random_forest'].predict(features_scaled)[0]
            predictions.append(prediction)

            # Update current_data for next prediction
            current_data['close'] = prediction
            current_data['open'] = prediction * 0.995
            current_data['high'] = prediction * 1.005
            current_data['low'] = prediction * 0.995

        return predictions

    def predict_with_lstm(self, df, days):
        """Predict using LSTM model"""
        try:
            close_prices = df['close'].values.reshape(-1, 1)
            scaled_data = self.scaler.fit_transform(close_prices)

            sequence_length = min(5, len(scaled_data) - 1)
            last_sequence = scaled_data[-sequence_length:].reshape(1, sequence_length, 1)

            predictions = []
            current_sequence = last_sequence.copy()

            for _ in range(days):
                prediction = self.models['lstm'].predict(current_sequence, verbose=0)[0][0]
                predictions.append(prediction)

                # Update sequence for next prediction
                new_sequence = np.append(current_sequence[0][1:], prediction)
                current_sequence = new_sequence.reshape(1, sequence_length, 1)

            # Inverse transform predictions
            predictions = self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
            return predictions.flatten().tolist()

        except Exception as e:
            print(f"LSTM prediction error: {str(e)}")
            return []

    def create_ensemble_prediction(self, predictions, days):
        """Create ensemble prediction by averaging all models"""
        ensemble = []
        for i in range(days):
            day_predictions = []
            for model_name, model_predictions in predictions.items():
                if model_name != 'ensemble' and i < len(model_predictions):
                    day_predictions.append(model_predictions[i])

            if day_predictions:
                ensemble.append(sum(day_predictions) / len(day_predictions))
            else:
                ensemble.append(0)

        return ensemble

    def get_best_model(self):
        """Determine the best performing model"""
        if not hasattr(self, 'metrics') or not self.metrics:
            return 'ensemble'

        best_model = 'linear'
        best_score = float('inf')

        for model_name, metrics in self.metrics.items():
            if metrics['mae'] < best_score:
                best_score = metrics['mae']
                best_model = model_name

        return best_model

    def calculate_confidence(self, df, predicted_price):
        """Calculate confidence interval for prediction"""
        recent_volatility = df['close'].tail(10).std()
        return recent_volatility * 1.96  # 95% confidence interval

    def simple_prediction(self, days, company_symbol):
        """Simple prediction when ML libraries are not available"""
        try:
            company = Company.objects.get(symbol=company_symbol)
            recent_prices = PriceHistory.objects.filter(
                company=company
            ).order_by('-date')[:10]

            if not recent_prices:
                raise ValueError("No price data available")

            prices = [float(p.close_price) for p in recent_prices]

            # Simple moving average prediction
            avg_price = sum(prices) / len(prices)
            trend = (prices[0] - prices[-1]) / len(prices) if len(prices) > 1 else 0

            results = []
            last_date = recent_prices[0].date

            for i in range(1, days + 1):
                next_date = last_date + timedelta(days=i)
                while next_date.weekday() >= 5:
                    next_date += timedelta(days=1)

                predicted_price = avg_price + (trend * i)

                results.append({
                    'date': next_date,
                    'predicted_price': round(predicted_price, 2),
                    'confidence_lower': round(predicted_price * 0.95, 2),
                    'confidence_upper': round(predicted_price * 1.05, 2),
                    'model_used': 'simple_moving_average',
                    'all_predictions': {'simple': round(predicted_price, 2)}
                })

            return {
                'success': True,
                'predictions': results,
                'model_metrics': {'simple': 'Moving average with trend'},
                'data_points_used': len(prices),
                'last_actual_price': prices[0],
                'last_actual_date': last_date
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'predictions': []
            }
