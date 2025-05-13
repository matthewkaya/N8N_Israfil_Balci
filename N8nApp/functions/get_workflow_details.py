#!/usr/bin/env python3
"""
Workflow detayı getirme işlevleri
"""

import json
import requests
from datetime import datetime
from functions.utils import N8N_URL, headers
from functions.list_workflows import list_workflows

def get_workflow_details():
    """ID ile workflow detayını getir ve JSON olarak kaydet"""
    workflows = list_workflows()
    
    if not workflows:
        return
    
    try:
        choice = int(input("\nDetayını görmek istediğiniz workflow'un numarasını girin (0 iptal): "))
        if choice == 0:
            return
        
        if choice < 1 or choice > len(workflows):
            print("Geçersiz seçim.")
            return
        
        workflow_id = workflows[choice-1]["id"]
        
        print(f"\nWorkflow ID: {workflow_id} için detaylar getiriliyor...")
        response = requests.get(
            f"{N8N_URL}/api/v1/workflows/{workflow_id}?excludePinnedData=true",
            headers=headers
        )
        response.raise_for_status()
        
        workflow = response.json()
        
        # Workflow adı ve zaman damgası kullanarak dosya adı oluştur
        sanitized_name = workflow["name"].replace(" ", "_").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"workflow_{sanitized_name}_{workflow_id}_{timestamp}.json"
        
        # Workflow'u dosyaya kaydet
        with open(filename, 'w') as file:
            json.dump(workflow, file, indent=2)
        
        print(f"\nWorkflow detayları şuraya kaydedildi: {filename}")
    
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
    except requests.exceptions.RequestException as e:
        print(f"Workflow detaylarını getirirken hata oluştu: {str(e)}")
