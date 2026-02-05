"""
Base classes for the scoring system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ScorerResult:
    """Result from a scorer evaluation."""
    
    name: str
    score: float  # 0.0 to 1.0
    message: str
    details: Optional[dict[str, str]] = None
    
    @property
    def percentage(self) -> float:
        """Return score as percentage."""
        return round(self.score * 100, 2)


class Scorer(ABC):
    """Abstract base class for all scorers."""
    
    name: str = "base"
    weight: float = 1.0
    description: str = ""
    
    @abstractmethod
    def evaluate(self, cwd: str = ".") -> ScorerResult:
        """
        Evaluate the scoring criteria.
        
        Args:
            cwd: Working directory to run the evaluation in.
            
        Returns:
            ScorerResult with score and details.
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(weight={self.weight})"
