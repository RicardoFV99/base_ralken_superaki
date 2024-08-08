from pydantic import BaseModel
from typing import Dict, Any

class DialogflowPOST(BaseModel):
    responseId: str
    queryResult: Dict[str, Any]
    
    