import unittest
from final507proj import *


class TestDatabase(unittest.TestCase):

    def test_proj_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Director FROM AEFProjects'
        res = cur.execute(sql)
        res_list = res.fetchall()
        self.assertIn(('Janet Richards',), res_list)
        self.assertEqual(len(res_list), 102)

        sql = '''
            SELECT Year, Name, Director
            FROM AEFProjects
            WHERE Round=1
        '''
        res = cur.execute(sql)
        res_list = res.fetchall()
        self.assertEqual(len(res_list), 8)
        self.assertEqual(res_list[0][0], '2003')
        self.assertEqual(res_list[0][2], 'Peter Lacovara')

        conn.close()

    def test_rounds_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Year
            FROM Rounds
            WHERE RoundNumber=12
        '''
        res = cur.execute(sql)
        res_list = res.fetchall()
        self.assertIn((2014,), res_list)
        self.assertEqual(len(res_list), 1)

        sql = '''
            SELECT COUNT(*)
            FROM Rounds
        '''
        res = cur.execute(sql)
        count = res.fetchone()[0]
        self.assertEqual(count, 12)

        conn.close()


class Test_getting_data(unittest.TestCase):

    def test_getproj(self):
        res = get_projname(2003)
        self.assertIn('Predynastic', res[0])

        res = get_projname(2009)
        self.assertEqual('Chicago House Photographic Archive Documentation and Digital Backup Projects', res[0])



class TestInstitutions(unittest.TestCase):

    def test_inst(self):
        res = institutions(2009)
        self.assertFalse(res[0] == 'University of Chicago')

        res = institutions(2004)
        self.assertTrue(res[0] != 'Institute of Fine Arts')
        self.assertEqual(res[1], ' Temple University')

        res = institutions(2008)
        self.assertEqual(res[0],' University of Michigan')

        res = institutions(2008)
        self.assertEqual(res[1],' New York University')        

    



unittest.main()
