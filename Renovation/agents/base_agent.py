"""
Base Agent Interface
Abstract class defining common interface for all agents in the system
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum


class AgentStatus(Enum):
    """Agent execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class AgentType(Enum):
    """Agent classification"""
    ANALYSIS = "analysis"
    GENERATION = "generation"
    VALIDATION = "validation"
    ORCHESTRATION = "orchestration"


class BaseAgent(ABC):
    """
    Abstract base class for all agents
    Defines common interface and behavior
    """
    
    def __init__(self, name: str, agent_type: AgentType):
        self.name = name
        self.agent_type = agent_type
        self.status = AgentStatus.PENDING
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.error_message: Optional[str] = None
        self.outputs: Dict[str, Any] = {}
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic
        
        Args:
            input_data: Input data for agent processing
            
        Returns:
            Dict containing agent outputs
            
        Raises:
            AgentExecutionError: If execution fails
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input data before execution
        
        Args:
            input_data: Data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    @abstractmethod
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """
        Validate output data after execution
        
        Args:
            output_data: Data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution wrapper with status tracking and error handling
        
        Args:
            input_data: Input data for agent
            
        Returns:
            Dict with status and outputs
        """
        try:
            # Mark as started
            self.status = AgentStatus.IN_PROGRESS
            self.started_at = datetime.now()
            
            # Validate input
            if not self.validate_input(input_data):
                raise ValueError(f"Invalid input for agent {self.name}")
            
            # Execute
            self.outputs = self.execute(input_data)
            
            # Validate output
            if not self.validate_output(self.outputs):
                raise ValueError(f"Invalid output from agent {self.name}")
            
            # Mark as completed
            self.status = AgentStatus.COMPLETED
            self.completed_at = datetime.now()
            
            return {
                "status": self.status.value,
                "agent_name": self.name,
                "agent_type": self.agent_type.value,
                "outputs": self.outputs,
                "execution_time": (self.completed_at - self.started_at).total_seconds()
            }
            
        except Exception as e:
            self.status = AgentStatus.FAILED
            self.error_message = str(e)
            self.completed_at = datetime.now()
            
            return {
                "status": self.status.value,
                "agent_name": self.name,
                "agent_type": self.agent_type.value,
                "error": self.error_message,
                "execution_time": (self.completed_at - self.started_at).total_seconds() if self.started_at else 0
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "name": self.name,
            "type": self.agent_type.value,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error_message
        }
    
    def reset(self):
        """Reset agent state for reuse"""
        self.status = AgentStatus.PENDING
        self.started_at = None
        self.completed_at = None
        self.error_message = None
        self.outputs = {}


class AgentExecutionError(Exception):
    """Exception raised when agent execution fails"""
    pass


class ValidationError(Exception):
    """Exception raised when validation fails"""
    pass


__all__ = [
    "BaseAgent",
    "AgentStatus", 
    "AgentType",
    "AgentExecutionError",
    "ValidationError"
]
