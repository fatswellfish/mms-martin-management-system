# fix_batch.py
from pathlib import Path

# Target file
file_path = Path("mms/fieldops/models/batch.py")

# Correct content
content = '''from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime

class Base:
    pass

class Batch(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Transfer(Base):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)'''

# Write safely (UTF-8, no null bytes)
try:
    file_path.write_text(content, encoding="utf-8")
    print(f"✅ Successfully wrote to {file_path}")
except Exception as e:
    print(f"❌ Failed to write: {e}")