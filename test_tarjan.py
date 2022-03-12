from sat_solver import Variable, strongly_connected_components

res = strongly_connected_components({
    Variable('-0'): [Variable('1')],
    Variable('1'): [Variable('2')],
    Variable('2'): [Variable('3')],
    Variable('3'): [Variable('-0')],
    Variable('4'): [Variable('2'), Variable('3'), Variable('5')],
    Variable('5'): [Variable('4'), Variable('6')],
    Variable('6'): [Variable('3'), Variable('7')],
    Variable('7'): [Variable('6')],
    Variable('8'): [Variable('5'), Variable('7'), Variable('8')]
})

print(res)