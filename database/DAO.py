from database.DB_connect import DBConnect
from model.arco import Arco
from model.regista import Regista


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getRating():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct r.total_votes as punteggio
                    from ratings r 
                    order by r.total_votes desc"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["punteggio"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(avg1,avg2):
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct n.*
                    from ratings r , director_mapping dm , names n , movie m 
                    where r.total_votes between %s and %s and dm.name_id = n.id and m.id = r.movie_id and dm.movie_id =m.id and n.date_of_birth is not null  
"""
        cursor.execute(query,(avg1,avg2,))
        for row in cursor:
            res.append(Regista(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getArchi(avg1,avg2,idMap):
        conn = DBConnect.get_connection()
        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select dm1.name_id as nodo1 , dm2.name_id as nodo2, sum(m1.duration ) as peso 
from director_mapping dm1 , movie m1 , director_mapping dm2
where dm1.movie_id = m1.id and dm2.movie_id = m1.id and dm1.movie_id =dm2.movie_id and dm1.name_id <dm2.name_id and m1.duration is not null
and dm1.name_id in (select distinct n.id
from ratings r , director_mapping dm , names n , movie m 
where r.total_votes between %s and %s and dm.name_id = n.id and m.id = r.movie_id and dm.movie_id =m.id and n.date_of_birth is not null  
) and dm2.name_id in (select distinct n.id
from ratings r , director_mapping dm , names n , movie m 
where r.total_votes between %s and %s and dm.name_id = n.id and m.id = r.movie_id and dm.movie_id =m.id and n.date_of_birth is not null  
)
group by dm1.name_id , dm2.name_id 
"""
        cursor.execute(query,(avg1,avg2,avg1,avg2))
        for row in cursor:
            res.append(Arco(idMap.get(row["nodo1"]),idMap.get(row["nodo2"]),row["peso"]))

        cursor.close()
        conn.close()
        return res
