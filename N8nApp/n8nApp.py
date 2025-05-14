#!/usr/bin/env python3
"""
N8N API CLI - N8n API ile etkileşim için terminal tabanlı uygulama
"""

# Gerekli modülleri içe aktar
from functions.menu import display_menu
from functions.list_workflows import list_workflows
from functions.get_workflow_details import get_workflow_details
from functions.create_workflow import create_workflow
from functions.update_workflow import update_workflow
from functions.delete_workflow import delete_workflow
from functions.activate_workflow import activate_workflow, deactivate_workflow
from functions.upload_workflow import upload_all_workflows, upload_selected_workflow
from functions.compare_workflows import compare_workflows

def main():
    """Ana uygulama döngüsü"""
    while True:
        display_menu()
        
        try:
            choice = input("\nBir seçenek seçin (0-10): ")
            
            if choice == "1":
                list_workflows()
            elif choice == "2":
                get_workflow_details()
            elif choice == "3":
                create_workflow()
            elif choice == "4":
                update_workflow()
            elif choice == "5":
                delete_workflow()
            elif choice == "6":
                activate_workflow()
            elif choice == "7":
                deactivate_workflow()
            elif choice == "8":
                upload_all_workflows()
            elif choice == "9":
                upload_selected_workflow()
            elif choice == "10":
                compare_workflows()
            elif choice == "0":
                print("\nN8N API CLI'dan çıkılıyor. Hoşça kalın!")
                break
            else:
                print("\nGeçersiz seçenek. Lütfen tekrar deneyin.")
            
            input("\nDevam etmek için Enter tuşuna basın...")
        
        except KeyboardInterrupt:
            print("\n\nİşlem iptal edildi. Menüye dönülüyor.")
            continue

if __name__ == "__main__":
    main()
