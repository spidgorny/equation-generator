from html import escape

from flask import Flask, render_template
from sympy import symbols, init_printing, solveset, Eq, linsolve, FiniteSet
from sym import genEq2, solve
from sympy.printing.mathml import print_mathml, mathml

app = Flask(__name__)


@app.route('/')
def hello_world():
    x, y = symbols('x y')
    eq1, eq2 = genEq2(x, y)
    res: FiniteSet = solve(eq1, eq2, x, y)

    val_x = tuple(res)[0][0]
    val_y = tuple(res)[0][1]

    eq = mml('<mfenced open="{" close=""><mtable>' +
             mathml(eq1, printer="presentation") +
             mathml(eq2, printer="presentation") +
             "</mtable></mfenced>")

    return render_template('2eq.html', eq=eq,
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
