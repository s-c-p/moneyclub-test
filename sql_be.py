"""
This code uses CTE and SQL-spec functions like sum, avg and round to return
the result in one go, this is faster because all calculations take place
inside DB, Python just takes care of fetch and present.

Code is self-explainatory.
"""

query = """
WITH vvpat AS (
    SELECT
        customer_id as person,
        date_part('year', age(date_of_birth)) as curr_age, -- no meaningful/predefined way to "round" age
        CAST(CASE
            WHEN txn_type = 'DEBIT' THEN -1*txn_amount
            WHEN txn_type = 'CREDIT' THEN txn_amount
        END AS numeric) transaction_amt
    FROM Customers
    INNER JOIN Transactions USING (customer_id)
    WHERE transaction_date >= '{tgt_date} 00:00:00'
    AND transaction_date < '{tgt_date} 00:00:00'::timestamp + interval '86401 seconds'
)
SELECT
    curr_age,
    round(avg(sumval), 2)
FROM (
    SELECT
        person,
        curr_age,
        sum(transaction_amt) as sumval
    FROM vvpat
    GROUP BY person, curr_age -- thanks to so/a/11107719
) temp_tbl
GROUP BY curr_age
"""

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

def calculate_savings(payload, context):
    try:
        host = payload["host"]
        port = payload["port"]
        database = payload["database"]
        username = payload["username"]
        password = payload["password"]
        tgt_date = '-'.join(list(payload["date"].split("/"))[::-1])
        dataset = get_data(database, username, password, host, port, tgt_date)
    except Exception as e:
        return {
            "statusCode": 400,
            "message": str(e)
        }
    else:
        return {
            "statusCode": 200,
            "data": {
                int(age): float(avg)
                for (age, avg) in dataset
            }
        }

if __name__ == '__main__':
    from secrets import events
    from pprint import pprint
    pprint(calculate_savings(events, None))
