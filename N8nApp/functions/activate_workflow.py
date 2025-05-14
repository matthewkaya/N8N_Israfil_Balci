#!/usr/bin/env python3
"""
Workflow aktivasyon işlevleri
"""

import requests
from .utils import N8N_URL, headers, headers_with_content_type

def get_workflows_list():
    """Tüm workflow'ları ID ve isimleriyle listeler ve döndürür (kaydetme isteği olmadan)"""
    print("\nWorkflow'lar getiriliyor...\n")
    
    try:
        # API isteğini güncellenen endpoint ile yap (tüm workflow'ları getir)
        response = requests.get(f"{N8N_URL}/api/v1/workflows?excludePinnedData=true&limit=100", headers=headers)
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
            return None
        
        print(f"Toplam {len(workflows)} workflow bulundu:\n")
        for idx, workflow in enumerate(workflows, 1):
            # Tip kontrolü ekle
            if isinstance(workflow, dict):
                active_status = "[Aktif]" if workflow.get("active", False) else "[Pasif]"
                print(f"{idx}. {active_status} ID: {workflow['id']} - İsim: {workflow['name']}")
            else:
                print(f"{idx}. Geçersiz workflow verisi: {workflow}")
        
        return workflows
    
    except requests.exceptions.RequestException as e:
        print(f"Workflow'ları getirirken hata oluştu: {str(e)}")
        return None

def activate_workflow():
    """ID ile workflow'u aktif et"""
    workflows = get_workflows_list()
    
    if not workflows:
        return
    
    while True:
        try:
            choice = input("\nAktif etmek istediğiniz workflow'un numarasını girin (0 iptal): ")
            if choice == "0":
                return
            
            choice = int(choice)
            if choice < 1 or choice > len(workflows):
                print("Geçersiz seçim. Lütfen listeden geçerli bir numara seçin.")
                continue
            
            workflow_id = workflows[choice-1]["id"]
            workflow_name = workflows[choice-1]["name"]
            
            # Halihazırda aktif mi kontrol et
            if workflows[choice-1].get("active", False):
                print(f"\nUyarı: '{workflow_name}' workflow'u zaten aktif durumda.")
                while True:
                    confirm = input("Yine de devam etmek istiyor musunuz? (e/h): ")
                    if confirm.lower() == 'e':
                        break
                    elif confirm.lower() == 'h':
                        return
                    else:
                        print("Geçersiz giriş. Lütfen 'e' veya 'h' girin.")
            
            print(f"\nWorkflow ID: {workflow_id} '{workflow_name}' aktif ediliyor...")
            # Use POST method with an empty string as the data parameter, matching the curl example
            response = requests.post(
                f"{N8N_URL}/api/v1/workflows/{workflow_id}/activate",
                headers=headers,
                data=""  # Empty string as data
            )
            response.raise_for_status()
            
            print(f"\nWorkflow '{workflow_name}' başarıyla aktif edildi!")
            break
        
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
            
            print(f"Workflow aktif edilirken hata oluştu: {error_detail}")
            break

def deactivate_workflow():
    """ID ile workflow'u pasif et"""
    workflows = get_workflows_list()
    
    if not workflows:
        return
    
    while True:
        try:
            choice = input("\nPasif etmek istediğiniz workflow'un numarasını girin (0 iptal): ")
            if choice == "0":
                return
            
            choice = int(choice)
            if choice < 1 or choice > len(workflows):
                print("Geçersiz seçim. Lütfen listeden geçerli bir numara seçin.")
                continue
            
            workflow_id = workflows[choice-1]["id"]
            workflow_name = workflows[choice-1]["name"]
            
            # Halihazırda pasif mi kontrol et
            if not workflows[choice-1].get("active", False):
                print(f"\nUyarı: '{workflow_name}' workflow'u zaten pasif durumda.")
                while True:
                    confirm = input("Yine de devam etmek istiyor musunuz? (e/h): ")
                    if confirm.lower() == 'e':
                        break
                    elif confirm.lower() == 'h':
                        return
                    else:
                        print("Geçersiz giriş. Lütfen 'e' veya 'h' girin.")
            
            print(f"\nWorkflow ID: {workflow_id} '{workflow_name}' pasif ediliyor...")
            # Use POST method with an empty string as the data parameter, matching the curl example
            response = requests.post(
                f"{N8N_URL}/api/v1/workflows/{workflow_id}/deactivate",
                headers=headers,
                data=""  # Empty string as data
            )
            response.raise_for_status()
            
            print(f"\nWorkflow '{workflow_name}' başarıyla pasif edildi!")
            break
        
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
            
            print(f"Workflow pasif edilirken hata oluştu: {error_detail}")
            break
