"""
Migrate blacklist.txt entries to database
Run with: python manage.py shell < scripts/migrate_blacklist_txt.py
"""
import re
from blacklist.models import Blacklist

def migrate_blacklist():
    with open('blacklist.txt', 'r') as f:
        lines = f.readlines()
    
    added = 0
    skipped = 0
    
    for line in lines:
        phrase = line.strip()
        if not phrase or phrase.startswith('#'):
            continue
        
        # Escape the phrase and wrap with word boundaries
        regex_pattern = fr'\s+{re.escape(phrase)}\s+'
        
        # Check if already exists
        if Blacklist.objects.filter(regex=regex_pattern).exists():
            skipped += 1
            continue
        
        try:
            Blacklist.objects.create(regex=regex_pattern, is_temp=False)
            added += 1
            print(f"Added: {phrase}")
        except Exception as e:
            print(f"Error adding {phrase}: {e}")
    
    print(f"\nMigration complete: {added} added, {skipped} skipped (already exist)")

migrate_blacklist()
