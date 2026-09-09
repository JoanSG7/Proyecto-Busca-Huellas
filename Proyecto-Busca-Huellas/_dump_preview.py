from app import app

client = app.test_client()
with client.session_transaction() as session:
    session["usuario_id"] = 1
    session["rol_id"] = 2

response = client.get("/inicio")
with open("static/_preview_inicio.html", "w", encoding="utf-8") as preview:
    preview.write(response.get_data(as_text=True))
print(response.status_code, len(response.data))
