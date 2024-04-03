from typing import Generic, TypeVar
import pyodbc

from Metrik.exceptions import ObjectDoesNotExists
settings = __import__("settings")

T = TypeVar('T', bound='OrmManager')
class OrmManager(Generic[T]):
    
    _connection = None
    def _get_or_create_connection(self) -> pyodbc.Connection:
        if self._connection is None:
            self._connection = pyodbc.connect(
                driver=settings.DB_DRIVER,
                database=settings.DB_NAME,
                server=settings.DB_SERVER,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
            )
            
        return self._connection
    
    def __get__(self, instance, owner):
        self.owner = owner
        
        
        
        self.connection = self._get_or_create_connection()
        
        return self

    def create(self, **kwargs) -> T:
        cursor = self.connection.cursor()
        
        sql = f"""
        INSERT INTO {self.owner.__tablename_plural__} ({', '.join(list(kwargs.keys()))}) VALUES ({', '.join(['?']*len(kwargs))})
        """
        
        
        cursor.execute(sql, list(kwargs.values()))
        cursor.commit()
        return self.owner(**kwargs)
    
    def all(self) -> list[T]:
        cursor = self.connection.cursor()
        sql = f"SELECT * FROM {self.owner.__name__}"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        rows = [self.owner(**dict(zip(columns, row))) for row in cursor.fetchall()] #cursor.fetchall()
        return rows
    
    
    def where_clause_generate(self, **kwargs):
        where_clause = 'WHERE ' + ' AND '.join([k +' = ' + str(v) for k, v in kwargs.items()])
        return where_clause
    
    
    def filter(self, **kwargs) -> list[T]:
        cursor = self.connection.cursor()
        sql = f"""
        SELECT * FROM {self.owner.__name__} {self.where_clause_generate(**kwargs)}"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        rows = [self.owner(**dict(zip(columns, row))) for row in cursor.fetchall()] #cursor.fetchall()
        return rows
    
    def update(self, where_clause: str, **kwargs):
        cursor = self.connection.cursor()
        if where_clause:
            sql = f"""
            UPDATE {self.owner.__name__} SET {', '.join([k +' = ?' for k in kwargs.keys()])} {where_clause}"""
        else:
            sql = f"""
            UPDATE {self.owner.__name__} SET {', '.join([k +' = ?' for k in kwargs.keys()])}"""
        cursor.execute(sql, list(kwargs.values()))
        cursor.commit()
        return self.owner(**kwargs)
    
    def get(self, **kwargs) -> T:
        
        results = self.filter(**kwargs)
        if len(results) == 0:
            raise ObjectDoesNotExists(self.owner, **kwargs)

        return results[0]
    
    def delete(self, **kwargs):
        cursor = self.connection.cursor()
        sql = f"""
        DELETE FROM {self.owner.__name__} {self.where_clause_generate(**kwargs)}"""
        cursor.execute(sql)
        cursor.commit()
        return True