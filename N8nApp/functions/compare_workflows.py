#!/usr/bin/env python3
"""
Workflow dosyalarını N8N API'deki karşılıklarıyla karşılaştırma işlevleri
"""

import os
import json
import requests
from .utils import N8N_URL, headers, headers_with_content_type
from .upload_workflow import update_workflow, get_workflow_files, read_workflow_json

def get_all_workflows_from_api():
    """N8N API'dan tüm workflow'ları alır"""
    try:
        print("\nN8N API'dan workflow'lar alınıyor...")
        response = requests.get(f"{N8N_URL}/api/v1/workflows", headers=headers)
        response.raise_for_status()
        
        data = response.json()
        # Ensure we're getting the data in the right format - API may return data in a nested structure
        workflows = data if isinstance(data, list) else data.get("data", [])
        
        if not workflows:
            print("N8N'de hiç workflow bulunamadı.")
            return []
            
        print(f"N8N'de toplam {len(workflows)} workflow bulundu.")
        return workflows
    
    except requests.exceptions.RequestException as e:
        error_detail = str(e)
        try:
            if hasattr(e, 'response') and e.response is not None:
                error_json = e.response.json()
                if 'message' in error_json:
                    error_detail = error_json['message']
        except:
            pass
        
        print(f"N8N API'dan workflow'lar alınırken hata oluştu: {error_detail}")
        return []

def save_workflow_to_file(workflow_data, workflow_dir, original_file_path=None):
    """Workflow verisini dosyaya kaydeder"""
    if not workflow_data or "id" not in workflow_data or "name" not in workflow_data:
        print("Geçersiz workflow verisi.")
        return False
    
    # Dosya adını oluştur (ad_id.json formatında)
    safe_name = workflow_data["name"].lower().replace(" ", "_")
    new_file_name = f"{safe_name}_{workflow_data['id']}.json"
    new_file_path = os.path.join(workflow_dir, new_file_name)
    
    # Eğer orijinal dosya yolu verilmişse ve yeni dosya adı farklıysa
    if original_file_path and os.path.exists(original_file_path):
        original_file_name = os.path.basename(original_file_path)
        
        # Yeni dosya adı farklıysa yedekleme seçeneği sun
        if original_file_name != new_file_name:
            print(f"\n  ⚠️  Dikkat: Yeni dosya adı farklı olacak: {new_file_name}")
            while True:
                backup = input("  Orijinal dosyayı yedeklemek istiyor musunuz? (e/h): ").lower()
                if backup == 'e':
                    # Orijinal dosyayı .bck uzantısıyla yedekle
                    backup_path = f"{original_file_path}.bck"
                    try:
                        import shutil
                        shutil.copy2(original_file_path, backup_path)
                        print(f"  ✓ Orijinal dosya yedeklendi: {backup_path}")
                    except Exception as e:
                        print(f"  ❌ Dosya yedeklenirken hata oluştu: {str(e)}")
                    break
                elif backup == 'h':
                    try:
                        # Orijinal dosyayı sil
                        os.remove(original_file_path)
                        print(f"  ✓ Orijinal dosya silindi: {original_file_name}")
                    except Exception as e:
                        print(f"  ❌ Dosya silinirken hata oluştu: {str(e)}")
                    break
                else:
                    print("  ❌ Geçersiz giriş. Lütfen 'e' veya 'h' girin.")
    
    try:
        with open(new_file_path, 'w', encoding='utf-8') as f:
            json.dump(workflow_data, f, indent=2)
        print(f"Workflow başarıyla kaydedildi: {new_file_name}")
        return True
    except Exception as e:
        print(f"Workflow kaydedilirken hata oluştu: {str(e)}")
        return False

def are_workflows_equal(workflow1, workflow2):
    """İki workflow arasındaki temel farklılıkları kontrol eder"""
    # Bu fonksiyon kapsamlı bir karşılaştırma yapar
    # 1. Sadece önemli alanları karşılaştırır
    # 2. Karşılaştırma yaparken ayrıntılı inceleme yapar
    
    # Workflow güncelleme için gerekli alanları karşılaştır
    
    # İsim kontrolü
    if workflow1.get("name") != workflow2.get("name"):
        print(f"İsimler farklı: '{workflow1.get('name')}' != '{workflow2.get('name')}'")
        return False
    
    # Nodes kontrolü - sadece kritik özellikleri karşılaştır
    nodes1 = workflow1.get("nodes", [])
    nodes2 = workflow2.get("nodes", [])
    
    if len(nodes1) != len(nodes2):
        print(f"Node sayıları farklı: {len(nodes1)} != {len(nodes2)}")
        return False
    
    # Node'lar için kapsamlı karşılaştırma
    # Önce node1'leri id'lerine göre bir sözlüğe ekle
    nodes1_dict = {node.get("id"): node for node in nodes1}
    nodes2_dict = {node.get("id"): node for node in nodes2}
    
    # Her bir node'un kritik özelliklerini karşılaştır
    for node_id, node1 in nodes1_dict.items():
        if node_id not in nodes2_dict:
            print(f"Node ID '{node_id}' bir workflow'da var diğerinde yok")
            return False
        
        node2 = nodes2_dict[node_id]
        
        # Kritik özellikler
        critical_props = ["name", "type", "typeVersion", "position", "parameters"]
        
        for prop in critical_props:
            if prop == "parameters":
                # Parameters karşılaştırması için recursive yapı gerekebilir
                # Basit bir şekilde JSON string olarak karşılaştıralım
                try:
                    params1_str = json.dumps(node1.get(prop, {}), sort_keys=True)
                    params2_str = json.dumps(node2.get(prop, {}), sort_keys=True)
                    if params1_str != params2_str:
                        print(f"Node '{node_id}' parameters farklı")
                        return False
                except:
                    # JSON dönüşümü başarısız olursa farklı kabul et
                    print(f"Node '{node_id}' parameters karşılaştırma hatası")
                    return False
            elif node1.get(prop) != node2.get(prop):
                print(f"Node '{node_id}' için '{prop}' değeri farklı")
                return False
    
    # Connections kontrolü
    connections1 = workflow1.get("connections", {})
    connections2 = workflow2.get("connections", {})
    
    try:
        connections1_str = json.dumps(connections1, sort_keys=True)
        connections2_str = json.dumps(connections2, sort_keys=True)
        if connections1_str != connections2_str:
            print("Connections yapısı farklı")
            return False
    except:
        # JSON dönüşümü başarısız olursa farklı kabul et
        print("Connections karşılaştırma hatası")
        return False
    
    # Settings kontrolü - sadece executionOrder'ı karşılaştır
    settings1 = workflow1.get("settings", {})
    settings2 = workflow2.get("settings", {})
    
    if settings1.get("executionOrder") != settings2.get("executionOrder"):
        print("Settings executionOrder değeri farklı")
        return False
    
    # Tüm kritik kontrolleri geçti, workflow'lar eşit kabul edilebilir
    return True

def compare_workflows():
    """N8N API'daki workflow'lar ile dosya sistemindeki workflow'ları karşılaştırır"""
    # API'den tüm workflow'ları al
    api_workflows = get_all_workflows_from_api()
    if not api_workflows:
        return
    
    # Dosya sistemindeki tüm workflow dosyalarını al
    workflow_files, workflow_dir = get_workflow_files()
    if not workflow_dir:
        return
    
    # Dosya sistemindeki workflow'ları ID'lerine göre eşleştir
    file_workflows = {}
    files_without_id = []  # ID'si olmayan dosyaları kaydet
    
    for file in workflow_files:
        file_path = os.path.join(workflow_dir, file)
        workflow_data = read_workflow_json(file_path)
        if workflow_data:
            if "id" in workflow_data:
                file_workflows[workflow_data["id"]] = {
                    "data": workflow_data,
                    "file_path": file_path,
                    "file_name": file
                }
            else:
                # ID'si olmayan dosyaları farklı bir listeye ekle
                files_without_id.append({
                    "data": workflow_data,
                    "file_path": file_path,
                    "file_name": file
                })
    
    print(f"Dosya sisteminde {len(file_workflows)} workflow dosyası bulundu.")
    
    # Karşılaştırma sonuçları
    to_update_from_file = []  # Dosya içeriği API'den farklı
    to_create_file = []       # API'de var ama dosyada yok
    to_create_api = []        # Dosyada var ama API'de yok
    matching_workflows = []   # Hem API'de hem de dosyada var ve içerikleri eşit
    
    # API workflow'larını dosya sistemindekilerle karşılaştır
    for api_wf in api_workflows:
        wf_id = api_wf.get("id")
        if not wf_id:
            continue
            
        if wf_id in file_workflows:
            # Hem API'de hem dosyada var - içerik karşılaştır
            file_wf = file_workflows[wf_id]["data"]
            if are_workflows_equal(api_wf, file_wf):
                # İçerik eşit - eşleşen workflow
                matching_workflows.append({
                    "api": api_wf,
                    "file": file_workflows[wf_id]
                })
            else:
                # İçerik farklı - güncelleme gerekiyor
                to_update_from_file.append({
                    "api": api_wf,
                    "file": file_workflows[wf_id]
                })
        else:
            # Sadece API'de var - dosya oluşturulmalı
            to_create_file.append(api_wf)
    
    # Dosya sistemindeki workflow'ları API'dekilerle karşılaştır
    api_workflow_ids = [wf.get("id") for wf in api_workflows if wf.get("id")]
    
    # ID'si olan workflow'ları kontrol et
    for file_id, file_wf in file_workflows.items():
        if file_id not in api_workflow_ids:
            # Sadece dosyada var - API'ye yüklenmeli
            to_create_api.append(file_wf)
    
    # ID'si olmayan workflow dosyalarını da ekle
    for file_wf in files_without_id:
        # ID olmayan her dosyayı yeni workflow kabul et
        to_create_api.append(file_wf)
    
    # Sonuçları tablo şeklinde göster - Daha düzenli bir formatta
    print("\n")
    
    # Tablo başlığı
    print("╔════════════════════════════════╦═══════════════════════════╦═══════════════════════════════╦═════════════════╗")
    print("║ Dosya Adı                      ║ Workflow ID               ║ WorkFlow İsmi                 ║ Durum           ║")
    print("╠════════════════════════════════╬═══════════════════════════╬═══════════════════════════════╬═════════════════╣")
    
    # 1. Eşleşen workflow'ları göster
    for item in matching_workflows:
        api_wf = item["api"]
        file_name = item["file"]["file_name"]
        # Uzun isim ve ID'leri kısalt
        file_name_short = file_name[:26] if len(file_name) > 26 else file_name
        wf_id_short = api_wf['id'][:23] if len(api_wf['id']) > 23 else api_wf['id']
        wf_name_short = api_wf['name'][:27] if len(api_wf['name']) > 27 else api_wf['name']
        
        print(f"║ {file_name_short:<28} ║ {wf_id_short:<25} ║ {wf_name_short:<29} ║ EŞLEŞİYOR       ║")
    
    # 2. Farklı olan workflow'ları göster
    for item in to_update_from_file:
        api_wf = item["api"]
        file_name = item["file"]["file_name"]
        # Uzun isim ve ID'leri kısalt
        file_name_short = file_name[:26] if len(file_name) > 26 else file_name
        wf_id_short = api_wf['id'][:23] if len(api_wf['id']) > 23 else api_wf['id']
        wf_name_short = api_wf['name'][:27] if len(api_wf['name']) > 27 else api_wf['name']
        
        print(f"║ {file_name_short:<28} ║ {wf_id_short:<25} ║ {wf_name_short:<29} ║ FARKLI         ║")
    
    # 3. Sadece API'de olan workflow'ları göster
    for wf in to_create_file:
        wf_id_short = wf['id'][:23] if len(wf['id']) > 23 else wf['id']
        wf_name_short = wf['name'][:27] if len(wf['name']) > 27 else wf['name']
        
        print(f"║ {'---':<28} ║ {wf_id_short:<25} ║ {wf_name_short:<29} ║ SADECE API     ║")
    
    # 4. Sadece dosyada olan workflow'ları göster
    for item in to_create_api:
        wf = item["data"]
        file_name = item["file_name"]
        # Uzun isim ve ID'leri kısalt
        file_name_short = file_name[:26] if len(file_name) > 26 else file_name
        wf_name_short = wf['name'][:27] if len(wf['name']) > 27 else wf['name']
        
        print(f"║ {file_name_short:<28} ║ {'---':<25} ║ {wf_name_short:<29} ║ SADECE DOSYA   ║")
    
    # Tablo alt çizgisi
    print("╚════════════════════════════════╩═══════════════════════════╩═══════════════════════════════╩═════════════════╝")
    
    # Özet bilgisi - Güzel bir kutu içinde
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║                      ÖZET BİLGİSİ                         ║")
    print("╠══════════════════════════════════╦═════════════════════════╣")
    print(f"║  Eşleşen workflow sayısı:        ║ {len(matching_workflows):<23} ║")
    print(f"║  Farklı workflow sayısı:         ║ {len(to_update_from_file):<23} ║")
    print(f"║  Sadece API'de olan sayısı:      ║ {len(to_create_file):<23} ║")
    print(f"║  Sadece dosyada olan sayısı:     ║ {len(to_create_api):<23} ║")
    print("╚══════════════════════════════════╩═════════════════════════╝")
    
    # Hiç değişiklik gerektiren workflow yoksa bilgilendirme mesajı göster
    if not to_update_from_file and not to_create_file and not to_create_api:
        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║            TÜM WORKFLOW'LAR SENKRON DURUMDA!             ║")
        print("╚════════════════════════════════════════════════════════════╝")
        return
    
    # Kullanıcıya güncelleme yapmak isteyip istemediğini sor
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║                   İŞLEM SEÇENEKLERİ                       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    while True:
        choice = input("\nGüncelleme yapmak istiyor musunuz? (e/h): ")
        if choice.lower() == 'h':
            return
        elif choice.lower() == 'e':
            break
        else:
            print("❌ Geçersiz giriş. Lütfen 'e' veya 'h' girin.")
    
    # Güncelleme işlemlerini gerçekleştir
    update_count = 0
    
    # 1. API ve dosya içeriği farklı olan workflow'ları güncelle
    if to_update_from_file:
        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║             FARKLI İÇERİKLİ WORKFLOW'LAR                 ║")
        print("╚════════════════════════════════════════════════════════════╝")
        
        for i, item in enumerate(to_update_from_file, 1):
            print(f"{i}. '{item['api']['name']}' (ID: {item['api']['id']})")
        
        for item in to_update_from_file:
            api_wf = item["api"]
            file_wf = item["file"]["data"]
            file_path = item["file"]["file_path"]
            file_name = item["file"]["file_name"]
            
            print(f"\n➤ '{api_wf['name']}' (ID: {api_wf['id']}) workflow'u için:")
            
            while True:
                source = input("  Hangi kaynağı kullanmak istiyorsunuz? (dosya/n8n): ").lower()
                if source == 'dosya':
                    # API'deki workflow'u yedeklemek isteyip istemediğini sor
                    backup_choice = input("  API'deki mevcut workflow'u yedeklemek istiyor musunuz? (e/h): ").lower()
                    backup_api = backup_choice == 'e'
                    
                    print(f"  ⟳ Dosya içeriği N8N'e yükleniyor: {file_name}")
                    if update_workflow(api_wf["id"], file_wf, backup_api_workflow=backup_api):
                        print("  ✓ Başarıyla güncellendi!")
                        update_count += 1
                    break
                elif source == 'n8n':
                    print(f"  ⟳ N8N içeriği dosyaya kaydediliyor: {file_path}")
                    if save_workflow_to_file(api_wf, workflow_dir, original_file_path=file_path):
                        print("  ✓ Başarıyla güncellendi!")
                        update_count += 1
                    break
                else:
                    print("  ❌ Geçersiz giriş. Lütfen 'dosya' veya 'n8n' girin.")
    
    # 2. Sadece API'de olan workflow'lar için dosya oluştur
    if to_create_file:
        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║             SADECE API'DE OLAN WORKFLOW'LAR               ║")
        print("╚════════════════════════════════════════════════════════════╝")
        
        for i, wf in enumerate(to_create_file, 1):
            print(f"{i}. '{wf['name']}' (ID: {wf['id']})")
        
        while True:
            create_files = input("\nBu workflow'lar için dosya oluşturmak istiyor musunuz? (e/h): ")
            if create_files.lower() == 'e':
                for wf in to_create_file:
                    print(f"  ⟳ Workflow dosyası oluşturuluyor: {wf['name']}")
                    if save_workflow_to_file(wf, workflow_dir):
                        print("  ✓ Başarıyla kaydedildi!")
                        update_count += 1
                break
            elif create_files.lower() == 'h':
                break
            else:
                print("  ❌ Geçersiz giriş. Lütfen 'e' veya 'h' girin.")
    
    # 3. Sadece dosyada olan workflow'ları API'ye yükle
    if to_create_api:
        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║            SADECE DOSYADA OLAN WORKFLOW'LAR               ║")
        print("╚════════════════════════════════════════════════════════════╝")
        
        for i, item in enumerate(to_create_api, 1):
            wf = item["data"]
            wf_name = wf.get("name", "İsimsiz Workflow")
            print(f"{i}. '{wf_name}' (ID: {wf.get('id', 'Belirtilmemiş')})")
        
        while True:
            upload_files = input("\nBu workflow'ları N8N'e yüklemek istiyor musunuz? (e/h): ")
            if upload_files.lower() == 'e':
                for item in to_create_api:
                    wf = item["data"]
                    wf_name = wf.get("name", "İsimsiz Workflow")
                    
                    if "id" in wf and wf["id"]:
                        wf_id = wf["id"]
                        # API'deki workflow'u yedeklemek isteyip istemediğini sor
                        backup_choice = input(f"  '{wf_name}' workflow'u için API'deki mevcut halini yedeklemek istiyor musunuz? (e/h): ").lower()
                        backup_api = backup_choice == 'e'
                        
                        print(f"  ⟳ '{wf_name}' (ID: {wf_id}) workflow'u N8N'e yükleniyor...")
                        if update_workflow(wf_id, wf, backup_api_workflow=backup_api):
                            print("  ✓ Başarıyla yüklendi!")
                            update_count += 1
                    else:
                        # ID yoksa veya boşsa yeni workflow oluştur
                        print(f"  ⟳ '{wf_name}' için yeni bir workflow oluşturuluyor...")
                        from .upload_workflow import create_new_workflow
                        file_path = item.get("file_path")
                        if create_new_workflow(wf_name, wf, file_path):
                            print("  ✓ Yeni workflow başarıyla oluşturuldu ve dosya güncellendi!")
                            update_count += 1
                break
            elif upload_files.lower() == 'h':
                break
            else:
                print("  ❌ Geçersiz giriş. Lütfen 'e' veya 'h' girin.")
    
    # Özet sonuç bilgisi
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║                     İŞLEM SONUCU                          ║")
    print("╠══════════════════════════════════════════╦═════════════════╣")
    print(f"║  Toplam güncellenen workflow sayısı:     ║ {update_count:<15} ║")
    print("╚══════════════════════════════════════════╩═════════════════╝")