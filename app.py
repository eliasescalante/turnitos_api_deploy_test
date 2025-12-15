from flask import Flask, jsonify, request, render_template
from db import get_connection

app = Flask(__name__)

#ruta get medicos
@app.route("/medicos", methods=["GET"])
def get_medicos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM medicos")
    medicos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(medicos), 200

# ruta get turnos con id medicos
@app.route("/turnos/<int:medico_id>", methods=["GET"])
def get_turnos_medico(medico_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
            SELECT id, fecha_hora, nombre_paciente
            FROM turnos
            WHERE medico_id = %s
            ORDER BY fecha_hora
        """
    , (medico_id,))

    turnos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(turnos), 200

#ruta post turnos
@app.route("/turnos", methods=["POST"])
def reservar_turno():
    data = request.get_json()

    medico_id = data.get("medico_id")
    fecha_hora = data.get("fecha_hora")
    paciente = data.get("paciente")

    if not medico_id or not fecha_hora or not paciente:
        return({"error":"Datos incompletos"}), 400
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
            SELECT id FROM turnos
            WHERE medico_id = %s AND fecha_hora = %s
        """
    , (medico_id, fecha_hora))

    turno_existence = cursor.fetchone()

    if turno_existence:
        cursor.close()
        conn.close()
        return jsonify({"message": "Turno no disponible"}), 400
    
    cursor.execute(
        """
            INSERT INTO turnos (medico_id, fecha_hora, nombre_paciente)
            VALUES (%s, %s, %s)
        """,
        (medico_id, fecha_hora, paciente)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Turno reservado correctamente"}), 201
    
@app.route("/")
def home():
    return render_template("guia.html")

if __name__ == "__main__":
    app.run()
