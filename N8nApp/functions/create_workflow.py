#!/usr/bin/env python3
"""
Yeni workflow oluşturma işlevleri
"""

import json
import requests
from functions.utils import N8N_URL, headers_with_content_type

def create_workflow():
    """Kullanıcıdan isim alarak yeni bir workflow oluştur"""
    workflow_name = input("\nYeni workflow için isim girin: ")
    
    if not workflow_name:
        print("Workflow ismi boş olamaz. İşlem iptal edildi.")
        return
    
    # N8N API beklediği formatta workflow şablonu
    workflow_template = {
        "name": workflow_name,
        "nodes": [
            {
                "id": "0f5532f9-36ba-4bef-86c7-30d607400b15",
                "name": "Start",
                "type": "n8n-nodes-base.start",
                "typeVersion": 1,
                "position": [0, 0],
                "parameters": {}
            }
        ],
        "connections": {},
        "settings": {
            "executionOrder": "v1"
        },
        "staticData": {}
    }
    
    try:
        print(f"\n'{workflow_name}' isimli yeni workflow oluşturuluyor...")
        
        # JSON formatında veri gönder (data yerine json parametresi kullan)
        response = requests.post(
            f"{N8N_URL}/api/v1/workflows",
            headers=headers_with_content_type,
            json=workflow_template  # data=json.dumps yerine doğrudan json kullan
        )
        
        # Hata durumunda detaylı bilgi göster
        if response.status_code != 200 and response.status_code != 201:
            print(f"Hata Kodu: {response.status_code}")
            print(f"Hata Detayı: {response.text}")
            print(f"Gönderilen veri: {json.dumps(workflow_template, indent=2)}")
            print(f"Headers: {headers_with_content_type}")
        
        response.raise_for_status()
        
        new_workflow = response.json()
        print(f"\nWorkflow başarıyla oluşturuldu!")
        print(f"ID: {new_workflow['id']}")
        print(f"İsim: {new_workflow['name']}")
    
    except requests.exceptions.RequestException as e:
        print(f"Workflow oluştururken hata oluştu: {str(e)}")
