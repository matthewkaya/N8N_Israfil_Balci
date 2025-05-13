#!/usr/bin/env python3
"""
Menü fonksiyonu
"""

from functions.utils import clear_screen

def display_menu():
    """Ana menü seçeneklerini göster"""
    clear_screen()
    print("\n===== N8N API CLI =====")
    print("1. Tüm workflow'ları listele (ID ve isim)")
    print("2. Workflow detayını ID ile getir ve JSON olarak kaydet")
    print("3. Yeni workflow oluştur")
    print("4. Var olan workflow'u güncelle")
    print("5. Workflow sil (ID ile)")
    print("6. Workflow'u aktif et")
    print("7. Workflow'u pasif yap")
    print("8. Workflow'un mevcut etiketlerini getir")
    print("9. Workflow'a etiket ata (tag ID ile)")
    print("10. Workflow'tan etiket kaldır")
    print("0. Çıkış")
    print("=======================")
