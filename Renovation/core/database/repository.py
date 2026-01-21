"""
Repository Pattern for Database Access
Provides abstraction layer over existing BusinessDatabase for domain logic
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from pathlib import Path
import sys

# Import existing database
sys.path.append(str(Path(__file__).parents[3] / "scraper"))
from database import BusinessDatabase


class AbstractRepository(ABC):
    """Base repository interface for all repositories"""
    
    @abstractmethod
    def get_by_id(self, id: Any) -> Optional[Dict]:
        """Get single record by ID"""
        pass
    
    @abstractmethod
    def list_all(self, limit: Optional[int] = None) -> List[Dict]:
        """List all records with optional limit"""
        pass
    
    @abstractmethod
    def add(self, data: Dict) -> bool:
        """Add new record"""
        pass
    
    @abstractmethod
    def update(self, id: Any, data: Dict) -> bool:
        """Update existing record"""
        pass


class BusinessRepository(AbstractRepository):
    """
    Repository pattern wrapper for BusinessDatabase
    Maintains backward compatibility while providing cleaner domain interface
    """
    
    def __init__(self, db_path: str = "businesses.db"):
        self._db = BusinessDatabase(db_path)
    
    def get_by_id(self, fsq_id: str) -> Optional[Dict]:
        """Get business by Foursquare ID"""
        return self._db.get_business(fsq_id)
    
    def get_by_tier(self, tier: int, limit: Optional[int] = None) -> List[Dict]:
        """Get businesses by tier classification"""
        return self._db.get_businesses_by_tier(tier, limit)
    
    def get_no_website(self, limit: Optional[int] = None) -> List[Dict]:
        """Get businesses without websites (Tier 1 priority leads)"""
        return self._db.get_businesses_without_website(limit)
    
    def list_all(self, limit: Optional[int] = None) -> List[Dict]:
        """List all businesses"""
        return self._db.get_all_businesses(limit)
    
    def add(self, data: Dict) -> bool:
        """Add new business"""
        return self._db.add_business(data)
    
    def update(self, fsq_id: str, data: Dict) -> bool:
        """Update business data"""
        return self._db.update_business_analysis(fsq_id, data)
    
    def bulk_add(self, businesses: List[Dict]) -> int:
        """Add multiple businesses, returns count added"""
        count = 0
        for business in businesses:
            if self.add(business):
                count += 1
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return self._db.get_stats()
    
    def search(self, category: Optional[str] = None, 
               city: Optional[str] = None,
               has_website: Optional[bool] = None) -> List[Dict]:
        """Search businesses with filters"""
        # Delegate to existing database methods
        if category and city:
            return self._db.search_by_category_and_location(category, city)
        elif has_website is False:
            return self.get_no_website()
        else:
            return self.list_all()


class WorkflowStateRepository:
    """Repository for workflow execution state (task registry)"""
    
    def __init__(self, db_path: str = "businesses.db"):
        from Renovation.infrastructure.task_registry.registry import TaskRegistry
        self._registry = TaskRegistry(Path(db_path))
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get task by ID"""
        # Stub - extend TaskRegistry to support get
        return None
    
    def mark_started(self, task_id: str, workflow_type: str, business_fsq_id: Optional[str]) -> None:
        """Mark task as started"""
        self._registry.mark_started(task_id, workflow_type, business_fsq_id)
    
    def mark_completed(self, task_id: str, outputs: Optional[Dict] = None) -> None:
        """Mark task as completed"""
        self._registry.mark_completed(task_id, outputs)
    
    def mark_failed(self, task_id: str, error: str) -> None:
        """Mark task as failed"""
        self._registry.mark_failed(task_id, error)
    
    def exists(self, task_id: str) -> bool:
        """Check if task exists"""
        return self._registry.exists(task_id)


__all__ = [
    "AbstractRepository",
    "BusinessRepository", 
    "WorkflowStateRepository"
]
