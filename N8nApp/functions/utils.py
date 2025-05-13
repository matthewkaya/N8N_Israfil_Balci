#!/usr/bin/env python3
"""
Yardımcı fonksiyonlar ve ortak kullanılan yapılar
"""

import os
import json
import requests
from dotenv import load_dotenv

# .env dosyasından çevre değişkenlerini yükle
load_dotenv()

# API kimlik bilgilerini çevre değişkenlerinden al
API_KEY = os.getenv("API_KEY")
N8N_URL = os.getenv("N8N_URL")

if not API_KEY or not N8N_URL:
    print("Hata: API_KEY veya N8N_URL .env dosyasında bulunamadı")
    exit(1)

# Tüm API isteklerinde kullanılan başlıklar
headers = {
    "accept": "application/json",
    "X-N8N-API-KEY": API_KEY
}

# Content-Type içeren POST/PUT istekleri için başlıklar
headers_with_content_type = {
    **headers,
    "Content-Type": "application/json"
}

def clear_screen():
    """Terminal ekranını temizler"""
    os.system('clear' if os.name != 'nt' else 'cls')
