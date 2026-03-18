"""
Script para probar las conexiones y credenciales
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_env_variables():
    """Verificar que las variables de entorno están configuradas"""
    print("=" * 50)
    print("VERIFICANDO VARIABLES DE ENTORNO")
    print("=" * 50)

    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_PHONE_NUMBER',
        'MONGODB_URI',
        'OPENAI_API_KEY'
    ]

    all_ok = True
    for var in required_vars:
        value = os.getenv(var)
        if value and 'tu_' not in value and 'password' not in value:
            print(f"✓ {var}: Configurado")
        else:
            print(f"✗ {var}: NO configurado o usa valor por defecto")
            all_ok = False

    return all_ok

def test_mongodb():
    """Probar conexión a MongoDB"""
    print("\n" + "=" * 50)
    print("PROBANDO MONGODB")
    print("=" * 50)

    try:
        from pymongo import MongoClient
        client = MongoClient(os.getenv('MONGODB_URI'), serverSelectionTimeoutMS=5000)
        # Probar conexión
        client.server_info()
        print("✓ Conexión exitosa a MongoDB")

        # Verificar base de datos y colección
        db = client['cafe_feedback']
        collection = db['mensajes']
        count = collection.count_documents({})
        print(f"✓ Colección 'mensajes' accesible ({count} documentos)")

        client.close()
        return True
    except Exception as e:
        print(f"✗ Error conectando a MongoDB: {e}")
        return False

def test_twilio():
    """Probar credenciales de Twilio"""
    print("\n" + "=" * 50)
    print("PROBANDO TWILIO")
    print("=" * 50)

    try:
        from twilio.rest import Client

        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')

        client = Client(account_sid, auth_token)

        # Obtener información de la cuenta
        account = client.api.accounts(account_sid).fetch()
        print(f"✓ Credenciales válidas - Cuenta: {account.friendly_name}")
        print(f"✓ Status: {account.status}")

        return True
    except Exception as e:
        print(f"✗ Error con Twilio: {e}")
        return False

def test_openai():
    """Probar API key de OpenAI"""
    print("\n" + "=" * 50)
    print("PROBANDO OPENAI API")
    print("=" * 50)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        # Hacer una petición simple
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Di 'ok'"}],
            max_tokens=5
        )

        print(f"✓ API Key válida - Respuesta: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"✗ Error con OpenAI: {e}")
        return False

if __name__ == "__main__":
    print("\n🔍 VERIFICACIÓN DE CONFIGURACIÓN\n")

    # Test 1: Variables de entorno
    if not test_env_variables():
        print("\n⚠️  IMPORTANTE: Primero configura tus credenciales en el archivo .env")
        exit(1)

    # Test 2: MongoDB
    mongodb_ok = test_mongodb()

    # Test 3: Twilio
    twilio_ok = test_twilio()

    # Test 4: OpenAI
    openai_ok = test_openai()

    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN")
    print("=" * 50)

    if mongodb_ok and twilio_ok and openai_ok:
        print("✓ Todas las conexiones funcionan correctamente")
        print("\n✅ ¡Listo para continuar con el PASO 3!")
    else:
        print("✗ Algunas conexiones fallaron - revisa la configuración")
