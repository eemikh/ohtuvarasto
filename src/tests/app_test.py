import unittest
from app import app, varastos

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        """Set up test client and clear varastos"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        varastos.clear()

    def tearDown(self):
        """Clear varastos after each test"""
        varastos.clear()

    def test_index_page_loads(self):
        """Test that index page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Varasto Management', response.data)

    def test_create_varasto_success(self):
        """Test creating a varasto successfully"""
        response = self.client.post('/create', data={
            'name': 'TestVarasto',
            'tilavuus': '100.0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('TestVarasto', varastos)
        self.assertEqual(varastos['TestVarasto'].tilavuus, 100.0)
        self.assertIn(b'luotu onnistuneesti', response.data)

    def test_create_varasto_invalid_tilavuus(self):
        """Test creating a varasto with invalid tilavuus"""
        response = self.client.post('/create', data={
            'name': 'BadVarasto',
            'tilavuus': '-10.0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('BadVarasto', varastos)
        self.assertIn(b'positiivinen', response.data)

    def test_create_varasto_duplicate_name(self):
        """Test creating a varasto with duplicate name"""
        self.client.post('/create', data={
            'name': 'TestVarasto',
            'tilavuus': '100.0'
        })
        
        response = self.client.post('/create', data={
            'name': 'TestVarasto',
            'tilavuus': '200.0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'on jo olemassa', response.data)
        # Original varasto should still exist with original tilavuus
        self.assertEqual(varastos['TestVarasto'].tilavuus, 100.0)

    def test_create_varasto_empty_name(self):
        """Test creating a varasto with empty name"""
        response = self.client.post('/create', data={
            'name': '',
            'tilavuus': '100.0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(varastos), 0)
        self.assertIn(b'pakollinen', response.data)

    def test_add_to_varasto_success(self):
        """Test adding to a varasto successfully"""
        self.client.post('/create', data={
            'name': 'TestVarasto',
            'tilavuus': '100.0'
        })
        
        response = self.client.post('/add/TestVarasto', data={
            'maara': '50.0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(varastos['TestVarasto'].saldo, 50.0)
        self.assertIn('Lisätty'.encode('utf-8'), response.data)

    def test_add_to_nonexistent_varasto(self):
        """Test adding to a non-existent varasto"""
        response = self.client.post('/add/NonExistent', data={
            'maara': '50.0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('ei löydy'.encode('utf-8'), response.data)

    def test_add_negative_amount(self):
        """Test adding negative amount to varasto"""
        self.client.post('/create', data={
            'name': 'TestVarasto',
            'tilavuus': '100.0'
        })
        
        response = self.client.post('/add/TestVarasto', data={
            'maara': '-10.0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(varastos['TestVarasto'].saldo, 0.0)
        self.assertIn(b'positiivinen', response.data)

    def test_take_from_varasto_success(self):
        """Test taking from a varasto successfully"""
        self.client.post('/create', data={
            'name': 'TestVarasto',
            'tilavuus': '100.0'
        })
        self.client.post('/add/TestVarasto', data={'maara': '50.0'})
        
        response = self.client.post('/take/TestVarasto', data={
            'maara': '20.0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(varastos['TestVarasto'].saldo, 30.0)
        self.assertIn('Otettu'.encode('utf-8'), response.data)

    def test_take_from_nonexistent_varasto(self):
        """Test taking from a non-existent varasto"""
        response = self.client.post('/take/NonExistent', data={
            'maara': '20.0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('ei löydy'.encode('utf-8'), response.data)

    def test_take_more_than_available(self):
        """Test taking more than available amount"""
        self.client.post('/create', data={
            'name': 'TestVarasto',
            'tilavuus': '100.0'
        })
        self.client.post('/add/TestVarasto', data={'maara': '30.0'})
        
        response = self.client.post('/take/TestVarasto', data={
            'maara': '50.0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Should only take what's available (30.0)
        self.assertEqual(varastos['TestVarasto'].saldo, 0.0)
        self.assertIn('Otettu 30'.encode('utf-8'), response.data)

    def test_delete_varasto_success(self):
        """Test deleting a varasto successfully"""
        self.client.post('/create', data={
            'name': 'TestVarasto',
            'tilavuus': '100.0'
        })
        
        response = self.client.post('/delete/TestVarasto', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('TestVarasto', varastos)
        self.assertIn('poistettu'.encode('utf-8'), response.data)

    def test_delete_nonexistent_varasto(self):
        """Test deleting a non-existent varasto"""
        response = self.client.post('/delete/NonExistent', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('ei löydy'.encode('utf-8'), response.data)

    def test_multiple_varastos(self):
        """Test creating and managing multiple varastos"""
        # Create multiple varastos
        self.client.post('/create', data={'name': 'Varasto1', 'tilavuus': '100.0'})
        self.client.post('/create', data={'name': 'Varasto2', 'tilavuus': '200.0'})
        self.client.post('/create', data={'name': 'Varasto3', 'tilavuus': '150.0'})
        
        self.assertEqual(len(varastos), 3)
        
        # Add to different varastos
        self.client.post('/add/Varasto1', data={'maara': '50.0'})
        self.client.post('/add/Varasto2', data={'maara': '100.0'})
        
        self.assertEqual(varastos['Varasto1'].saldo, 50.0)
        self.assertEqual(varastos['Varasto2'].saldo, 100.0)
        self.assertEqual(varastos['Varasto3'].saldo, 0.0)
        
        # Delete one varasto
        self.client.post('/delete/Varasto2')
        
        self.assertEqual(len(varastos), 2)
        self.assertNotIn('Varasto2', varastos)

    def test_add_overflow_handling(self):
        """Test that adding more than capacity is handled correctly"""
        self.client.post('/create', data={
            'name': 'TestVarasto',
            'tilavuus': '100.0'
        })
        
        self.client.post('/add/TestVarasto', data={'maara': '150.0'})
        
        # Should be capped at tilavuus
        self.assertEqual(varastos['TestVarasto'].saldo, 100.0)

    def test_invalid_number_format(self):
        """Test handling of invalid number formats"""
        self.client.post('/create', data={
            'name': 'TestVarasto',
            'tilavuus': '100.0'
        })
        
        response = self.client.post('/add/TestVarasto', data={
            'maara': 'invalid'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Virheellinen'.encode('utf-8'), response.data)
