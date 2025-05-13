#!/usr/bin/env python3
"""
Workflow listeleme işlevleri
"""

import requests
from functions.utils import N8N_URL, headers

def list_workflows():
    """Tüm workflow'ları ID ve isimleriyle listeler"""
    print("\nWorkflow'lar getiriliyor...\n")
    
    try:
        response = requests.get(f"{N8N_URL}/api/v1/workflows?limit=100", headers=headers)
        response.raise_for_status()
        
        response_data = response.json()
        
        # API yanıt formatını kontrol et
        if isinstance(response_data, dict) and "data" in response_data:
            # Yeni API formatı - 'data' içinde workflow array'i var
            workflows = response_data["data"]
        else:
            # Eski API formatı - doğrudan workflow array'i
            workflows = response_data
        
        if not workflows or len(workflows) == 0:
            print("Hiç workflow bulunamadı.")
            return
        
        print(f"Toplam {len(workflows)} workflow bulundu:\n")
        for idx, workflow in enumerate(workflows, 1):
            # Tip kontrolü ekle
            if isinstance(workflow, dict):
                active_status = "[Aktif]" if workflow.get("active", False) else "[Pasif]"
                print(f"{idx}. {active_status} ID: {workflow['id']} - İsim: {workflow['name']}")
            else:
                print(f"{idx}. Geçersiz workflow verisi: {workflow}")
        
        # Olası ileri kullanım için workflow'ları döndür
        return workflows
    
    except requests.exceptions.RequestException as e:
        print(f"Workflow'ları getirirken hata oluştu: {str(e)}")
        return None
