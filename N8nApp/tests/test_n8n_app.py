#!/usr/bin/env python3
"""
Test script for n8nApp.py functionality
"""

import unittest
import os
import sys
import io
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock

# Ana proje dizinini import path'e ekleyelim
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.menu import display_menu
from functions.list_workflows import list_workflows
from functions.get_workflow_details import get_workflow_details
from functions.create_workflow import create_workflow
from functions.update_workflow import update_workflow
from functions.delete_workflow import delete_workflow
from functions.activate_workflow import activate_workflow, deactivate_workflow
from functions.workflow_tags import get_workflow_tags, assign_tag, remove_tags
from functions.utils import clear_screen, headers, headers_with_content_type, N8N_URL, API_KEY

class TestN8nAppFunctions(unittest.TestCase):
    """Test N8nApp modüllerinin her birini test et"""

    def test_environment_variables(self):
        """API_KEY ve N8N_URL ortam değişkenlerinin yüklenmesini test et"""
        self.assertIsNotNone(API_KEY, "API_KEY bulunamadı")
        self.assertIsNotNone(N8N_URL, "N8N_URL bulunamadı")
        self.assertTrue(len(API_KEY) > 0, "API_KEY boş")
        self.assertTrue(len(N8N_URL) > 0, "N8N_URL boş")
        self.assertTrue(N8N_URL.startswith("http"), "N8N_URL bir URL değil")
    
    def test_headers(self):
        """HTTP header'larının doğru yapılandırıldığını test et"""
        self.assertIn("accept", headers)
        self.assertIn("X-N8N-API-KEY", headers)
        self.assertEqual(headers["accept"], "application/json")
        self.assertEqual(headers["X-N8N-API-KEY"], API_KEY)
        
        # Content-Type ile genişletilmiş header'ları test et
        self.assertIn("Content-Type", headers_with_content_type)
        self.assertEqual(headers_with_content_type["Content-Type"], "application/json")

    @patch('functions.menu.clear_screen')
    @patch('builtins.print')
    def test_display_menu(self, mock_print, mock_clear):
        """Menü görüntüleme işlevini test et"""
        display_menu()
        mock_clear.assert_called_once()
        # En az 10 kez print çağrısı yapıldığını kontrol et (menü öğeleri)
        self.assertGreaterEqual(mock_print.call_count, 10)

    @patch('functions.list_workflows.requests.get')
    def test_list_workflows(self, mock_get):
        """Workflow'ları listeleme işlevini test et"""
        # Mock response oluştur
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = [
            {"id": "123", "name": "Test Workflow 1", "active": True},
            {"id": "456", "name": "Test Workflow 2", "active": False},
        ]
        mock_get.return_value = mock_response

        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f):
            result = list_workflows()
        
        # Beklenen çıktıları kontrol et
        output = f.getvalue()
        self.assertIn("workflow", output.lower())
        self.assertIn("123", output)
        self.assertIn("456", output)
        self.assertIn("Test Workflow 1", output)
        self.assertIn("Test Workflow 2", output)
        
        # Döndürülen değeri kontrol et
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "123")
        self.assertEqual(result[1]["id"], "456")

    @patch('functions.create_workflow.requests.post')
    @patch('builtins.input', return_value="Test Workflow")
    def test_create_workflow(self, mock_input, mock_post):
        """Workflow oluşturma işlevini test et"""
        # Mock response oluştur
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "id": "789",
            "name": "Test Workflow"
        }
        mock_post.return_value = mock_response

        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f):
            create_workflow()
        
        # Beklenen çıktıları kontrol et
        output = f.getvalue()
        self.assertIn("başarıyla oluşturuldu", output.lower())
        self.assertIn("789", output)
        self.assertIn("Test Workflow", output)
        
        # Post isteğinin doğru URL ve parametrelerle yapıldığını kontrol et
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/workflows"))
        self.assertIn("headers", kwargs)
        self.assertIn("data", kwargs)

    @patch('functions.get_workflow_details.list_workflows')
    @patch('functions.get_workflow_details.requests.get')
    @patch('builtins.input', return_value="1")
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    def test_get_workflow_details(self, mock_json_dump, mock_open, mock_input, mock_get, mock_list_workflows):
        """Workflow detaylarını getirme işlevini test et"""
        # list_workflows için mock değer oluştur
        mock_list_workflows.return_value = [
            {"id": "123", "name": "Test Workflow 1", "active": True},
            {"id": "456", "name": "Test Workflow 2", "active": False},
        ]
        
        # Mock response oluştur
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "id": "123", 
            "name": "Test Workflow 1",
            "nodes": [],
            "connections": {}
        }
        mock_get.return_value = mock_response

        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f):
            get_workflow_details()
        
        # Beklenen çıktıları kontrol et
        output = f.getvalue()
        self.assertIn("detaylar", output.lower())
        self.assertIn("123", output)
        
        # JSON dosyasına kaydetme işlemini kontrol et
        mock_open.assert_called_once()
        mock_json_dump.assert_called_once()

    @patch('functions.update_workflow.list_workflows')
    @patch('functions.update_workflow.requests.get')
    @patch('functions.update_workflow.requests.put')
    @patch('builtins.input', side_effect=["1", "Yeni İsim"])
    def test_update_workflow(self, mock_input, mock_put, mock_get, mock_list_workflows):
        """Workflow güncelleme işlevini test et"""
        # list_workflows için mock değer oluştur
        mock_list_workflows.return_value = [
            {"id": "123", "name": "Test Workflow 1", "active": True},
        ]
        
        # Get için mock response
        get_response = MagicMock()
        get_response.raise_for_status = MagicMock()
        get_response.json.return_value = {
            "id": "123",
            "name": "Test Workflow 1",
            "nodes": [],
            "connections": {}
        }
        mock_get.return_value = get_response
        
        # Put için mock response
        put_response = MagicMock()
        put_response.raise_for_status = MagicMock()
        mock_put.return_value = put_response

        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f):
            update_workflow()
        
        # Beklenen çıktıları kontrol et
        output = f.getvalue()
        self.assertIn("güncelleniyor", output.lower())
        self.assertIn("başarıyla güncellendi", output.lower())

    @patch('functions.delete_workflow.list_workflows')
    @patch('functions.delete_workflow.requests.delete')
    @patch('builtins.input', side_effect=["1", "SIL"])
    def test_delete_workflow(self, mock_input, mock_delete, mock_list_workflows):
        """Workflow silme işlevini test et"""
        # list_workflows için mock değer oluştur
        mock_list_workflows.return_value = [
            {"id": "123", "name": "Test Workflow 1", "active": True},
        ]
        
        # Delete için mock response
        delete_response = MagicMock()
        delete_response.raise_for_status = MagicMock()
        mock_delete.return_value = delete_response

        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f):
            delete_workflow()
        
        # Beklenen çıktıları kontrol et
        output = f.getvalue()
        self.assertIn("siliniyor", output.lower())
        self.assertIn("başarıyla silindi", output.lower())

    @patch('functions.activate_workflow.list_workflows')
    @patch('functions.activate_workflow.requests.post')
    @patch('builtins.input', return_value="1")
    def test_activate_workflow(self, mock_input, mock_post, mock_list_workflows):
        """Workflow aktifleştirme işlevini test et"""
        # list_workflows için mock değer oluştur
        mock_list_workflows.return_value = [
            {"id": "123", "name": "Test Workflow 1", "active": False},
        ]
        
        # Post için mock response
        post_response = MagicMock()
        post_response.raise_for_status = MagicMock()
        mock_post.return_value = post_response

        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f):
            activate_workflow()
        
        # Beklenen çıktıları kontrol et
        output = f.getvalue()
        self.assertIn("aktif ediliyor", output.lower())
        self.assertIn("başarıyla aktif edildi", output.lower())

    @patch('functions.activate_workflow.list_workflows')
    @patch('functions.activate_workflow.requests.post')
    @patch('builtins.input', return_value="1")
    def test_deactivate_workflow(self, mock_input, mock_post, mock_list_workflows):
        """Workflow pasifleştirme işlevini test et"""
        # list_workflows için mock değer oluştur
        mock_list_workflows.return_value = [
            {"id": "123", "name": "Test Workflow 1", "active": True},
        ]
        
        # Post için mock response
        post_response = MagicMock()
        post_response.raise_for_status = MagicMock()
        mock_post.return_value = post_response

        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f):
            deactivate_workflow()
        
        # Beklenen çıktıları kontrol et
        output = f.getvalue()
        self.assertIn("pasif ediliyor", output.lower())
        self.assertIn("başarıyla pasif edildi", output.lower())

    @patch('functions.workflow_tags.list_workflows')
    @patch('functions.workflow_tags.requests.get')
    @patch('builtins.input', return_value="1")
    def test_get_workflow_tags(self, mock_input, mock_get, mock_list_workflows):
        """Workflow etiketlerini getirme işlevini test et"""
        # list_workflows için mock değer oluştur
        mock_list_workflows.return_value = [
            {"id": "123", "name": "Test Workflow 1", "active": True},
        ]
        
        # Get için mock response
        get_response = MagicMock()
        get_response.raise_for_status = MagicMock()
        get_response.json.return_value = [
            {"id": "tag1", "name": "Test Tag 1"},
            {"id": "tag2", "name": "Test Tag 2"}
        ]
        mock_get.return_value = get_response

        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f):
            get_workflow_tags()
        
        # Beklenen çıktıları kontrol et
        output = f.getvalue()
        self.assertIn("etiketler getiriliyor", output.lower())
        self.assertIn("etiketler", output.lower())
        self.assertIn("tag1", output)
        self.assertIn("tag2", output)

    @patch('functions.workflow_tags.list_workflows')
    @patch('functions.workflow_tags.requests.put')
    @patch('builtins.input', side_effect=["1", "tag1"])
    def test_assign_tag(self, mock_input, mock_put, mock_list_workflows):
        """Workflow etiket atama işlevini test et"""
        # list_workflows için mock değer oluştur
        mock_list_workflows.return_value = [
            {"id": "123", "name": "Test Workflow 1", "active": True},
        ]
        
        # Put için mock response
        put_response = MagicMock()
        put_response.raise_for_status = MagicMock()
        mock_put.return_value = put_response

        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f):
            assign_tag()
        
        # Beklenen çıktıları kontrol et
        output = f.getvalue()
        self.assertIn("etiketi atanıyor", output.lower())
        self.assertIn("başarıyla atandı", output.lower())

    @patch('functions.workflow_tags.list_workflows')
    @patch('functions.workflow_tags.requests.put')
    @patch('builtins.input', return_value="1")
    def test_remove_tags(self, mock_input, mock_put, mock_list_workflows):
        """Workflow etiketlerini kaldırma işlevini test et"""
        # list_workflows için mock değer oluştur
        mock_list_workflows.return_value = [
            {"id": "123", "name": "Test Workflow 1", "active": True},
        ]
        
        # Put için mock response
        put_response = MagicMock()
        put_response.raise_for_status = MagicMock()
        mock_put.return_value = put_response

        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f):
            remove_tags()
        
        # Beklenen çıktıları kontrol et
        output = f.getvalue()
        self.assertIn("etiketler kaldırılıyor", output.lower())
        self.assertIn("başarıyla kaldırıldı", output.lower())

if __name__ == '__main__':
    unittest.main()
