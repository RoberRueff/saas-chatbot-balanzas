import os

os.environ["GEMINI_API_KEY"] = "test-key"

from main import app, _ia_configurada
from fastapi.testclient import TestClient

client = TestClient(app)

# GET / indica proveedor gemini
r = client.get("/")
assert r.status_code == 200
assert r.json()["ia"] == "gemini-2.0-flash"
print("GET / OK:", r.json())

# _ia_configurada con clave presente
assert _ia_configurada() is True
print("_ia_configurada(clave presente) OK")

# _ia_configurada sin clave
os.environ["GEMINI_API_KEY"] = ""
assert _ia_configurada() is False
print("_ia_configurada(sin clave) OK")

print()
print("Todos los checks pasaron.")
