#!/usr/bin/env python3
"""
Basit test scripti - N8N API CLI modüllerinin doğru çalıştığını test eder
"""
import os
import sys
import traceback

# Proje dizinini Python path'ine ekle
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    print("Proje dizini Python path'ine eklendi")
except Exception as e:
    print(f"Path eklenirken hata: {e}")
    traceback.print_exc()

# Utils modülünü test et
try:
    from functions.utils import N8N_URL, API_KEY
    print(f"N8N_URL: {N8N_URL}")
    print(f"API_KEY uzunluğu: {len(API_KEY)} karakter")
except Exception as e:
    print(f"Utils modülü hatası: {e}")
    traceback.print_exc()

# Menu modülünü test et
try:
    from functions.menu import display_menu
    print("Menu modülü başarıyla yüklendi")
except Exception as e:
    print(f"Menu modülü hatası: {e}")
    traceback.print_exc()

# List workflows modülünü test et
try:
    from functions.list_workflows import list_workflows
    print("List workflows modülü başarıyla yüklendi")
except Exception as e:
    print(f"List workflows modülü hatası: {e}")
    traceback.print_exc()

print("\nTüm import testleri tamamlandı.")
