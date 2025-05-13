#!/usr/bin/env python3
"""
Workflow etiket (tag) işlevleri
"""

import json
import requests
from functions.utils import N8N_URL, headers, headers_with_content_type
from functions.list_workflows import list_workflows

def get_workflow_tags():
    """Workflow'a atanmış mevcut etiketleri getir"""
    workflows = list_workflows()
    
    if not workflows:
        return
    
    try:
        choice = int(input("\nEtiketlerini görmek istediğiniz workflow'un numarasını girin (0 iptal): "))
        if choice == 0:
            return
        
        if choice < 1 or choice > len(workflows):
            print("Geçersiz seçim.")
            return
        
        workflow_id = workflows[choice-1]["id"]
        
        print(f"\nWorkflow ID: {workflow_id} için etiketler getiriliyor...")
        response = requests.get(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}/tags",
            headers=headers
        )
        response.raise_for_status()
        
        tags = response.json()
        
        if not tags or len(tags) == 0:
            print("\nBu workflow'a atanmış etiket yok.")
            return
        
        print("\nBu workflow'a atanmış etiketler:")
        for idx, tag in enumerate(tags, 1):
            print(f"{idx}. ID: {tag.get('id')} - İsim: {tag.get('name')}")
    
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    except requests.exceptions.RequestException as e:
        print(f"Workflow etiketleri getirilirken hata oluştu: {str(e)}")

def assign_tag():
    """Workflow'a etiket ata"""
    workflows = list_workflows()
    
    if not workflows:
        return
    
    try:
        choice = int(input("\nEtiket atamak istediğiniz workflow'un numarasını girin (0 iptal): "))
        if choice == 0:
            return
        
        if choice < 1 or choice > len(workflows):
            print("Geçersiz seçim.")
            return
        
        workflow_id = workflows[choice-1]["id"]
        
        # Bu örnekte doğrudan etiket ID'si soracağız
        # Daha gelişmiş bir uygulamada, önce mevcut etiketleri listeleyebilirsiniz
        tag_id = input("\nAtamak istediğiniz etiket ID'sini girin: ")
        
        if not tag_id:
            print("Etiket ID'si boş olamaz. İşlem iptal edildi.")
            return
        
        tag_data = [{"id": tag_id}]
        
        print(f"\nWorkflow ID: {workflow_id} etiketi atanıyor...")
        response = requests.put(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}/tags",
            headers=headers_with_content_type,
            data=json.dumps(tag_data)
        )
        response.raise_for_status()
        
        print("\nEtiket başarıyla atandı!")
    
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    except requests.exceptions.RequestException as e:
        print(f"Etiket atanırken hata oluştu: {str(e)}")

def remove_tags():
    """Workflow'dan tüm etiketleri kaldır"""
    workflows = list_workflows()
    
    if not workflows:
        return
    
    try:
        choice = int(input("\nTüm etiketlerini kaldırmak istediğiniz workflow'un numarasını girin (0 iptal): "))
        if choice == 0:
            return
        
        if choice < 1 or choice > len(workflows):
            print("Geçersiz seçim.")
            return
        
        workflow_id = workflows[choice-1]["id"]
        
        print(f"\nWorkflow ID: {workflow_id} için tüm etiketler kaldırılıyor...")
        response = requests.put(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}/tags",
            headers=headers_with_content_type,
            data=json.dumps([])  # Tüm etiketleri kaldırmak için boş dizi
        )
        response.raise_for_status()
        
        print("\nTüm etiketler başarıyla kaldırıldı!")
    
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    except requests.exceptions.RequestException as e:
        print(f"Etiketler kaldırılırken hata oluştu: {str(e)}")
