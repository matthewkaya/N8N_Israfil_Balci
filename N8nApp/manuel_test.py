#!/usr/bin/env python3
"""
N8nApp fonksiyonlarını manuel olarak test eden script
"""
import os
import sys
import traceback
from pathlib import Path

# Projenin kök dizinini Python yoluna ekleyelim
try:
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    project_dir = current_dir
    sys.path.insert(0, str(project_dir))
    print(f"Proje dizini eklendi: {project_dir}")
    print(f"Python path: {sys.path}")
except Exception as e:
    print(f"Proje dizini eklenirken hata: {e}")
    traceback.print_exc()

from functions.menu import display_menu
from functions.utils import N8N_URL, API_KEY

def run_test():
    """Manuel test fonksiyonu"""
    print("N8nApp Manuel Test\n")
    
    print("1. Ortam değişkenlerini kontrol etme...")
    if not N8N_URL:
        print("  ❌ Hata: N8N_URL tanımlanmamış")
    else:
        print(f"  ✅ N8N_URL: {N8N_URL}")
        
    if not API_KEY:
        print("  ❌ Hata: API_KEY tanımlanmamış")
    else:
        print(f"  ✅ API_KEY: {'*' * min(10, len(API_KEY))}")
    
    print("\n2. Modülleri import etme testi...")
    
    try:
        print("  📦 functions.menu modülünü import etme...")
        from functions.menu import display_menu
        print("  ✅ functions.menu başarıyla import edildi")
    except Exception as e:
        print(f"  ❌ functions.menu import hatası: {e}")
        traceback.print_exc()
        
    try:
        print("  📦 functions.list_workflows modülünü import etme...")
        from functions.list_workflows import list_workflows
        print("  ✅ functions.list_workflows başarıyla import edildi")
    except Exception as e:
        print(f"  ❌ functions.list_workflows import hatası: {e}")
        traceback.print_exc()
        
    try:
        print("  📦 functions.get_workflow_details modülünü import etme...")
        from functions.get_workflow_details import get_workflow_details
        print("  ✅ functions.get_workflow_details başarıyla import edildi")
    except Exception as e:
        print(f"  ❌ functions.get_workflow_details import hatası: {e}")
        traceback.print_exc()
        
    try:
        print("  📦 functions.create_workflow modülünü import etme...")
        from functions.create_workflow import create_workflow
        print("  ✅ functions.create_workflow başarıyla import edildi")
    except Exception as e:
        print(f"  ❌ functions.create_workflow import hatası: {e}")
        traceback.print_exc()
        
    try:
        print("  📦 functions.update_workflow modülünü import etme...")
        from functions.update_workflow import update_workflow
        print("  ✅ functions.update_workflow başarıyla import edildi")
    except Exception as e:
        print(f"  ❌ functions.update_workflow import hatası: {e}")
        traceback.print_exc()
        
    try:
        print("  📦 functions.delete_workflow modülünü import etme...")
        from functions.delete_workflow import delete_workflow
        print("  ✅ functions.delete_workflow başarıyla import edildi")
    except Exception as e:
        print(f"  ❌ functions.delete_workflow import hatası: {e}")
        traceback.print_exc()
        
    try:
        print("  📦 functions.activate_workflow modülünü import etme...")
        from functions.activate_workflow import activate_workflow, deactivate_workflow
        print("  ✅ functions.activate_workflow başarıyla import edildi")
    except Exception as e:
        print(f"  ❌ functions.activate_workflow import hatası: {e}")
        traceback.print_exc()
        
    try:
        print("  📦 functions.workflow_tags modülünü import etme...")
        from functions.workflow_tags import get_workflow_tags, assign_tag, remove_tags
        print("  ✅ functions.workflow_tags başarıyla import edildi")
    except Exception as e:
        print(f"  ❌ functions.workflow_tags import hatası: {e}")
        traceback.print_exc()
    
    print("\nManuel test tamamlandı!")

if __name__ == "__main__":
    run_test()
