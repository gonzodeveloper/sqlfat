from bin import utility
import json

if __name__ == "__main__":
    code = 'CREATE TABLE t4 ( ' \
           'uid INT,' \
           'name VARCHAR NOT NULL,' \
           'PRIMARY KEY (uid) ) ' \
           'PARTITION BY RANGE(uid, 1, 100) ' \
           'PARTITIONS 3'
    code = 'INSERT INTO t1 (uid, name) ' \
           'VALUES ' \
           '    (11, "kyle"),' \
           '    (22, "sukkie"),' \
           '    (88, "mia")'

    code = 'SELECT uid, name FROM t4 WHERE uid > 50 AND name = "paul"'
    node1 = "200.0.0.11"
    node2 = "200.0.0.12"
    node3 = "200.0.0.13"

    nodes = [node1, node2, node3]
    util = utility.DbUtils(nodes)
    sql = util.parse(code)
    strs = util.get_node_strings()

    #util.enter_table_data()
    #print(util._get_table_meta("t4"))
    for s in strs:
        print(s)
    #print(json.dumps(sql, indent=4, separators=(',', ': ')))