from database.DB_connect import DBConnect
from model.order import Order

from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from orders o where o.store_id=%s """

        cursor.execute(query, (store.store_id, ))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(store,k,idMap):
            conn = DBConnect.get_connection()

            results = []

            cursor = conn.cursor(dictionary=True)
            query = """select o1.order_id as id1, o2.order_id as id2, ((sum(oi1.quantity)+sum(oi2.quantity))/ datediff(o2.order_date,o1.order_date)) as peso 
from orders o1, orders o2, stores s, order_items oi1, order_items oi2
where o1.store_id = s.store_id 
and o2.store_id = s.store_id
and o1.store_id = %s
and o2.store_id = o1.store_id
and o1.order_id = oi1.order_id 
and o2.order_id = oi2.order_id 
and o1.order_date < o2.order_date
and datediff(o2.order_date,o1.order_date) <= %s
group by o1.order_id, o2.order_id"""

            cursor.execute(query, (store.store_id,k))

            for row in cursor:
                results.append((idMap[row["id1"]], idMap[row["id2"]], row["peso"]))


            cursor.close()
            conn.close()
            return results