#!/usr/bin/env python3
"""
Workflow aktivasyon işlevleri
"""

import requests
from functions.utils import N8N_URL, headers
from functions.list_workflows import list_workflows

def activate_workflow():
    """ID ile workflow'u aktif et"""
    workflows = list_workflows()
    
    if not workflows:
        return
    
    try:
        choice = int(input("\nAktif etmek istediğiniz workflow'un numarasını girin (0 iptal): "))
        if choice == 0:
            return
        
        if choice < 1 or choice > len(workflows):
            print("Geçersiz seçim.")
            return
        
        workflow_id = workflows[choice-1]["id"]
        
        print(f"\nWorkflow ID: {workflow_id} aktif ediliyor...")
        response = requests.post(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}/activate",
            headers=headers
        )
        response.raise_for_status()
        
        print("\nWorkflow başarıyla aktif edildi!")
    
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    except requests.exceptions.RequestException as e:
        print(f"Workflow aktif edilirken hata oluştu: {str(e)}")

def deactivate_workflow():
    """ID ile workflow'u pasif et"""
    workflows = list_workflows()
    
    if not workflows:
        return
    
    try:
        choice = int(input("\nPasif etmek istediğiniz workflow'un numarasını girin (0 iptal): "))
        if choice == 0:
            return
        
        if choice < 1 or choice > len(workflows):
            print("Geçersiz seçim.")
            return
        
        workflow_id = workflows[choice-1]["id"]
        
        print(f"\nWorkflow ID: {workflow_id} pasif ediliyor...")
        response = requests.post(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}/deactivate",
            headers=headers
        )
        response.raise_for_status()
        
        print("\nWorkflow başarıyla pasif edildi!")
    
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    except requests.exceptions.RequestException as e:
        print(f"Workflow pasif edilirken hata oluştu: {str(e)}")
