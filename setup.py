# setup.py

from setuptools import setup, find_packages

setup(
    name='stock_predictor',
    version='1.0.0',
    description='Stock Market Prediction Project with LSTM, FastAPI, and Streamlit',
    author='Elias Martinelli',
    author_email='elias.martinelli@hotmail.com',
    packages=find_packages(include=['stock_predictor', 'stock_predictor.*']),
    install_requires=[
        'tensorflow>=2.8',
        'keras',
        'scikit-learn',
        'pandas',
        'numpy',
        'pandas_datareader',
        'fastapi',
        'uvicorn[standard]',
        'joblib',
        'streamlit',
        'python-dotenv',
        'keras-tuner',
        'matplotlib',
        'requests'
    ],
    include_package_data=True,
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    entry_points={
        'console_scripts': [
            'run-predictor=stock_predictor.__main__:main',
        ]
    }
)
