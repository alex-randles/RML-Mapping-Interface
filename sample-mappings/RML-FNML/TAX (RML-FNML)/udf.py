__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "arenas.guerrero.julian@outlook.com"


@udf(
    fun_id='http://example.com/toUpperCase',
    text='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def to_upper_case(text):
    return text.lower()


@udf(
    fun_id='http://example.com/calculateTax',
    salary='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def calculate_tax(salary):
    tax = int(salary) * 0.2
    take_home_salary = int(salary) - tax
    return str(take_home_salary)
