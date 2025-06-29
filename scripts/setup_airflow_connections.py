#!/usr/bin/env python3
"""
Airflow connection'larını otomatik olarak oluşturan script
"""

import subprocess
import sys
import time

def run_command(command):
    """Komut çalıştırma ve sonuç kontrolü"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Başarılı: {command}")
            return True
        else:
            print(f"❌ Hata: {command}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {command} - {e}")
        return False

def main():
    """Main connection setup function"""
    print("🔧 Airflow PostgreSQL Connection kurulumu başlatılıyor...")
    
    # PostgreSQL connection için gerekli bilgiler
    postgres_conn_id = "postgres_default"
    postgres_uri = "postgresql://admin:admin@postgres:5432/swen_dwh"
    
    # Mevcut connection'ı sil (varsa)
    delete_command = f"airflow connections delete {postgres_conn_id}"
    run_command(delete_command)
    
    # Yeni PostgreSQL connection oluştur
    create_command = f"""airflow connections add {postgres_conn_id} \
        --conn-type postgres \
        --conn-host postgres \
        --conn-login admin \
        --conn-password admin \
        --conn-schema swen_dwh \
        --conn-port 5432"""
    
    if run_command(create_command):
        print(f"✅ PostgreSQL connection '{postgres_conn_id}' başarıyla oluşturuldu!")
    else:
        print(f"❌ PostgreSQL connection '{postgres_conn_id}' oluşturulamadı!")
        sys.exit(1)
    
    # Connection'ı test et
    test_command = f"airflow connections test {postgres_conn_id}"
    if run_command(test_command):
        print(f"✅ PostgreSQL connection testi başarılı!")
    else:
        print(f"⚠️ PostgreSQL connection testi başarısız - ancak devam ediliyor")
    
    print("🎉 Airflow connection kurulumu tamamlandı!")

if __name__ == "__main__":
    main() 