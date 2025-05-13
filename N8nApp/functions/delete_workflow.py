#!/usr/bin/env python3
"""
Workflow silme işlevleri
"""

import requests
from functions.utils import N8N_URL, headers
from functions.list_workflows import list_workflows

def delete_workflow():
    """ID ile workflow sil"""
    workflows = list_workflows()
    
    if not workflows:
        return
    
    try:
        choice = int(input("\nSILMEK istediğiniz workflow'un numarasını girin (0 iptal): "))
        if choice == 0:
            return
        
        if choice < 1 or choice > len(workflows):
            print("Geçersiz seçim.")
            return
        
        workflow_id = workflows[choice-1]["id"]
        workflow_name = workflows[choice-1]["name"]
        
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
