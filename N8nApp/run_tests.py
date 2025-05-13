#!/usr/bin/env python3
"""
Tüm N8N CLI testlerini çalıştırmak için ana script
"""

import unittest
import sys
import os
from pathlib import Path

# Tests dizinini bul
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = SCRIPT_DIR / "tests"
PROJECT_DIR = SCRIPT_DIR

# Ana dizini ve testler dizinini Python path'ine ekle
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(TESTS_DIR))

if __name__ == "__main__":
    # Testleri keşfet ve çalıştır
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir=TESTS_DIR, pattern="test_*.py")
    
    # Test runner'ı oluştur ve çalıştır
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Başarısız test varsa uygun çıkış kodu ile çık
    sys.exit(not result.wasSuccessful())
