"""
This code requests just 4 columns from DB (to reduce bandwidth and memory).
It then arranges data per customer by Customer class and finally condenses
it using mean and sum functions over the list of customers.
This is slower because fetching takes almost same time but Python must do all
calculations locally.

Code is self-explainatory.
"""

from datetime import date
from typing import NamedTuple, List, Mapping, Optional

class Customer(NamedTuple):
    customer_id: str
    age: int
    transactions: List[float]

query = """
SELECT customer_id, date_of_birth, txn_type, txn_amount
  FROM Customers
 INNER JOIN Transactions
 USING (customer_id)
 WHERE transaction_date >= '{tgt_date} 00:00:00'
   AND transaction_date < '{tgt_date} 00:00:00'::timestamp + interval '86401 seconds'
"""

mean = lambda v: round(sum(v)/len(v), 2)

def get_data(database, username, password, host, port, tgt_date):
    try:
        import psycopg2
        conn = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
    except:
        raise RuntimeError("Unable to connect to database")
    try:
        cursor.execute(query.format(tgt_date=tgt_date))
        dataset = cursor.fetchall()
    except:
        raise RuntimeError("Perhaps bad date string input")
    finally:
        conn.close()
    return dataset

def calc_age(dob):
    # thanks to so/a/9754466
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def calc_stats(dataset):
    init_dict = dict()
    for row in dataset:
        customer_id = row[0]
        dob = row[1]
        txn = float(row[3]) if row[2] == 'CREDIT' else -1*float(row[3])
        try:
            init_dict[customer_id].transactions.append(txn)
        except KeyError:
            init_dict[customer_id] = Customer(customer_id, calc_age(dob), [txn])
    answer = dict()
    for v in init_dict.values():
        try:
            answer[v.age].append(sum(v.transactions))
        except KeyError:
            answer[v.age] = [sum(v.transactions)]
    return {k: mean(v) for k, v in answer.items()}

def calculate_savings(payload, context):
    try:
        host = payload["host"]
        port = payload["port"]
        database = payload["database"]
        username = payload["username"]
        password = payload["password"]
        tgt_date = '-'.join(list(payload["date"].split("/"))[::-1])
        dataset = get_data(database, username, password, host, port, tgt_date)
        answer = calc_stats(dataset)
    except Exception as e:
        return {
            "statusCode": 400,
            "message": str(e)
        }
    else:
        return {
            "statusCode": 200,
            "data": answer
        }

if __name__ == '__main__':
    from secrets import events
    from pprint import pprint
    pprint(calculate_savings(events, None))
