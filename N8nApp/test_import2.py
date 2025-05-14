import traceback
try:
  from functions.compare_workflows import compare_workflows
  print("Import başarılı")
except Exception as e:
  print(f"Hata: {type(e).__name__}: {e}")
  traceback.print_exc()
