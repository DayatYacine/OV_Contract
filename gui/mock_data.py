import random
from datetime import datetime, timedelta

# Helper lists to generate realistic dummy data
first_names_en = ["John", "Jane", "Alex", "Emily", "Michael", "Sarah", "David", "Jessica"]
last_names_en = ["Smith", "Doe", "Johnson", "Brown", "Williams", "Miller", "Davis", "Wilson"]
first_names_ar = ["أحمد", "فاطمة", "محمد", "مريم", "يوسف", "عائشة", "علي", "زينب"]
last_names_ar = ["علوي", "براهيمي", "منصور", "بن علي", "عثمان", "قاسم", "راضي", "سعيد"]
cities_en = ["Algiers", "Oran", "Constantine", "Annaba", "Setif", "Tlemcen"]
cities_ar = ["الجزائر", "وهران", "قسنطينة", "عنابة", "سطيف", "تلمسان"]

def generate_mock_data(num_rows=100):
    mock_data = []
    
    for i in range(1, num_rows + 1):
        # Calculate random birthdate
        start_date = datetime(1975, 1, 1)
        days_between = (datetime(2003, 12, 31) - start_date).days
        birthdate = (start_date + timedelta(days=random.randrange(days_between))).strftime("%Y-%m-%d")
        
        # Build the structured dictionary directly
        employee_dict = {
            "id": f"{i:03d}",
            "matricule": f"MAT-{random.randint(1000, 9999)}",
            "first_name": random.choice(first_names_en),
            "last_name": random.choice(last_names_en),
            "first_name_arabic": random.choice(first_names_ar),
            "last_name_arabic": random.choice(last_names_ar),
            "national_id": f"NID-{random.randint(10000, 99999)}",
            "date_of_birth": birthdate,
            "place_of_birth": random.choice(cities_en),
            "place_of_birth_arabic": random.choice(cities_ar)
        }
        
        mock_data.append(employee_dict)
        
    return mock_data