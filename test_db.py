import json
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from database import Base, obtener_o_crear_conversacion, guardar_mensaje

test_engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(bind=test_engine)

with Session(test_engine) as db:
    # Test 1: crear conversacion nueva
    conv = obtener_o_crear_conversacion(db, "+5491155551234")
    assert conv.id is not None
    assert conv.telefono_cliente == "+5491155551234"
    assert conv.estado_humano == False
    print(f"Test 1 OK: conversacion creada con id={conv.id}")

    # Test 2: reusar la misma conversacion activa
    conv2 = obtener_o_crear_conversacion(db, "+5491155551234")
    assert conv2.id == conv.id
    print(f"Test 2 OK: conversacion reutilizada (mismo id={conv2.id})")

    # Test 3: guardar mensaje user
    msg_user = guardar_mensaje(db, conv.id, "user", "Hola, necesito una bascula")
    assert msg_user.id is not None
    assert msg_user.rol == "user"
    print(f"Test 3 OK: mensaje user guardado con id={msg_user.id}")

    # Test 4: guardar mensaje assistant con nota interna
    nota = json.dumps({"categoria": "Venta de Equipos", "ubicacion": None})
    msg_ai = guardar_mensaje(db, conv.id, "assistant", "Hola! Con gusto te ayudo.", nota)
    assert msg_ai.nota_interna_json == nota
    print("Test 4 OK: mensaje assistant con nota_interna guardado")

    # Test 5: historial se carga en orden correcto
    db.refresh(conv)
    historial = [{"role": m.rol, "content": m.contenido} for m in conv.mensajes]
    assert historial[0]["role"] == "user"
    assert historial[1]["role"] == "assistant"
    print(f"Test 5 OK: historial ordenado ({len(historial)} mensajes)")

    # Test 6: otro telefono crea conversacion nueva
    conv3 = obtener_o_crear_conversacion(db, "+5491199998888")
    assert conv3.id != conv.id
    print(f"Test 6 OK: telefono diferente -> conversacion nueva (id={conv3.id})")

    # Test 7: nota_interna_json es None cuando no se pasa
    msg_sin_nota = guardar_mensaje(db, conv.id, "user", "mensaje sin nota")
    assert msg_sin_nota.nota_interna_json is None
    print("Test 7 OK: nota_interna_json es None cuando no se pasa")

print()
print("Todos los tests de base de datos pasaron correctamente.")
