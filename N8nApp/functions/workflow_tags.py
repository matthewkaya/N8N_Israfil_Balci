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
        # API'den dönen JSON hata mesajını çıkarmaya çalış
        error_detail = str(e)
        try:
            if hasattr(e, 'response') and e.response is not None:
                error_json = e.response.json()
                if 'message' in error_json:
                    error_detail = error_json['message']
        except:
            pass  # JSON parse edilemezse orijinal hata mesajını kullan
        
        print(f"Workflow etiketleri getirilirken hata oluştu: {error_detail}")

def get_all_tags():
    """Tüm mevcut tagleri getir"""
    try:
        print("\nTüm taglar getiriliyor...")
        response = requests.get(
            f"{N8N_URL}/api/v1/tags",
            headers=headers
        )
        response.raise_for_status()
        
        tags = response.json()
        
        if not tags or len(tags) == 0:
            print("\nSistemde kayıtlı tag bulunamadı.")
            return
        
        print(f"\nToplam {len(tags)} tag bulundu:\n")
        for idx, tag in enumerate(tags, 1):
            if isinstance(tag, dict):
                print(f"{idx}. ID: {tag.get('id')} - İsim: {tag.get('name')}")
            else:
                print(f"{idx}. {tag}")
            
        # Beğenilen taglerin ID'lerini kaydetme veya kopyalama imkanı sunabilirsiniz
        copy_choice = input("\nBir tag ID'sini kopyalamak ister misiniz? (tag numarası/h): ")
        if copy_choice.lower() != 'h':
            try:
                copy_idx = int(copy_choice)
                if copy_idx > 0 and copy_idx <= len(tags):
                    tag = tags[copy_idx-1]
                    if isinstance(tag, dict):
                        tag_id = tag.get('id')
                        tag_name = tag.get('name')
                        print(f"\nTag ID: {tag_id} - İsim: {tag_name}")
                        print("Bu ID'yi kullanarak workflow'a etiket atayabilirsiniz.")
                    else:
                        print(f"\nTag: {tag}")
                else:
                    print("Geçersiz numara.")
            except ValueError:
                print("Geçerli bir sayı girilmedi.")
                
    except requests.exceptions.RequestException as e:
        error_detail = str(e)
        try:
            if hasattr(e, 'response') and e.response is not None:
                error_json = e.response.json()
                if 'message' in error_json:
                    error_detail = error_json['message']
        except:
            pass  # JSON parse edilemezse orijinal hata mesajını kullan
        
        print(f"Taglar getirilirken hata oluştu: {error_detail}")

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
        
        # Önce mevcut tagleri getir
        get_all_tags()
        
        tag_id = input("\nAtamak istediğiniz tag ID'sini girin: ")
        
        if not tag_id:
            print("Tag ID'si boş olamaz. İşlem iptal edildi.")
            return
        
        tag_data = [{"id": tag_id}]
        
        print(f"\nWorkflow ID: {workflow_id} için tag atanıyor...")
        response = requests.put(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}/tags",
            headers=headers_with_content_type,
            data=json.dumps(tag_data)
        )
        response.raise_for_status()
        
        print("\nTag başarıyla atandı!")
    
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    except requests.exceptions.RequestException as e:
        error_detail = str(e)
        try:
            if hasattr(e, 'response') and e.response is not None:
                error_json = e.response.json()
                if 'message' in error_json:
                    error_detail = error_json['message']
        except:
            pass  # JSON parse edilemezse orijinal hata mesajını kullan
        
        print(f"Tag atanırken hata oluştu: {error_detail}")

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
        # API'den dönen JSON hata mesajını çıkarmaya çalış
        error_detail = str(e)
        try:
            if hasattr(e, 'response') and e.response is not None:
                error_json = e.response.json()
                if 'message' in error_json:
                    error_detail = error_json['message']
        except:
            pass  # JSON parse edilemezse orijinal hata mesajını kullan
        
        print(f"Etiketler kaldırılırken hata oluştu: {error_detail}")
