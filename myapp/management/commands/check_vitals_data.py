from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import User, WatchVitals
import random


class Command(BaseCommand):
    help = 'Check and optionally populate watch vitals test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--populate',
            action='store_true',
            help='Populate test data for all patients',
        )
        parser.add_argument(
            '--user-id',
            type=int,
            help='Add test data for specific user ID',
        )

    def handle(self, *args, **options):
        self.stdout.write('Checking watch_vitals table...')
        
        # Count total vitals records
        total_vitals = WatchVitals.objects.count()
        self.stdout.write(f'Total watch vitals records: {total_vitals}')
        
        # Get all patients
        patients = User.objects.filter(role='patient')
        self.stdout.write(f'Total patients in system: {patients.count()}')
        
        # Check which patients have vitals
        patients_with_vitals = []
        patients_without_vitals = []
        
        for patient in patients:
            vitals_count = WatchVitals.objects.filter(user=patient).count()
            if vitals_count > 0:
                patients_with_vitals.append((patient, vitals_count))
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Patient {patient.user_id} ({patient.username}): {vitals_count} vitals records'
                    )
                )
            else:
                patients_without_vitals.append(patient)
                self.stdout.write(
                    self.style.WARNING(
                        f'✗ Patient {patient.user_id} ({patient.username}): No vitals data'
                    )
                )
        
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'Patients with vitals: {len(patients_with_vitals)}')
        self.stdout.write(f'Patients without vitals: {len(patients_without_vitals)}')
        
        # Populate test data if requested
        if options['populate'] or options['user_id']:
            if options['user_id']:
                # Add data for specific user
                try:
                    user = User.objects.get(user_id=options['user_id'], role='patient')
                    self._create_test_vitals(user)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Created test vitals for patient {user.user_id} ({user.username})'
                        )
                    )
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'✗ Patient with user_id {options["user_id"]} not found'
                        )
                    )
            elif options['populate']:
                # Add data for all patients without vitals
                for patient in patients_without_vitals:
                    self._create_test_vitals(patient)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Created test vitals for patient {patient.user_id} ({patient.username})'
                        )
                    )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\nSuccessfully created test vitals for {len(patients_without_vitals)} patients'
                    )
                )
    
    def _create_test_vitals(self, user):
        """Create realistic test vital signs for a user"""
        # Generate realistic vital signs
        WatchVitals.objects.create(
            user=user,
            device_id=f'WATCH_{user.user_id}',
            heart_rate=random.randint(60, 100),  # Normal range
            systolic=random.randint(110, 130),    # Normal range
            diastolic=random.randint(70, 85),     # Normal range
            spo2=random.randint(95, 100),         # Normal range
            steps=random.randint(1000, 8000),
            calories=random.randint(200, 500),
            distance_m=random.randint(1000, 6000),
            captured_at=timezone.now(),
            created_at=timezone.now(),
            measured_by='Test Data Generator',
            user_email=user.email or f'{user.username}@example.com'
        )
