from django.core.management.base import BaseCommand
from django.db import transaction
from optimasite.models import users, user_wallets
from optimasite.services.wallet_service import EnhancedWalletService

class Command(BaseCommand):
    help = 'Crée des wallets pour tous les utilisateurs existants'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche ce qui serait fait sans effectuer les changements',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        service = EnhancedWalletService()
        
        if dry_run:
            self.stdout.write(self.style.WARNING('Mode DRY RUN - Aucune modification'))
        
        # Récupérer tous les utilisateurs sans wallet
        users_without_wallet = users.objects.filter(wallet__isnull=True)
        total_users = users_without_wallet.count()
        
        self.stdout.write(f'Trouvé {total_users} utilisateurs sans wallet')
        
        created_count = 0
        error_count = 0
        
        for user in users_without_wallet:
            try:
                if not dry_run:
                    # Déterminer la devise
                    currency_code = user._get_user_currency_code()
                    
                    # Créer le wallet
                    wallet = service.create_wallet(user, currency_code)
                    
                    if wallet:
                        created_count += 1
                        self.stdout.write(f'✓ Wallet créé pour {user.username} - {currency_code}')
                    else:
                        error_count += 1
                        self.stdout.write(f'✗ Erreur pour {user.username}')
                else:
                    # Mode dry-run
                    currency_code = user._get_user_currency_code()
                    self.stdout.write(f'[DRY RUN] Créerait wallet pour {user.username} - {currency_code}')
                    created_count += 1
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(f'✗ Erreur pour {user.username}: {str(e)}')
        
        if not dry_run:
            self.stdout.write(f'\n✅ Terminé! {created_count} wallets créés, {error_count} erreurs')
        else:
            self.stdout.write(f'\n[DRY RUN] {created_count} wallets seraient créés')
