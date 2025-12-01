import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto, InvalidTilavuus

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get(
    'SECRET_KEY', 'dev-secret-key-change-in-production'
)


class VarastoManager:
    """Manages a collection of Varasto instances"""

    def __init__(self):
        self._varastos = {}

    def get_all(self):
        """Return all varastos"""
        return self._varastos

    def get(self, name):
        """Get a varasto by name"""
        return self._varastos.get(name)

    def exists(self, name):
        """Check if a varasto exists"""
        return name in self._varastos

    def create(self, name, tilavuus):
        """Create a new varasto"""
        if name in self._varastos:
            raise ValueError(f"Varasto '{name}' already exists")
        varasto = Varasto(tilavuus)
        self._varastos[name] = varasto
        return varasto

    def delete(self, name):
        """Delete a varasto"""
        if name not in self._varastos:
            raise KeyError(f"Varasto '{name}' not found")
        del self._varastos[name]


varasto_manager = VarastoManager()

@app.route('/')
def index():
    """Display all varastos"""
    return render_template('index.html', varastos=varasto_manager.get_all())

@app.route('/create', methods=['POST'])
def create_varasto():
    """Create a new varasto"""
    try:
        name = request.form.get('name', '').strip()
        tilavuus = float(request.form.get('tilavuus', 0))

        if not name:
            flash('Varaston nimi on pakollinen', 'error')
            return redirect(url_for('index'))

        varasto_manager.create(name, tilavuus)
        flash(f'Varasto "{name}" luotu onnistuneesti', 'success')
    except InvalidTilavuus:
        flash('Tilavuuden täytyy olla positiivinen luku', 'error')
    except ValueError as e:
        if "already exists" in str(e):
            flash(f'Varasto nimellä "{name}" on jo olemassa', 'error')
        else:
            flash('Virheellinen tilavuus. Anna positiivinen numero.', 'error')
    except Exception as e:
        logger.error("Unexpected error in create_varasto: %s", e, exc_info=True)
        flash('Virhe luotaessa varastoa', 'error')

    return redirect(url_for('index'))

@app.route('/add/<name>', methods=['POST'])
def add_to_varasto(name):
    """Add amount to a varasto"""
    try:
        varasto = varasto_manager.get(name)
        if not varasto:
            flash(f'Varastoa "{name}" ei löydy', 'error')
            return redirect(url_for('index'))

        maara = float(request.form.get('maara', 0))

        if maara <= 0:
            flash('Määrän täytyy olla positiivinen luku', 'error')
            return redirect(url_for('index'))

        varasto.lisaa_varastoon(maara)
        flash(f'Lisätty {maara} varastoon "{name}"', 'success')
    except ValueError:
        flash('Virheellinen määrä. Anna positiivinen numero.', 'error')
    except Exception as e:
        logger.error("Unexpected error in add_to_varasto: %s", e, exc_info=True)
        flash('Virhe lisättäessä varastoon', 'error')

    return redirect(url_for('index'))

@app.route('/take/<name>', methods=['POST'])
def take_from_varasto(name):
    """Take amount from a varasto"""
    try:
        varasto = varasto_manager.get(name)
        if not varasto:
            flash(f'Varastoa "{name}" ei löydy', 'error')
            return redirect(url_for('index'))

        maara = float(request.form.get('maara', 0))

        if maara <= 0:
            flash('Määrän täytyy olla positiivinen luku', 'error')
            return redirect(url_for('index'))

        saatu = varasto.ota_varastosta(maara)
        flash(f'Otettu {saatu} varastosta "{name}"', 'success')
    except ValueError:
        flash('Virheellinen määrä. Anna positiivinen numero.', 'error')
    except Exception as e:
        logger.error(
            "Unexpected error in take_from_varasto: %s", e, exc_info=True
        )
        flash('Virhe otettaessa varastosta', 'error')

    return redirect(url_for('index'))

@app.route('/delete/<name>', methods=['POST'])
def delete_varasto(name):
    """Delete a varasto"""
    try:
        varasto_manager.delete(name)
        flash(f'Varasto "{name}" poistettu', 'success')
    except KeyError:
        flash(f'Varastoa "{name}" ei löydy', 'error')
    except Exception as e:
        logger.error("Unexpected error in delete_varasto: %s", e, exc_info=True)
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
