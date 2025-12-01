import os
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto, InvalidTilavuus

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# In-memory storage for varastos
varastos = {}

@app.route('/')
def index():
    """Display all varastos"""
    return render_template('index.html', varastos=varastos)

@app.route('/create', methods=['POST'])
def create_varasto():
    """Create a new varasto"""
    try:
        name = request.form.get('name', '').strip()
        tilavuus = float(request.form.get('tilavuus', 0))

        if not name:
            flash('Varaston nimi on pakollinen', 'error')
            return redirect(url_for('index'))

        if name in varastos:
            flash(f'Varasto nimellä "{name}" on jo olemassa', 'error')
            return redirect(url_for('index'))

        varasto = Varasto(tilavuus)
        varastos[name] = varasto
        flash(f'Varasto "{name}" luotu onnistuneesti', 'success')
    except InvalidTilavuus:
        flash('Tilavuuden täytyy olla positiivinen luku', 'error')
    except ValueError:
        flash('Virheellinen tilavuus. Anna positiivinen numero.', 'error')
    except Exception:  # pylint: disable=broad-exception-caught
        flash('Virhe luotaessa varastoa', 'error')

    return redirect(url_for('index'))

@app.route('/add/<name>', methods=['POST'])
def add_to_varasto(name):
    """Add amount to a varasto"""
    try:
        if name not in varastos:
            flash(f'Varastoa "{name}" ei löydy', 'error')
            return redirect(url_for('index'))

        maara = float(request.form.get('maara', 0))

        if maara <= 0:
            flash('Määrän täytyy olla positiivinen luku', 'error')
            return redirect(url_for('index'))

        varastos[name].lisaa_varastoon(maara)
        flash(f'Lisätty {maara} varastoon "{name}"', 'success')
    except ValueError:
        flash('Virheellinen määrä. Anna positiivinen numero.', 'error')
    except Exception:  # pylint: disable=broad-exception-caught
        flash('Virhe lisättäessä varastoon', 'error')

    return redirect(url_for('index'))

@app.route('/take/<name>', methods=['POST'])
def take_from_varasto(name):
    """Take amount from a varasto"""
    try:
        if name not in varastos:
            flash(f'Varastoa "{name}" ei löydy', 'error')
            return redirect(url_for('index'))

        maara = float(request.form.get('maara', 0))

        if maara <= 0:
            flash('Määrän täytyy olla positiivinen luku', 'error')
            return redirect(url_for('index'))

        saatu = varastos[name].ota_varastosta(maara)
        flash(f'Otettu {saatu} varastosta "{name}"', 'success')
    except ValueError:
        flash('Virheellinen määrä. Anna positiivinen numero.', 'error')
    except Exception:  # pylint: disable=broad-exception-caught
        flash('Virhe otettaessa varastosta', 'error')

    return redirect(url_for('index'))

@app.route('/delete/<name>', methods=['POST'])
def delete_varasto(name):
    """Delete a varasto"""
    try:
        if name not in varastos:
            flash(f'Varastoa "{name}" ei löydy', 'error')
        else:
            del varastos[name]
            flash(f'Varasto "{name}" poistettu', 'success')
    except Exception:  # pylint: disable=broad-exception-caught
        flash('Virhe poistettaessa varastoa', 'error')

    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(_error):
    """Handle 404 errors"""
    flash('Sivua ei löytynyt', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(_error):
    """Handle 500 errors"""
    flash('Sisäinen palvelinvirhe', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
