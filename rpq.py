"""
    File name: rpq.py
    Author: Temur Malishava
"""
import textwrap
import config

counter = 0


# config.sql_full = ""


class RPQ_Predicate:
    """
    A class used to represent an RPQ Predicate
    Example: a
    """

    def __init__(self, pred):
        """
        :param pred: a predicate name
        :type pred: str
        """
        self.pred = pred

    def __str__(self):
        """
        :return: human readable version of the predicate
        :rtype: str
        """
        return f"{self.pred}"

    def eval(self):
        """
        Prints an SQL version of the RPQ and returns a name of the created common table expression

        :return: name of the created common table expression
        :rtype: str
        """
        return self.sql_translation()

    def sql_translation(self):
        """
        Prints the SQL query after translating an RPQ to an SQL and
        returns a name of the created common table expression

        :return: name of the created common table expression needed for recursion
        :rtype: str
        """
        global counter
        counter += 1
        if counter == 1:
            start = "WITH RECURSIVE "
        else:
            start = ""
        sql_query = textwrap.dedent(f"""\
                                    {start}cte_{counter}(x, y) AS(
                                    SELECT g.x, g.y
                                    FROM graph g
                                    WHERE g.r = '{self.pred}'
                                    ),
                                    """)
        # global sql_full
        config.sql_full += sql_query

        return f"cte_{counter}"


class RPQ_Plus:
    """
    A class used to represent an RPQ with a repetition operator plus defined by a character ‘+’
    Example: a+
    """

    def __init__(self, subRPQ):
        """
        :param subRPQ: sub RPQ of the current RPQ
        :type subRPQ: RPQ_Predicate or RPQ_Plus or RPQ_Concat or RPQ_Or
        """
        self.subRPQ = subRPQ

    def eval(self):
        """
        Prints an SQL version of the sub RPQ and returns a name of the created common table expression

        :return: name of the created common table expression
        :rtype: str
        """
        return self.sql_translation()

    def sql_translation(self):
        """
        Prints the SQL query after translating an RPQ to an SQL and
        returns a name of the created common table expression

        :return: name of the created common table expression
        :rtype: str
        """
        sub = self.subRPQ.eval()

        global counter
        counter += 1
        sql_query = textwrap.dedent(f"""\
                                    cte_{counter}(x, y) AS(
                                    SELECT x, y
                                    FROM {sub} g
                                    UNION
                                    SELECT c.x, g.y
                                    FROM cte_{counter} c, {sub} g
                                    WHERE c.y = g.x
                                    ),
                                    """)
        # global sql_full
        config.sql_full += sql_query

        return f"cte_{counter}"


class RPQ_Concat:
    """
    A class used to represent concatenated RPQs defined by a character ‘/’
    Example: a/b
    """

    def __init__(self, left_subRPQ, right_subRPQ):
        """
        :param left_subRPQ: left sub RPQ of the concatenated RPQ
        :type left_subRPQ: RPQ_Predicate or RPQ_Plus or RPQ_Concat or RPQ_Or
        :param right_subRPQ: right sub RPQ of the concatenated RPQ
        :type right_subRPQ: RPQ_Predicate or RPQ_Plus or RPQ_Concat or RPQ_Or
        """
        self.left_subRPQ = left_subRPQ
        self.right_subRPQ = right_subRPQ

    def eval(self):
        """
        Prints an SQL version of the sub RPQ and returns a name of the created common table expression

        :return: name of the created common table expression
        :rtype: str
        """
        return self.sql_translation()

    def sql_translation(self):
        """
        Prints the SQL query after translating an RPQ to an SQL and
        returns a name of the created common table expression

        :return: name of the created common table expression
        :rtype: str
        """
        left = self.left_subRPQ.eval()
        right = self.right_subRPQ.eval()

        global counter
        counter += 1
        sql_query = textwrap.dedent(f"""\
                                    cte_{counter}(x, y) AS(
                                    SELECT l.x, r.y
                                    FROM {left} l, {right} r
                                    WHERE l.y = r.x 
                                    ),
                                    """)
        # global sql_full
        config.sql_full += sql_query

        return f"cte_{counter}"


class RPQ_Or:
    """
    A class used to represent an RPQ with an operator OR defined by a char '|'
    Example: a|b
    """

    def __init__(self, left_subRPQ, right_subRPQ):
        """
        :param left_subRPQ: left sub RPQ of the joint RPQ
        :type left_subRPQ: RPQ_Predicate or RPQ_Plus or RPQ_Concat or RPQ_Or
        :param right_subRPQ: right sub RPQ of the joint RPQ
        :type right_subRPQ: RPQ_Predicate or RPQ_Plus or RPQ_Concat or RPQ_Or
        """
        self.left_subRPQ = left_subRPQ
        self.right_subRPQ = right_subRPQ

    def eval(self):
        """
        Prints an SQL version of the sub RPQ and returns a name of the created common table expression

        :return: name of the created common table expression
        :rtype: str
        """
        return self.sql_translation()

    def sql_translation(self):
        """
        Prints the SQL query after translating an RPQ to an SQL and
        returns a name of the created common table expression

        :return: name of the created common table expression
        :rtype: str
        """
        left = self.left_subRPQ.eval()
        right = self.right_subRPQ.eval()

        global counter
        counter += 1
        sql_query = textwrap.dedent(f"""\
                                    cte_{counter}(x, y) AS(
                                    SELECT l.x, l.y FROM {left} l
                                    UNION
                                    SELECT r.x, r.y FROM {right} r
                                    ),
                                    """)
        # global sql_full
        config.sql_full += sql_query

        return f"cte_{counter}"


class RPQ_S:
    """
    A class used to reform the RPQ_Concat which includes and RPQ_Plus into an RPQ_Or
    Example: a+/b -> a*/(a/b) -> (a/b) | a+/(a/b)
    """

    def __init__(self, left, base, right):
        """
        :param left: left RPQ object of the joint RPQ
        :type left: RPQ_Predicate or RPQ_Plus or None
        :param base: the base RPQ object of the joint RPQ which is the main part of the output
        :type base: RPQ_Predicate or RPQ_Concat
        :param right: right RPQ object of the joint RPQ
        :type right: RPQ_Predicate or RPQ_Plus or None
        """
        self.left = left
        self.base = base
        self.right = right

    def eval(self):
        """
        Prints an SQL version of the sub RPQ and returns a name of the created common table expression

        :return: name of the created common table expression
        :rtype: str
        """
        return self.sql_translation()

    def sql_translation(self):
        """
        Prints the SQL query after translating an RPQ to an SQL and
        returns a name of the created common table expression

        :return: name of the created common table expression
        :rtype: str
        """

        cte = self.base.eval()

        global counter
        left_counter = counter - 2  # a
        right_counter = counter - 1  # b
        counter += 1
        if self.left is not None and self.right is not None:
            sql_query = textwrap.dedent(f"""\
                                        cte_{counter}(x, y) AS(
                                        SELECT x, y
                                        FROM {cte} g
                                        UNION
                                        SELECT g.x, c.y
                                        FROM cte_{counter} c, cte_{left_counter} g
                                        WHERE g.y = c.x
                                        ),
                                        
                                        cte_{counter+1}(x, y) AS(
                                        SELECT x, y
                                        FROM cte_{counter} g
                                        UNION
                                        SELECT c.x, g.y
                                        FROM cte_{counter+1} c, cte_{right_counter} g
                                        WHERE c.y = g.x
                                        ),
                                        """)

            counter += 1  # because of the second cte

        elif self.right is None:
            sql_query = textwrap.dedent(f"""\
                                        cte_{counter}(x, y) AS(
                                        SELECT x, y
                                        FROM {cte} g
                                        UNION
                                        SELECT g.x, c.y
                                        FROM cte_{counter} c, cte_{left_counter} g
                                        WHERE g.y = c.x
                                        ),
                                        """)

        elif self.left is None:
            sql_query = textwrap.dedent(f"""\
                                        cte_{counter}(x, y) AS(
                                        SELECT x, y
                                        FROM {cte} g
                                        UNION
                                        SELECT c.x, g.y
                                        FROM cte_{counter} c, cte_{right_counter} g
                                        WHERE c.y = g.x
                                        ),
                                        """)

        config.sql_full += sql_query
        return f"cte_{counter}"


# Pa = RPQ_Predicate("a")
# Pb = RPQ_Predicate("b")
#
# Pab = RPQ_Or(Pa, Pb)
#
# final_cte = Pab.sql_translation()
#
# print(config.sql_full[:-2])
# print(f"SELECT x,y FROM {final_cte}")
