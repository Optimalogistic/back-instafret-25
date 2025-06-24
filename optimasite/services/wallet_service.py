# Remplacez les premières lignes par :
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None
from django.conf import settings
from django.db import transaction
from decimal import Decimal
from datetime import datetime
from django.utils import timezone
from ..models import (
    user_wallets, wallet_transactions, payment_methods, wallet_top_ups,
    supported_currencies, wallet_currency_balances, wallet_coupons, wallet_coupon_usage
)

import logging
logger = logging.getLogger(__name__)

if STRIPE_AVAILABLE:
    stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')

class EnhancedWalletService:
    def __init__(self):
        self.points_per_usd = Decimal('3.00')

    def create_wallet(self, user, main_currency_code='USD'):
        """Create a wallet for a new user with main currency"""
        try:
            # Utiliser uniquement supported_currencies
            main_currency = supported_currencies.objects.get(code=main_currency_code)
            
            # Vérifier si l'utilisateur a déjà un wallet
            wallet, created = user_wallets.objects.get_or_create(
                user=user,
                defaults={
                    'main_currency': main_currency,
                    'points_balance': Decimal('0.00'),
                    'is_active': True
                }
            )

            # Create initial currency balance for main currency
            if created:
                wallet_currency_balances.objects.create(
                    wallet=wallet,
                    currency=main_currency,
                    balance=Decimal('0.00')
                )
                logger.info(f"Wallet créé pour {user.username} avec {main_currency_code}")

            return wallet

        except supported_currencies.DoesNotExist:
            logger.error(f"Devise {main_currency_code} non trouvée dans supported_currencies")
            # Créer USD par défaut si la devise demandée n'existe pas
            usd_currency, created = supported_currencies.objects.get_or_create(
                code='USD',
                defaults={
                    'name': 'US Dollar',
                    'symbol': '$',
                    'exchange_rate_to_usd': Decimal('1.0'),
                    'is_active': True
                }
            )
            return self.create_wallet(user, 'USD')
        except Exception as e:
            logger.error(f"Error creating wallet for user {user.id}: {str(e)}")
            return None

    def admin_credit_wallet(self, user, amount, currency_code, admin_user, description=""):
        """Admin can credit user wallet without payment"""
        try:
            with transaction.atomic():
                wallet = user_wallets.objects.get(user=user)
                currency = supported_currencies.objects.get(code=currency_code)
                
                # Get or create currency balance
                currency_wallet, created = wallet_currency_balances.objects.get_or_create(
                    wallet=wallet,
                    currency=currency,
                    defaults={'balance': Decimal('0.00')}
                )

                balance_before = currency_wallet.balance
                currency_wallet.balance += Decimal(str(amount))
                currency_wallet.save()

                # Create transaction record (sans admin_user car le champ n'existe pas)
                wallet_transactions.objects.create(
                    wallet=wallet,
                    currency=currency,
                    transaction_type='ADMIN_CREDIT',
                    amount=Decimal(str(amount)),
                    balance_before=balance_before,
                    balance_after=currency_wallet.balance,
                    status='COMPLETED',
                    description=description or f'Admin credit by {admin_user.username}',
                    reference_id=f"ADMIN-{admin_user.id}"
                )

                return {
                    'success': True,
                    'new_balance': currency_wallet.balance,
                    'currency': currency_code
                }

        except Exception as e:
            logger.error(f"Error admin crediting wallet: {str(e)}")
            return {'success': False, 'error': str(e)}

    def admin_debit_wallet(self, user, amount, currency_code, admin_user, description=""):
        """Admin can debit user wallet"""
        try:
            with transaction.atomic():
                wallet = user_wallets.objects.get(user=user)
                currency = supported_currencies.objects.get(code=currency_code)

                try:
                    currency_wallet = wallet_currency_balances.objects.get(
                        wallet=wallet,
                        currency=currency
                    )
                except wallet_currency_balances.DoesNotExist:
                    return {'success': False, 'error': f'No {currency_code} balance found'}

                if currency_wallet.balance < Decimal(str(amount)):
                    return {'success': False, 'error': 'Insufficient balance'}

                balance_before = currency_wallet.balance
                currency_wallet.balance -= Decimal(str(amount))
                currency_wallet.save()

                # Create transaction record
                wallet_transactions.objects.create(
                    wallet=wallet,
                    currency=currency,
                    transaction_type='ADMIN_DEBIT',
                    amount=-Decimal(str(amount)),
                    balance_before=balance_before,
                    balance_after=currency_wallet.balance,
                    status='COMPLETED',
                    description=description or f'Admin debit by {admin_user.username}',
                    reference_id=f"ADMIN-{admin_user.id}"
                )

                return {
                    'success': True,
                    'new_balance': currency_wallet.balance,
                    'currency': currency_code
                }

        except Exception as e:
            logger.error(f"Error admin debiting wallet: {str(e)}")
            return {'success': False, 'error': str(e)}

    def apply_coupon(self, user, coupon_code, purchase_amount, currency_code):
        """Apply coupon to wallet transaction"""
        try:
            with transaction.atomic():
                coupon = wallet_coupons.objects.get(code=coupon_code)
                wallet = user_wallets.objects.get(user=user)
                currency = supported_currencies.objects.get(code=currency_code)

                # Validate coupon
                if not coupon.is_valid():
                    return {'success': False, 'error': 'Coupon is not valid or expired'}

                # Check if user already used this coupon
                if wallet_coupon_usage.objects.filter(coupon=coupon, user=user).exists():
                    if coupon.max_uses_per_user <= 1:
                        return {'success': False, 'error': 'Coupon already used'}

                # Check minimum amount
                if purchase_amount < coupon.minimum_amount:
                    return {'success': False, 'error': f'Minimum amount required: {coupon.minimum_amount}'}

                # Calculate discount/bonus
                if coupon.coupon_type == 'BONUS_CREDITS':
                    # Add bonus credits to wallet
                    currency_wallet, created = wallet_currency_balances.objects.get_or_create(
                        wallet=wallet,
                        currency=currency,
                        defaults={'balance': Decimal('0.00')}
                    )

                    balance_before = currency_wallet.balance
                    bonus_amount = coupon.fixed_amount
                    currency_wallet.balance += bonus_amount
                    currency_wallet.save()

                    # Create transaction
                    wallet_transaction = wallet_transactions.objects.create(
                        wallet=wallet,
                        currency=currency,
                        transaction_type='COUPON',
                        amount=bonus_amount,
                        balance_before=balance_before,
                        balance_after=currency_wallet.balance,
                        status='COMPLETED',
                        description=f'Coupon bonus: {coupon.code}'
                    )

                    # Record coupon usage
                    wallet_coupon_usage.objects.create(
                        coupon=coupon,
                        user=user,
                        wallet_transaction=wallet_transaction,
                        discount_amount=bonus_amount
                    )

                    # Update coupon usage count
                    coupon.used_count += 1
                    coupon.save()

                    return {
                        'success': True,
                        'bonus_amount': bonus_amount,
                        'new_balance': currency_wallet.balance
                    }

                else:
                    # Calculate discount for payment
                    discount = coupon.calculate_discount(purchase_amount)
                    return {
                        'success': True,
                        'discount_amount': discount,
                        'final_amount': purchase_amount - discount
                    }

        except wallet_coupons.DoesNotExist:
            return {'success': False, 'error': 'Invalid coupon code'}
        except Exception as e:
            logger.error(f"Error applying coupon: {str(e)}")
            return {'success': False, 'error': str(e)}

    def convert_currency(self, user, from_currency_code, to_currency_code, amount):
        """Convert between currencies in wallet"""
        try:
            with transaction.atomic():
                wallet = user_wallets.objects.get(user=user)
                from_currency = supported_currencies.objects.get(code=from_currency_code)
                to_currency = supported_currencies.objects.get(code=to_currency_code)

                # Get source currency balance
                try:
                    from_wallet = wallet_currency_balances.objects.get(
                        wallet=wallet,
                        currency=from_currency
                    )
                except wallet_currency_balances.DoesNotExist:
                    return {'success': False, 'error': f'No {from_currency_code} balance found'}

                if from_wallet.balance < Decimal(str(amount)):
                    return {'success': False, 'error': 'Insufficient balance'}

                # Calculate conversion
                usd_amount = Decimal(str(amount)) * from_currency.exchange_rate_to_usd
                converted_amount = usd_amount / to_currency.exchange_rate_to_usd

                # Get or create target currency balance
                to_wallet, created = wallet_currency_balances.objects.get_or_create(
                    wallet=wallet,
                    currency=to_currency,
                    defaults={'balance': Decimal('0.00')}
                )

                # Perform conversion
                from_balance_before = from_wallet.balance
                to_balance_before = to_wallet.balance

                from_wallet.balance -= Decimal(str(amount))
                to_wallet.balance += converted_amount

                from_wallet.save()
                to_wallet.save()

                # Create transaction records
                wallet_transactions.objects.create(
                    wallet=wallet,
                    currency=from_currency,
                    transaction_type='CONVERSION',
                    amount=-Decimal(str(amount)),
                    balance_before=from_balance_before,
                    balance_after=from_wallet.balance,
                    status='COMPLETED',
                    description=f'Converted to {to_currency_code}'
                )

                wallet_transactions.objects.create(
                    wallet=wallet,
                    currency=to_currency,
                    transaction_type='CONVERSION',
                    amount=converted_amount,
                    balance_before=to_balance_before,
                    balance_after=to_wallet.balance,
                    status='COMPLETED',
                    description=f'Converted from {from_currency_code}'
                )

                return {
                    'success': True,
                    'converted_amount': converted_amount,
                    'exchange_rate': converted_amount / Decimal(str(amount))
                }

        except Exception as e:
            logger.error(f"Error converting currency: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_wallet_summary(self, user):
        """Get complete wallet summary for user"""
        try:
            wallet = user_wallets.objects.get(user=user)
            currency_balances = []

            for balance in wallet.currency_balances.all():
                currency_balances.append({
                    'currency_code': balance.currency.code,
                    'currency_name': balance.currency.name,
                    'currency_symbol': balance.currency.symbol,
                    'balance': balance.balance,
                    'is_main_currency': balance.currency == wallet.main_currency
                })

            # Calculer le total dans la devise principale
            total_in_main = self._calculate_total_in_main_currency(wallet)

            return {
                'success': True,
                'wallet_id': wallet.wallet_id,
                'main_currency': wallet.main_currency.code,
                'points_balance': wallet.points_balance,
                'currency_balances': currency_balances,
                'total_in_main_currency': total_in_main,
                'is_active': wallet.is_active,
                'is_frozen': wallet.is_frozen
            }

        except Exception as e:
            logger.error(f"Error getting wallet summary: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _calculate_total_in_main_currency(self, wallet):
        """Calculate total balance in main currency"""
        total = Decimal('0.00')
        for currency_balance in wallet.currency_balances.all():
            if currency_balance.currency.code == wallet.main_currency.code:
                total += currency_balance.balance
            else:
                # Convert to main currency
                converted_amount = currency_balance.balance * currency_balance.currency.exchange_rate_to_usd
                if wallet.main_currency.code != 'USD':
                    converted_amount = converted_amount / wallet.main_currency.exchange_rate_to_usd
                total += converted_amount
        return total

    def get_or_create_wallet(self, user):
        """Récupère ou crée un wallet pour l'utilisateur"""
        try:
            return user_wallets.objects.get(user=user)
        except user_wallets.DoesNotExist:
            # Déterminer la devise basée sur le pays de l'utilisateur
            currency_code = self._get_user_currency_from_country(user)
            return self.create_wallet(user, currency_code)

    def _get_user_currency_from_country(self, user):
        """Détermine la devise de l'utilisateur basée sur son pays"""
        # Mapping simple pour les tests
        country_mapping = {
            'Algeria': 'DZD',
            'United States': 'USD',
            'France': 'EUR',
            'Germany': 'EUR',
            'Spain': 'EUR',
            'Italy': 'EUR',
            'Tunisia': 'TND',
            'Senegal': 'CFA',
            'Libya': 'LYD',
            'Mali': 'CFA',
            'Morocco': 'MAD',
            'Egypt': 'EGP',
            'Mauritania': 'MRU'
        }

        try:
            if user.country and user.country.label:
                return country_mapping.get(user.country.label, 'USD')
            return 'USD'
        except:
            return 'USD'

    def credit_wallet(self, user, amount, currency_code, description="", reference=""):
        """Méthode simplifiée pour créditer un wallet"""
        try:
            with transaction.atomic():
                wallet = self.get_or_create_wallet(user)
                currency = supported_currencies.objects.get(code=currency_code)
                
                # Get or create currency balance
                currency_wallet, created = wallet_currency_balances.objects.get_or_create(
                    wallet=wallet,
                    currency=currency,
                    defaults={'balance': Decimal('0.00')}
                )
                
                balance_before = currency_wallet.balance
                currency_wallet.balance += Decimal(str(amount))
                currency_wallet.save()
                
                # Create transaction record
                transaction_record = wallet_transactions.objects.create(
                    wallet=wallet,
                    currency=currency,
                    transaction_type='DEPOSIT',
                    amount=Decimal(str(amount)),
                    balance_before=balance_before,
                    balance_after=currency_wallet.balance,
                    status='COMPLETED',
                    description=description,
                    reference_id=reference
                )
                
                return {
                    'success': True,
                    'new_balance': currency_wallet.balance,
                    'transaction_id': transaction_record.transaction_id
                }
                
        except Exception as e:
            logger.error(f"Error crediting wallet: {str(e)}")
            return {'success': False, 'error': str(e)}

    def create_wallet_for_user(self, user):
        """Crée un wallet pour un utilisateur basé sur son pays (pour compatibilité)"""
        currency_code = self._get_user_currency_from_country(user)
        return self.create_wallet(user, currency_code)
