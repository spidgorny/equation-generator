from html import escape

from flask import Flask, render_template
from sympy import symbols, init_printing, solveset, Eq, linsolve, FiniteSet
from sym import genEq2, solve, getSimpleEq2
from sympy.printing.mathml import print_mathml, mathml

app = Flask(__name__, static_url_path='', static_folder='static')


@app.route('/')
def hello_world():
    x, y = symbols('x y')
    eq1, eq2 = getSimpleEq2(x, y)
    res: FiniteSet = solve(eq1, eq2, x, y)

    val_x = tuple(res)[0][0]
    val_y = tuple(res)[0][1]

    eq = mml('<mfenced open="{" close=""><mtable>' +
             mathml(eq1, printer="presentation") +
             mathml(eq2, printer="presentation") +
             "</mtable></mfenced>")

    sol1 = solveset(eq1, x)
    sol1f = tuple(sol1)[0] or 1
    int1 = 0

    sol2 = solveset(eq2, y)
    sol2f = tuple(sol2)[0] or 1
    int2 = 0

    return render_template('2eq.html', eq=eq,
    					   eq1=str(sol1f),
    					   eq2=str(sol2f),
    					   int1=int1,
    					   int2=int2,
                           val_x=show_val(val_x),
                           val_y=show_val(val_y))


def mml(mathml):
    return '<math xmlns="http://www.w3.org/1998/Math/MathML">' + mathml + '</math>'


def show_val(val_x):
    html = mml(mathml(val_x, printer="presentation"))
    # html += " [" + escape(mathml(val_x, printer="presentation")) + "]"
    # html += " [" + str(val_x) + "]"
    return html


if __name__ == '__main__':
    app.run()
