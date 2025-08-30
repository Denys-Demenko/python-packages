"""
Generic paginated result class for consistent pagination across the application.
"""

from typing import Generic, TypeVar, List
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class PaginatedResult(Generic[T]):
    """
    Generic paginated result container.
    
    Provides a consistent structure for paginated data across the application.
    """
    
    items: List[T]
    total_count: int
    page_count: int
    current_page: int
    page_size: int
    has_next: bool
    has_previous: bool
    
    @property
    def is_empty(self) -> bool:
        """Check if the result contains any items."""
        return len(self.items) == 0
    
    @property
    def item_count(self) -> int:
        """Get the number of items in the current page."""
        return len(self.items)
    
    @property
    def start_index(self) -> int:
        """Get the starting index of items in the current page (1-based)."""
        if self.is_empty:
            return 0
        return (self.current_page - 1) * self.page_size + 1
    
    @property
    def end_index(self) -> int:
        """Get the ending index of items in the current page (1-based)."""
        if self.is_empty:
            return 0
        return self.start_index + self.item_count - 1
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'items': self.items,
            'total_count': self.total_count,
            'page_count': self.page_count,
            'current_page': self.current_page,
            'page_size': self.page_size,
            'has_next': self.has_next,
            'has_previous': self.has_previous,
            'item_count': self.item_count,
            'start_index': self.start_index,
            'end_index': self.end_index,
            'is_empty': self.is_empty
        }
    
    @classmethod
    def empty(cls, page: int = 1, page_size: int = 20) -> 'PaginatedResult[T]':
        """Create an empty paginated result."""
        return cls(
            items=[],
            total_count=0,
            page_count=0,
            current_page=page,
            page_size=page_size,
            has_next=False,
            has_previous=False
        )
