#!/usr/bin/env python3
"""
N8nApp ana modülünü test etme
"""
import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os
import io
from contextlib import redirect_stdout

# Ana proje dizinini import path'e ekleyelim
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from n8nApp import main

class TestN8nAppMain(unittest.TestCase):
    """Ana n8nApp modülünün işlevselliğini test et"""
    
    @patch('functions.menu.display_menu')
    @patch('functions.list_workflows.list_workflows')
    @patch('builtins.input', side_effect=["1", "", "0"])
    def test_main_list_workflows(self, mock_input, mock_list_workflows, mock_display_menu):
        """Ana döngüde workflow listeleme işlevini test et"""
        # Klavyeden ilk seçim "1" yapılacak, sonra Enter tuşu, sonra "0" çıkış
        
        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f), patch.object(sys, 'exit'):
            main()
        
        # Display menü fonksiyonunun çağrıldığını kontrol et
        mock_display_menu.assert_called()
        
        # List workflows fonksiyonunun çağrıldığını kontrol et
        mock_list_workflows.assert_called_once()
        
        # Çıktıyı kontrol et
        output = f.getvalue()
        self.assertIn("çıkılıyor", output.lower())

    @patch('functions.menu.display_menu')
    @patch('functions.get_workflow_details.get_workflow_details')
    @patch('builtins.input', side_effect=["2", "", "0"])
    def test_main_get_details(self, mock_input, mock_get_details, mock_display_menu):
        """Ana döngüde workflow detay alma işlevini test et"""
        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f), patch.object(sys, 'exit'):
            main()
        
        # Get details fonksiyonunun çağrıldığını kontrol et
        mock_get_details.assert_called_once()

    @patch('functions.menu.display_menu')
    @patch('functions.create_workflow.create_workflow')
    @patch('builtins.input', side_effect=["3", "", "0"])
    def test_main_create_workflow(self, mock_input, mock_create, mock_display_menu):
        """Ana döngüde workflow oluşturma işlevini test et"""
        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f), patch.object(sys, 'exit'):
            main()
        
        # Create workflow fonksiyonunun çağrıldığını kontrol et
        mock_create.assert_called_once()

    @patch('functions.menu.display_menu')
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_main_keyboard_interrupt(self, mock_input, mock_display_menu):
        """Klavyeden Ctrl+C geldiğinde ana döngünün davranışını test et"""
        # Fonksiyonu çağır ve çıktıyı yakala
        f = io.StringIO()
        with redirect_stdout(f), patch.object(sys, 'exit'):
            # Döngüden çıkabilmek için ikinci input'u mock'la
            with patch('builtins.input', side_effect=["0"]):
                main()
        
        # Çıktıyı kontrol et
        output = f.getvalue()
        self.assertIn("iptal edildi", output.lower())

if __name__ == '__main__':
    unittest.main()
