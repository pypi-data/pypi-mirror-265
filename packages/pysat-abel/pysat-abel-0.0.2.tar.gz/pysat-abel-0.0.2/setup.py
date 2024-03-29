from setuptools import setup

setup(
    name='pysat-abel',
    vversion = "0.0.2",   
    description='Python implementation for Spline-based Abel Transform',
    url='https://gitlab.coria-cfd.fr/littinm/pysat',
    author='Mijail Littin, Alexandre Poux, Guillaume Lefevre, Marek Mazur, Felipe Escudero, Andrés Fuentes, Jérôme Yon',
    author_email='littinm@coria.fr',
    packages=['pysat'],
    dependencies = [ "scipy", "numpy", 'abel', 'joblib'],

    classifiers=[
        'Intended Audience :: Science/Research',
    ],
)