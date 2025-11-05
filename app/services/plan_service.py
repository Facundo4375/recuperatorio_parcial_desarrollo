from app.models import Plan
from app.repositories import PlanRepository

class PlanService:
    @staticmethod
    def crear(plan):
        PlanRepository.crear(plan)
    
    @staticmethod
    def buscar_por_id(id: int) -> Plan:
        return PlanRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[Plan]:
        return PlanRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id : int, plan: Plan) -> Plan:
        """
        Actualiza un plan existente usando merge directamente.
        Issue: #3 - Simplificación del método actualizar usando merge
        """
        plan_existente = PlanRepository.buscar_por_id(id)
        if not plan_existente:
            return None
        
        # Asignar el ID y usar merge (más simple que copiar campos manualmente)
        plan.id = id
        return PlanRepository.actualizar(plan)
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return PlanRepository.borrar_por_id(id)
