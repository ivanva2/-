import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prog import Materials, TypesOfMaterials, Base, hash_password

# Настройка тестовой базы данных
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

class TestMaterials(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создание таблиц в тестовой базе данных
        Base.metadata.create_all(engine)

    def test_material_creation(self):
        # Тестирование создания материала
        new_material = Materials(size='M', characteristic='Strong', quantity=100, material_id=1)
        session.add(new_material)
        session.commit()
        result = session.query(Materials).filter_by(size='M').first()
        self.assertIsNotNone(result)
        self.assertEqual(result.characteristic, 'Strong')

    def test_typesofmaterials_creation(self):
        # Тестирование создания типа материала
        new_type = TypesOfMaterials(typeofmaterial='Wood')
        session.add(new_type)
        session.commit()
        result = session.query(TypesOfMaterials).filter_by(typeofmaterial='Wood').first()
        self.assertIsNotNone(result)

    def test_password_hashing(self):
        # Тестирование хэширования пароля
        password = 'securepassword'
        hashed_password = hash_password(password)
        self.assertNotEqual(password, hashed_password)

if __name__ == '__main__':
    unittest.main()