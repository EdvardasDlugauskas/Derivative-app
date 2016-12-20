from flask import Flask
from flask import render_template
from flask import request

from newformula import *
import sympy

app = Flask(__name__)
app.jinja_env.line_statement_prefix = '#'


@app.route("/", methods=['GET', 'POST'])
def application():
    expression = ""
    answer = None
    error = ""
    all_symb = []
    delta_symb = []
    pretty = ''

    subs = {}
    derivatives = []
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            all_symb, delta_symb, non_delta_symb = all_delta_nondelta(expression)
            derivatives = partial_derivatives(expression, non_delta_symb)
        except Exception as e:
            error = "Could not understand formula (did you forget a '*'?)"
            print(e)

        try:
            subs = {smb: request.form[str(smb)] for smb in all_symb}
            with_deltas = indirect_observation_error(derivatives, delta_symb)
            pretty = sympy.printing.pretty(with_deltas, use_unicode=True)
            answer = with_deltas.subs(subs).evalf()
        except Exception as e:
            print(e)

    return render_template('main.html', expression=expression, values=subs, pretty=pretty,
                           answer=answer, variables=all_symb, error=error)


if __name__ == "__main__":
    app.run()