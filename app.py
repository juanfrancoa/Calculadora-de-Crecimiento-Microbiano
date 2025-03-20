from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Lista de microorganismos con su tiempo de generación en minutos
microorganismos = {
    "Escherichia coli": 20,
    "Staphylococcus aureus": 30,
    "Bacillus subtilis": 26,
    "Pseudomonas aeruginosa": 40,
    "Salmonella enterica": 35,
    "Lactobacillus acidophilus": 50,
    "Clostridium perfringens": 10,
    "Mycobacterium tuberculosis": 900,
    "Saccharomyces cerevisiae": 90,
    "Vibrio cholerae": 24
}

@app.route("/", methods=["GET", "POST"])
def index():
    Nt = Ni = n = tg = tiempo_incubacion = None
    mensaje_error = None
    seleccionado = None

    if request.method == "POST":
        try:
            # Obtener datos del formulario
            Nt_str = request.form.get("Nt")
            Ni_str = request.form.get("Ni")
            n_str = request.form.get("n")
            T_str = request.form.get("T")  # Tiempo de incubación
            micro_str = request.form.get("micro")
            tg_str = request.form.get("tg")  # Tiempo de generación ingresado manualmente

            # Convertir valores numéricos
            Nt = float(Nt_str) if Nt_str else None
            Ni = float(Ni_str) if Ni_str else None
            n = float(n_str) if n_str else None
            tiempo_incubacion = float(T_str) if T_str else None
            seleccionado = micro_str  # Microorganismo seleccionado

            # Usar el tiempo de generación ingresado o el predeterminado
            if tg_str:
                tg = float(tg_str)
            elif micro_str in microorganismos:
                tg = microorganismos[micro_str]

            # Calcular n con solo el tiempo de incubación y tg
            if n is None and tiempo_incubacion is not None and tg is not None:
                n = tiempo_incubacion / tg

            # Calcular cualquier variable faltante
            if Nt is None and Ni is not None and n is not None:
                Nt = Ni * (2 ** n)
            elif Ni is None and Nt is not None and n is not None:
                Ni = Nt / (2 ** n)
            elif n is None and Ni is not None and Nt is not None:
                n = math.log(Nt / Ni) / math.log(2)

            # Calcular el tiempo de generación (t_g) si se conoce T y n
            if tg is None and tiempo_incubacion is not None and n is not None:
                tg = tiempo_incubacion / n

        except ValueError as e:
            mensaje_error = f"Error: {str(e)}"

    return render_template("index.html", Nt=Nt, Ni=Ni, n=n, tg=tg,
                           tiempo_incubacion=tiempo_incubacion,
                           mensaje_error=mensaje_error,
                           microorganismos=microorganismos, seleccionado=seleccionado)

if __name__ == "__main__":
    app.run(debug=True)
