from django.core.management.base import BaseCommand
from django.db import transaction
from optimasite.models import users, user_wallets
from optimasite.services.wallet_service import EnhancedWalletService

class Command(BaseCommand):
    help = 'Crée des wallets pour tous les utilisateurs existants'

    def handle(self, *args, **options):
        service = EnhancedWalletService()
        
        # Récupérer tous les utilisateurs sans wallet
        users_without_wallet = users.objects.filter(wallet__isnull=True)
        total_users = users_without_wallet.count()
        
        self.stdout.write(f'Trouvé {total_users} utilisateurs sans wallet')
        
        created_count = 0
        error_count = 0
        
        for user in users_without_wallet:
            try:
                # Déterminer la devise
                currency_code = user._get_user_currency_code()
                
                # Créer le wallet
                wallet = service.create_wallet(user, currency_code)
                
                if wallet:
                    created_count += 1
                    self.stdout.write(f'✓ Wallet créé pour {user.username} - Devise: {currency_code}')
                else:
                    error_count += 1
                    self.stdout.write(f'✗ Erreur pour {user.username}')
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(f'✗ Erreur pour {user.username}: {str(e)}')
        
        self.stdout.write(f'\nTerminé! {created_count} wallets créés, {error_count} erreurs')
