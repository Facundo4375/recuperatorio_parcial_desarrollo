import unittest
import os
from flask import current_app
from app import create_app
from app.models import Especialidad, TipoEspecialidad
from app.services import EspecialidadService, TipoEspecialidadService
from test.instancias import nuevaespecialidad, nuevotipoespecialidad
from app import db

class EspecialidadTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear(self):
        especialidad= nuevaespecialidad()
        self.assertIsNotNone(especialidad)
        self.assertIsNotNone(especialidad.id)
        self.assertGreaterEqual(especialidad.id,1)
        self.assertEqual(especialidad.nombre, "Matematicas")
        self.assertEqual(especialidad.tipoespecialidad.nombre, "Cardiologia")

    def test_buscar_por_id(self):
        especialidad = nuevaespecialidad()
        r=EspecialidadService.buscar_por_id(especialidad.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, "Matematicas")
        self.assertEqual(r.letra, "A")

    def test_buscar_todos(self):
        especialidad1 =nuevaespecialidad()
        especialidad2 =nuevaespecialidad()
        especialidades = EspecialidadService.buscar_todos()
        self.assertIsNotNone(especialidades)
        self.assertEqual(len(especialidades),2)

    def test_actualizar(self):
        especialidad = nuevaespecialidad()
        especialidad.nombre = "matematica actualizada"
        especialidad_actualizada = EspecialidadService.actualizar(especialidad.id, especialidad)
        self.assertEqual(especialidad_actualizada.nombre, "matematica actualizada")

    def test_borrar(self):
        especialidad = nuevaespecialidad()
        borrado = EspecialidadService.borrar_por_id(especialidad.id)
        self.assertTrue(borrado)
        resultado = EspecialidadService.buscar_por_id(especialidad.id)
        self.assertIsNone(resultado)

    def test_obtener_alumnos_con_facultad(self):
        """
        Test TDD: Obtener todos los alumnos de una especialidad con su facultad.
        Verifica que retorna JSON con alumnos y facultad.
        """
        from test.instancias import nuevoalumno, nuevafacultad
        from datetime import date
        
        # Crear especialidad con facultad
        facultad = nuevafacultad(nombre="Facultad de Ciencias", sigla="FC")
        especialidad = nuevaespecialidad(nombre="Matemáticas", facultad=facultad)
        
        # Crear alumnos para la especialidad
        alumno1 = nuevoalumno(
            nombre="Juan",
            apellido="Pérez",
            nrodocumento="12345678",
            especialidad=especialidad
        )
        alumno2 = nuevoalumno(
            nombre="María",
            apellido="Gómez",
            nrodocumento="87654321",
            especialidad=especialidad
        )
        
        # Obtener alumnos con facultad
        resultado = EspecialidadService.obtener_alumnos_con_facultad(especialidad.id)
        
        # Verificaciones
        self.assertIsNotNone(resultado)
        self.assertIn('alumnos', resultado)
        self.assertIn('facultad', resultado)
        
        # Verificar alumnos
        self.assertEqual(len(resultado['alumnos']), 2)
        nombres_alumnos = [a['nombre'] for a in resultado['alumnos']]
        self.assertIn("Juan", nombres_alumnos)
        self.assertIn("María", nombres_alumnos)
        
        # Verificar facultad
        self.assertEqual(resultado['facultad']['nombre'], "Facultad de Ciencias")
        self.assertEqual(resultado['facultad']['sigla'], "FC")
        
        # Verificar que los alumnos tienen los datos correctos
        alumno1_data = next(a for a in resultado['alumnos'] if a['nombre'] == "Juan")
        self.assertEqual(alumno1_data['apellido'], "Pérez")
        self.assertEqual(alumno1_data['nrodocumento'], "12345678")

    