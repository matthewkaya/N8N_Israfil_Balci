# N8N API CLI

N8n API ile etkileşim için geliştirilmiş Python tabanlı terminal uygulaması.

## Özellikler

Bu terminal tabanlı uygulama şunları yapmanıza olanak tanır:

1. Tüm workflow'ları listele (ID ve isim)
2. Workflow detayını ID ile getir ve JSON olarak kaydet
3. Yeni workflow oluştur
4. Var olan workflow'u güncelle
5. Workflow sil (ID ile)
6. Workflow'u aktif et
7. Workflow'u pasif yap
8. Workflow'un mevcut etiketlerini getir
9. Workflow'a etiket ata (tag ID ile)
10. Workflow'tan etiket kaldır

## Kurulum

1. Bu depoyu klonlayın
2. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```
3. `.env.sample` dosyasını `.env` olarak kopyalayın ve n8n API bilgilerinizi güncelleyin:
   ```
   cp .env.sample .env
   # Ardından .env dosyasını gerçek kimlik bilgilerinizle düzenleyin
   ```

## Kullanım

Scripti çalıştırın:
```
python n8nApp.py
```

Veya çalıştırılabilir yapıp doğrudan çalıştırın:
```
chmod +x n8nApp.py
./n8nApp.py
```

## Proje Yapısı

```
N8nApp/
├── n8nApp.py          # Ana uygulama
├── .env               # API kimlik bilgileri (gizli, gite gönderilmez)
├── .env.sample        # Örnek API kimlik bilgileri şablonu
├── requirements.txt   # Bağımlılıklar
└── functions/         # İşlevsel modüller
    ├── __init__.py
    ├── activate_workflow.py
    ├── create_workflow.py
    ├── delete_workflow.py
    ├── get_workflow_details.py
    ├── list_workflows.py
    ├── menu.py
    ├── update_workflow.py
    ├── utils.py
    └── workflow_tags.py
```