#!/usr/bin/env python3
"""
Workflow detayı getirme işlevleri
"""

import json
import os
import requests
import subprocess
from datetime import datetime

def get_workflow_details():
    """ID ile workflow detayını getir ve JSON olarak kaydet"""
    # list_workflows fonksiyonunu çağırırken, dönüş değerini kullanma
    # sadece kullanıcıya workflow listesini göster
    from functions.list_workflows import list_workflows
    from functions.utils import N8N_URL, headers
    
    print("\nWorkflow'lar getiriliyor...\n")
    
    try:
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
            return
        
        print(f"Toplam {len(workflows)} workflow bulundu:\n")
        for idx, workflow in enumerate(workflows, 1):
            # Tip kontrolü ekle
            if isinstance(workflow, dict):
                active_status = "[Aktif]" if workflow.get("active", False) else "[Pasif]"
                print(f"{idx}. {active_status} ID: {workflow['id']} - İsim: {workflow['name']}")
            else:
                print(f"{idx}. Geçersiz workflow verisi: {workflow}")
    
    except requests.exceptions.RequestException as e:
        print(f"Workflow'ları getirirken hata oluştu: {str(e)}")
        return
    
    try:
        choice = int(input("\nDetayını görmek istediğiniz workflow'un numarasını girin (0 iptal): "))
        if choice == 0:
            return
        
        if choice < 1 or choice > len(workflows):
            print("Geçersiz seçim.")
            return
        
        selected_workflow = workflows[choice-1]
        workflow_id = selected_workflow["id"]
        workflow_name = selected_workflow["name"].replace(" ", "_").lower()
        
        print(f"\nWorkflow ID: {workflow_id} için detaylar getiriliyor...")
        response = requests.get(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}?excludePinnedData=true",
            headers=headers
        )
        response.raise_for_status()
        
        workflow = response.json()
        
        # Proje kök dizinini al ve workflows klasörünün tam yolunu oluştur
        base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        workflows_dir = os.path.join(base_dir, "workflows")
        
        # workflows klasörünü oluştur (eğer yoksa)
        if not os.path.exists(workflows_dir):
            os.makedirs(workflows_dir)
            print(f"'{workflows_dir}' klasörü oluşturuldu.")
        
        # İndirilen workflow için standart isimlendirme kullan (list_workflows.py ile aynı format)
        filename = f"{workflow_name}_{workflow_id}.json"
        file_path = os.path.join(workflows_dir, filename)
        
        # Dosyanın var olup olmadığını kontrol et
        if os.path.exists(file_path):
            while True:
                overwrite = input(f"'{file_path}' dosyası zaten var. Silmek ister misiniz? (e/h): ")
                if overwrite.lower() in ['e', 'h']:
                    break
                print("Geçersiz giriş! Lütfen 'e' veya 'h' girin.")
            
            if overwrite.lower() != 'e':
                print("İşlem iptal edildi.")
                return
            
            # Versiyonlama seçeneği sor
            while True:
                version = input(f"Mevcut dosyayı versiyonlamak ister misiniz? (e/h): ")
                if version.lower() in ['e', 'h']:
                    break
                print("Geçersiz giriş! Lütfen 'e' veya 'h' girin.")
                
            if version.lower() == 'e':
                try:
                    # Dosyayı git staging'e ekle
                    subprocess.run(['git', 'add', file_path], check=True)
                    print(f"Mevcut dosya git staging'e eklendi: {file_path}")
                except subprocess.SubprocessError as e:
                    print(f"Git komutu çalıştırılırken hata oluştu: {str(e)}")
            
            # Eski dosyayı sil
            os.remove(file_path)
            print(f"Eski dosya silindi: {file_path}")
        
        # Yeni dosyayı oluştur ve kaydet
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(workflow, file, indent=2, ensure_ascii=False)
        
        print(f"\nWorkflow detayları başarıyla kaydedildi: {file_path}")
    
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    except requests.exceptions.RequestException as e:
        print(f"Workflow detaylarını getirirken hata oluştu: {str(e)}")
