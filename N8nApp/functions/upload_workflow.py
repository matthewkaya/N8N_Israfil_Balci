#!/usr/bin/env python3
"""
Workflow yükleme işlevleri
"""

import os
import json
import requests
import datetime
from .utils import N8N_URL, headers, headers_with_content_type

def get_workflow_files():
    """Workflow dizinindeki tüm JSON dosyalarını listeler"""
    workflow_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "workflows")
    if not os.path.exists(workflow_dir):
        print("\nWorkflow dizini bulunamadı.")
        return []
    
    workflow_files = [f for f in os.listdir(workflow_dir) if f.endswith('.json')]
    return workflow_files, workflow_dir

def read_workflow_json(file_path):
    """JSON dosyasını okur ve içeriğini döndürür"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"\n{os.path.basename(file_path)} geçersiz JSON formatında.")
        return None
    except Exception as e:
        print(f"\n{os.path.basename(file_path)} okunurken hata oluştu: {str(e)}")
        return None

def create_new_workflow(workflow_name, workflow_data, file_path=None):
    """Yeni bir workflow oluşturur"""
    # Gerekli alanları hazırla
    if "nodes" not in workflow_data:
        print("Workflow verisi geçersiz, 'nodes' bulunamadı.")
        return False
    
    # Sadece temel alanları al
    allowed_data = {
        "name": workflow_name,
        "nodes": workflow_data["nodes"],
        "connections": workflow_data.get("connections", {}),
        "settings": {"executionOrder": "v1"},
        "staticData": {}
    }
    
    try:
        # API isteği gönder
        print(f"\nWorkflow oluşturuluyor: {workflow_name}")
        response = requests.post(
            f"{N8N_URL}/api/v1/workflows",
            headers=headers_with_content_type,
            json=allowed_data
        )
        response.raise_for_status()
        result = response.json()
        new_id = result.get('id')
        print(f"\nYeni workflow başarıyla oluşturuldu. ID: {new_id}")
        
        # Eğer dosya yolu verildiyse, dosyayı ID ile güncelle
        if file_path and new_id:
            # Dosyayı okuyalım
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                
                # ID'yi ekleyelim
                file_data["id"] = new_id
                
                # Güncellenmiş dosyayı geri yazalım
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(file_data, f, indent=2)
                print(f"Workflow dosyası ID ile güncellendi: {file_path}")
            except Exception as e:
                print(f"Dosya güncellenirken hata oluştu: {str(e)}")
        
        return True
    except requests.exceptions.RequestException as e:
        error_detail = str(e)
        try:
            if hasattr(e, 'response') and e.response is not None:
                error_json = e.response.json()
                if 'message' in error_json:
                    error_detail = error_json['message']
        except:
            pass
        
        print(f"\nWorkflow oluşturulurken hata oluştu: {error_detail}")
        return False

def update_workflow(workflow_id, workflow_data, backup_api_workflow=False):
    """Mevcut bir workflow'u günceller"""
    try:
        # API'deki mevcut workflow'u yedeklemek için isteğe bağlı olarak önce alalım
        if backup_api_workflow:
            try:
                # Mevcut workflow'u getir
                backup_response = requests.get(
                    f"{N8N_URL}/api/v1/workflows/{workflow_id}",
                    headers=headers
                )
                backup_response.raise_for_status()
                backup_workflow = backup_response.json()
                
                # Workflow'u yedekle - otomatik oluşturulan bir dosya adıyla
                backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backups")
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                    
                backup_name = backup_workflow.get("name", "unknown").lower().replace(" ", "_")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"{backup_name}_{backup_workflow.get('id')}_{timestamp}.json"
                backup_path = os.path.join(backup_dir, backup_file)
                
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(backup_workflow, f, indent=2)
                print(f"  ✓ API workflow yedeklendi: {backup_file}")
                
            except Exception as e:
                print(f"  ⚠️ API workflow yedeklenirken hata oluştu: {str(e)}")
        
        # Sadece temel alanları al
        allowed_data = {
            "name": workflow_data.get("name", ""),
            "nodes": workflow_data.get("nodes", []),
            "connections": workflow_data.get("connections", {}),
            "settings": {"executionOrder": "v1"},
            "staticData": {}
        }
        
        # API isteği gönder
        print(f"\nWorkflow güncelleniyor: ID {workflow_id}")
        response = requests.put(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            headers=headers_with_content_type,
            json=allowed_data
        )
        response.raise_for_status()
        print(f"\nWorkflow ID: {workflow_id} başarıyla güncellendi!")
        return True
    except requests.exceptions.RequestException as e:
        error_detail = str(e)
        try:
            if hasattr(e, 'response') and e.response is not None:
                error_json = e.response.json()
                if 'message' in error_json:
                    error_detail = error_json['message']
        except:
            pass
        
        print(f"\nWorkflow güncellenirken hata oluştu: {error_detail}")
        return False

def upload_all_workflows():
    """Tüm workflow dosyalarını N8N'e yükler"""
    workflow_files, workflow_dir = get_workflow_files()
    
    if not workflow_files:
        print("\nYüklenecek workflow dosyası bulunamadı.")
        return
    
    print(f"\nToplam {len(workflow_files)} workflow dosyası bulundu:")
    for idx, file in enumerate(workflow_files, 1):
        print(f"{idx}. {file}")
    
    # Kullanıcıya emin olup olmadığını sor
    while True:
        confirm = input("\nTüm workflow dosyalarını N8N'e yüklemek istediğinize emin misiniz? (e/h): ")
        if confirm.lower() == 'e':
            break
        elif confirm.lower() == 'h':
            return
        else:
            print("Geçersiz giriş. Lütfen 'e' veya 'h' girin.")
    
    success_count = 0
    fail_count = 0
    create_count = 0
    
    for file in workflow_files:
        file_path = os.path.join(workflow_dir, file)
        workflow_data = read_workflow_json(file_path)
        
        if not workflow_data:
            fail_count += 1
            continue
        
        # Workflow ID kontrol et
        if "id" in workflow_data:
            workflow_id = workflow_data["id"]
            workflow_name = workflow_data.get("name", "İsimsiz Workflow")
            print(f"\n'{workflow_name}' (ID: {workflow_id}) güncelleniyor...")
            
            if update_workflow(workflow_id, workflow_data):
                success_count += 1
            else:
                fail_count += 1
        else:
            # ID yoksa yeni workflow oluştur
            print(f"\nDosyada ({file}) workflow ID'si bulunamadı. Yeni bir workflow oluşturulması gerekiyor.")
            
            while True:
                create_new = input("Yeni bir workflow oluşturmak istiyor musunuz? (e/h): ")
                if create_new.lower() == 'e':
                    workflow_name = input("Yeni workflow için bir isim girin: ")
                    if create_new_workflow(workflow_name, workflow_data):
                        create_count += 1
                    else:
                        fail_count += 1
                    break
                elif create_new.lower() == 'h':
                    print("Bu dosya atlanıyor.")
                    break
                else:
                    print("Geçersiz giriş. Lütfen 'e' veya 'h' girin.")
    
    print(f"\nİşlem tamamlandı.")
    print(f"- {success_count} workflow güncellendi.")
    print(f"- {create_count} yeni workflow oluşturuldu.")
    print(f"- {fail_count} dosyada hata oluştu.")

def upload_selected_workflow():
    """Seçilen bir workflow dosyasını N8N'e yükler"""
    workflow_files, workflow_dir = get_workflow_files()
    
    if not workflow_files:
        print("\nYüklenecek workflow dosyası bulunamadı.")
        return
    
    print(f"\nToplam {len(workflow_files)} workflow dosyası bulundu:")
    for idx, file in enumerate(workflow_files, 1):
        print(f"{idx}. {file}")
    
    # Kullanıcıdan dosya seçmesini iste
    while True:
        try:
            choice = input("\nYüklemek istediğiniz workflow dosyasının numarasını girin (0 iptal): ")
            if choice == "0":
                return
            
            choice = int(choice)
            if 1 <= choice <= len(workflow_files):
                selected_file = workflow_files[choice-1]
                break
            else:
                print("Geçersiz seçim. Lütfen listeden bir numara seçin.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
    
    file_path = os.path.join(workflow_dir, selected_file)
    workflow_data = read_workflow_json(file_path)
    
    if not workflow_data:
        return
    
    # Workflow ID kontrol et
    if "id" in workflow_data:
        workflow_id = workflow_data["id"]
        workflow_name = workflow_data.get("name", "İsimsiz Workflow")
        
        print(f"\n'{workflow_name}' (ID: {workflow_id}) workflow'u güncellenecek.")
        
        while True:
            confirm = input("Devam etmek istiyor musunuz? (e/h): ")
            if confirm.lower() == 'e':
                update_workflow(workflow_id, workflow_data)
                break
            elif confirm.lower() == 'h':
                return
            else:
                print("Geçersiz giriş. Lütfen 'e' veya 'h' girin.")
    else:
        # ID yoksa yeni workflow oluştur
        print(f"\nDosyada ({selected_file}) workflow ID'si bulunamadı. Yeni bir workflow oluşturulması gerekiyor.")
        
        while True:
            create_new = input("Yeni bir workflow oluşturmak istiyor musunuz? (e/h): ")
            if create_new.lower() == 'e':
                workflow_name = input("Yeni workflow için bir isim girin: ")
                create_new_workflow(workflow_name, workflow_data)
                break
            elif create_new.lower() == 'h':
                return
            else:
                print("Geçersiz giriş. Lütfen 'e' veya 'h' girin.")
