#!/usr/bin/env python3
"""
Workflow listeleme işlevleri
"""

import os
import json
import subprocess
import requests
from functions.utils import N8N_URL, headers

def list_workflows():
    """Tüm workflow'ları ID ve isimleriyle listeler"""
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
            return
        
        print(f"Toplam {len(workflows)} workflow bulundu:\n")
        for idx, workflow in enumerate(workflows, 1):
            # Tip kontrolü ekle
            if isinstance(workflow, dict):
                active_status = "[Aktif]" if workflow.get("active", False) else "[Pasif]"
                print(f"{idx}. {active_status} ID: {workflow['id']} - İsim: {workflow['name']}")
            else:
                print(f"{idx}. Geçersiz workflow verisi: {workflow}")
        
        # Kullanıcıya workflow'ları kaydetme seçeneği sun - Geçerli giriş için while döngüsü ekle
        while True:
            save_option = input("\nTüm workflow'ları ayrı dosyalar halinde kaydetmek ister misiniz? (e/h): ")
            
            if save_option.lower() == 'e':
                # workflows dizinini oluştur (eğer yoksa)
                # Proje kök dizinini al ve tam yolu oluştur
                base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
                workflows_dir = os.path.join(base_dir, "workflows")
                if not os.path.exists(workflows_dir):
                    os.makedirs(workflows_dir)
                print(f"Dosyalar {workflows_dir} klasörüne kaydedilecek...")
                
                # Her workflow için detaylı bilgileri al ve dosyaya kaydet
                for workflow in workflows:
                    if isinstance(workflow, dict):
                        workflow_id = workflow['id']
                        workflow_name = workflow['name'].replace(" ", "_").lower()
                        
                        # Workflow dosya adını oluştur (tam yolları kullanarak)
                        filename = os.path.join(workflows_dir, f"{workflow_name}_{workflow_id}.json")
                        
                        # Dosyanın var olup olmadığını kontrol et - Geçerli giriş için while döngüsü ekle
                        if os.path.exists(filename):
                            while True:
                                overwrite = input(f"'{filename}' dosyası zaten var. Üzerine yazılsın mı? (e/h): ")
                                if overwrite.lower() == 'e' or overwrite.lower() == 'h':
                                    break
                                print("Lütfen 'e' veya 'h' girin.")
                                
                            if overwrite.lower() != 'e':
                                print(f"'{filename}' dosyası atlandı.")
                                continue
                            
                            # Git add komutunu çalıştır
                            try:
                                subprocess.run(['git', 'add', '.'], check=True)
                                print("Mevcut dosyalar git staging'e eklendi.")
                            except subprocess.SubprocessError as e:
                                print(f"Git komutu çalıştırılırken hata oluştu: {str(e)}")
                        
                        # Tam workflow detaylarını kullan (zaten elimizdeki JSON'da tüm detaylar var)
                        try:
                            # Dosyaya kaydet
                            with open(filename, 'w', encoding='utf-8') as file:
                                json.dump(workflow, file, indent=2, ensure_ascii=False)
                            
                            print(f"Workflow '{workflow_name}' başarıyla kaydedildi: {filename}")
                        
                        except Exception as e:
                            print(f"Workflow {workflow_id} kaydedilirken hata oluştu: {str(e)}")
                
                print("\nTüm seçilen workflow'lar kaydedildi.")
                break
            elif save_option.lower() == 'h':
                print("\nWorkflow'lar kaydedilmedi. Ana menüye dönülüyor.")
                break
            else:
                print("Geçersiz giriş! Lütfen 'e' veya 'h' girin.")
        
        # Olası ileri kullanım için workflow'ları döndür
        return workflows
    
    except requests.exceptions.RequestException as e:
        print(f"Workflow'ları getirirken hata oluştu: {str(e)}")
        return None
