from flask import Flask, render_template, request, redirect, url_for, flash
from dataaccess import dataaccess

app = Flask(__name__)
app.secret_key = b"cosmocargosecretkey_buawhaha"

@app.route("/")
def show_shipments():
    shipments = dataaccess.get_shipments()
    headers = ( "Shipment Time",
                "Weight (Kg)",
                "Volume (M3)",
                "ETA (min)",
                "Status",
                "Forecast Origin Wind Velocity",
                "Forecast Origin Wind Direction",
                "Forecast Origin Precipitation Chance",
                "Forecast Origin Precipitation Kind",
                "Origin Solar System",
                "Origin Planet",
                "Origin Country",
                "Origin Address",
                "Destination Solar System",
                "Destination Planet",
                "Destination Country",
                "Destination Address")
    return render_template("shipments.html", headers=headers, data=shipments)

@app.route("/shipment/<int:id>", methods=['GET', 'POST'])
def view_shipment(id):
    if request.method == 'GET':
        request.args.get('id')
        
        shipment = dataaccess.get_shipment(id)
        ref_data = {
            "shipment_status": dataaccess.get_ref_data("shipment_status"),
            "precipitation_kinds": dataaccess.get_ref_data("precipitation_kind"),
            "solar_systems": dataaccess.get_ref_data("solar_system"),
            "planets": dataaccess.get_ref_data("planet"),
            "countries": dataaccess.get_ref_data("country"),
        }

        return render_template("shipment.html", data=shipment, ref_data=ref_data)
    
    else:
        err = dataaccess.update_shipment(id, request.form)
        if err != None:
            flash(str(err), "list-group-item list-group-item-danger")

        return redirect(url_for('show_shipments'))

