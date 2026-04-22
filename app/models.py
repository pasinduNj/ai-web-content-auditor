import re  
from pydantic import BaseModel, field_validator  

class URLRequest(BaseModel):
    url: str

    @field_validator('url')
    @classmethod
    def validate_url_format(cls, v):
        # Regular expression for basic URL validation
        url_pattern = re.compile(
            r'^(https?:\/\/)?'  # http:// or https://
            r'([\da-z\.-]+)\.'  # domain
            r'([a-z\.]{2,6})'   # extension
            r'([\/\w \.-]*)*\/?$' # path
        )
        
        if not url_pattern.match(v):
            
            raise ValueError('please provide valid URL format')
        return v

class AnalysisReport(BaseModel):
    """
    Ensures recommendations are well-structured and easy to consume programmatically.
    """
    url: str
    status: str
    data: dict