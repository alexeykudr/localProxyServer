import sqlite3


conn = sqlite3.connect('database.db')
cur = conn.cursor()
name = 'qwerty'
portid = "11"
cur.execute('UPDATE proxyPorts SET generatedURL = ? where router_id = ?', (name, 11))
conn.commit()


# print(res)
conn.close()
# cur.execute("insert into proxyPorts values (?, ?)", ("C", 1972))

# UPDATE proxyPorts SET generatedUrl = ? where router_id = ? RETURNING router_id