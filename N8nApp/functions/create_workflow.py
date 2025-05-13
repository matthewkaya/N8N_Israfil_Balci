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
    
    # Minimal workflow için şablon
    workflow_template = {
        "name": workflow_name,
        "nodes": [],
        "connections": {},
        "settings": {
            "executionOrder": "v1"
        },
        "active": False
    }
    
    try:
        print(f"\n'{workflow_name}' isimli yeni workflow oluşturuluyor...")
        response = requests.post(
            f"{N8N_URL}/api/v1/workflows",
            headers=headers_with_content_type,
            data=json.dumps(workflow_template)
        )
        response.raise_for_status()
        
        new_workflow = response.json()
        print(f"\nWorkflow başarıyla oluşturuldu!")
        print(f"ID: {new_workflow['id']}")
        print(f"İsim: {new_workflow['name']}")
    
    except requests.exceptions.RequestException as e:
        print(f"Workflow oluştururken hata oluştu: {str(e)}")
