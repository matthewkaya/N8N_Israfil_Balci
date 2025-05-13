#!/usr/bin/env python3
"""
Workflow güncelleme işlevleri
"""

import json
import requests
from functions.utils import N8N_URL, headers, headers_with_content_type
from functions.list_workflows import list_workflows

def update_workflow():
    """Var olan bir workflow'u şablonla güncelle"""
    workflows = list_workflows()
    
    if not workflows:
        return
    
    try:
        choice = int(input("\nGüncellemek istediğiniz workflow'un numarasını girin (0 iptal): "))
        if choice == 0:
            return
        
        if choice < 1 or choice > len(workflows):
            print("Geçersiz seçim.")
            return
        
        selected_workflow = workflows[choice-1]
        workflow_id = selected_workflow["id"]
        
        # Değiştirilecek mevcut workflow'u al
        response = requests.get(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}?excludePinnedData=true",
            headers=headers
        )
        response.raise_for_status()
        current_workflow = response.json()
        
        # Workflow'u değiştir - basit örnek: ismi güncelle
        new_name = input(f"\nYeni isim girin (mevcut: {current_workflow['name']}, değiştirmemek için Enter tuşuna basın): ")
        if new_name:
            current_workflow["name"] = new_name
        
        # Güncellenmiş workflow'u gönder
        print(f"\nWorkflow ID: {workflow_id} güncelleniyor...")
        update_response = requests.put(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            headers=headers_with_content_type,
            data=json.dumps(current_workflow)
        )
        update_response.raise_for_status()
        
        print("\nWorkflow başarıyla güncellendi!")
    
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    except requests.exceptions.RequestException as e:
        print(f"Workflow güncellenirken hata oluştu: {str(e)}")
