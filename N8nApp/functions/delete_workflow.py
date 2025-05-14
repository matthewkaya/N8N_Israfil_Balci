#!/usr/bin/env python3
"""
Workflow silme işlevleri
"""

import requests
from functions.utils import N8N_URL, headers

def delete_workflow():
    """ID ile workflow sil"""
    # Doğrudan API'den workflow listesini al
    try:
        print("\nWorkflow'lar getiriliyor...")
        response = requests.get(
            f"{N8N_URL}/api/v1/workflows",
            headers=headers
        )
        response.raise_for_status()
        
        data = response.json()
        # Ensure we're getting the data in the right format - API may return data in a nested structure
        workflows = data if isinstance(data, list) else data.get("data", [])
        
        if not workflows:
            print("Hiç workflow bulunamadı.")
            return
        
        print(f"\nToplam {len(workflows)} workflow bulundu:\n")
        
        for i, workflow in enumerate(workflows, 1):
            if isinstance(workflow, dict):
                status = "Aktif" if workflow.get("active", False) else "Pasif"
                print(f"{i}. [{status}] ID: {workflow.get('id')} - İsim: {workflow.get('name')}")
            else:
                print(f"{i}. [Bilinmiyor] - {workflow}")
    
        choice = int(input("\nSILMEK istediğiniz workflow'un numarasını girin (0 iptal): "))
        if choice == 0:
            return
        
        if choice < 1 or choice > len(workflows):
            print("Geçersiz seçim.")
            return
        
        selected_workflow = workflows[choice-1]
        
        if not isinstance(selected_workflow, dict):
            print("Seçilen workflow formatı geçersiz.")
            return
            
        workflow_id = selected_workflow.get("id")
        workflow_name = selected_workflow.get("name", "İsimsiz")
        
        if not workflow_id:
            print("Seçilen workflow'un ID'si bulunamadı.")
            return
            
        confirm = input(f"\n⚠️ UYARI: '{workflow_name}' (ID: {workflow_id}) isimli workflow'u SILMEK üzeresiniz.\nBu işlem geri alınamaz. Onaylamak için 'SIL' yazın: ")
        
        if confirm != "SIL":
            print("\nSilme işlemi iptal edildi.")
            return
        
        print(f"\nWorkflow ID: {workflow_id} siliniyor...")
        response = requests.delete(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            headers=headers
        )
        response.raise_for_status()
        
        print("\nWorkflow başarıyla silindi!")
    
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    except requests.exceptions.RequestException as e:
        print(f"Workflow silinirken hata oluştu: {str(e)}")
