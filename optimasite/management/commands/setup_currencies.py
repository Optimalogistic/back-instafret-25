from django.core.management.base import BaseCommand
from optimasite.models import supported_currencies

class Command(BaseCommand):
    help = 'Setup initial supported currencies'
    
    def handle(self, *args, **options):
        currencies_data = [
            ('USD', 'US Dollar', '$', 1.000000),
            ('EUR', 'Euro', '€', 0.850000),
            ('TND', 'Tunisian Dinar', 'د.ت', 3.100000),
            ('DZD', 'Algerian Dinar', 'د.ج', 134.500000),
        ]
        
        for code, name, symbol, rate in currencies_data:
            currency, created = supported_currencies.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'symbol': symbol,
                    'exchange_rate_to_usd': rate,
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created currency: {code} - {name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Currency already exists: {code}')
                )
