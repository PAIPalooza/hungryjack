"""
Supabase Client for HungryJack
This module provides a Python client for interacting with Supabase
"""

import os
import httpx
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseClient:
    """Client for interacting with Supabase from Python"""
    
    def __init__(self):
        """Initialize the Supabase client with environment variables"""
        self.supabase_url = os.getenv("SUPABASE_URL", "http://localhost:54321")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
        # Validate configuration
        if not self.supabase_key:
            raise ValueError("SUPABASE_SERVICE_KEY environment variable is not set")
    
    async def select(self, table: str, columns: str = "*", filters: Dict = None) -> List[Dict]:
        """
        Select data from a table
        
        Args:
            table: The table to select from
            columns: The columns to select (default: "*")
            filters: Optional filters to apply
            
        Returns:
            List of records
        """
        url = f"{self.supabase_url}/rest/v1/{table}?select={columns}"
        
        # Apply filters if provided
        if filters:
            for key, value in filters.items():
                url += f"&{key}=eq.{value}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def insert(self, table: str, data: Dict) -> Dict:
        """
        Insert data into a table
        
        Args:
            table: The table to insert into
            data: The data to insert
            
        Returns:
            The inserted record
        """
        url = f"{self.supabase_url}/rest/v1/{table}"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self.headers,
                json=data,
                params={"select": "*"}
            )
            response.raise_for_status()
            return response.json()[0] if response.json() else {}
    
    async def update(self, table: str, id_column: str, id_value: str, data: Dict) -> Dict:
        """
        Update data in a table
        
        Args:
            table: The table to update
            id_column: The column to use for identifying the record
            id_value: The value to match in the id_column
            data: The data to update
            
        Returns:
            The updated record
        """
        url = f"{self.supabase_url}/rest/v1/{table}"
        params = {
            "select": "*",
            f"{id_column}": f"eq.{id_value}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                url,
                headers=self.headers,
                json=data,
                params=params
            )
            response.raise_for_status()
            return response.json()[0] if response.json() else {}
    
    async def delete(self, table: str, id_column: str, id_value: str) -> Dict:
        """
        Delete data from a table
        
        Args:
            table: The table to delete from
            id_column: The column to use for identifying the record
            id_value: The value to match in the id_column
            
        Returns:
            The deleted record
        """
        url = f"{self.supabase_url}/rest/v1/{table}"
        params = {
            "select": "*",
            f"{id_column}": f"eq.{id_value}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                url,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()[0] if response.json() else {}
    
    async def execute_sql(self, query: str, params: Dict = None) -> List[Dict]:
        """
        Execute a raw SQL query
        
        Args:
            query: The SQL query to execute
            params: Optional parameters for the query
            
        Returns:
            Query results
        """
        url = f"{self.supabase_url}/rest/v1/rpc/execute_sql"
        data = {
            "query": query,
            "params": params or {}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()

# Create a singleton instance
supabase = SupabaseClient()
