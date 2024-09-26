import pymysql
# import bcrypt

# mariadb root: @[mdb_Root#9]
# phpmyadmin root: @[pma_Root#9]

# informasi database
db_host = 'localhost'
db_user = 'alisatia'
db_password = '@[db_aliSatia#9]'
db_database = 'itbpress_erp'
db_cursorclass = pymysql.cursors.DictCursor

# autentikasi (belum tambah bcrypt)
def get_user(ag_email, ag_password):
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, cursorclass=db_cursorclass)

    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM pi_user WHERE u_email = %s AND u_password = %s"
            cursor.execute(query, (ag_email, ag_password))
            user = cursor.fetchone()

        if user:
            return {"status": "success", 'sid': user['u_uniq']}
        else:
            return {"status": "failed"}

    except Exception as e:
        print("Error:", str(e))
        return {"status": "error", "message": str(e)}

    finally:
        conn.close()

# cari produk / page
def get_page_product(ag_page, ag_per_page, ag_offset):
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, cursorclass=db_cursorclass)

    try:
        with conn.cursor() as cursor:
            sql_products = "SELECT * FROM pi_product LIMIT %s OFFSET %s"
            cursor.execute(sql_products, (ag_per_page, ag_offset))
            products = cursor.fetchall()

            sql_total_pages = "SELECT CEIL(COUNT(*) / %s) AS total_pages FROM pi_product"
            cursor.execute(sql_total_pages, (ag_per_page,))
            total_pages = cursor.fetchone()['total_pages']

        if products:
            return {
                'status': 'success',
                'data': {
                    'products': products,
                    'total_pages': total_pages,
                    'current_page': ag_page
                }
            }
        else:
            return {'status': 'empty'}

    except Exception as e:
        print("Error:", str(e))
        return {'status': 'error', 'message': str(e)}

    finally:
        conn.close()

# cari produk / term
def get_search_product(ag_search_term):
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, cursorclass=db_cursorclass)

    try:
        with conn.cursor() as cursor: 
            sql = "SELECT * FROM `pi_product` WHERE `p_code` LIKE %s OR `p_description` LIKE %s OR `p_price` LIKE %s"
            cursor.execute(sql, (ag_search_term, ag_search_term, ag_search_term))
            products = cursor.fetchall()

        if products:
            return {
                'status': 'success',
                'data': products
            }
        else:
            return {'status': 'empty'}

    except Exception as e:
        print("Error:", str(e))
        return {'status': 'error', 'message': str(e)}

    finally:
        conn.close()

