from setuptools import setup, find_packages

setup(
    name="myToshokan",  # Nom de votre package
    version="1.0.2",  # Version de votre package
    author="Robin Messiaen",  # Ajoutez votre nom
    author_email="robin_messiaen@hotmail.fr",  # Ajoutez votre adresse email
    description="My library is your library.",  # Ajoutez une brève description
    long_description=open("README.md").read(),  # Ceci charge le contenu de README.md comme description longue
    long_description_content_type="text/markdown",  # Indique que la description longue est en Markdown
    packages=find_packages(),  # Découvre automatiquement tous les paquets
    include_package_data=True,  # Inclut les fichiers spécifiés dans MANIFEST.in
    install_requires=[
        # Ajoutez ici les dépendances nécessaires
        "requests",  # Exemple, remplacer par les dépendances réelles de votre package
    ],
    classifiers=[
        # Classificateurs de votre choix (https://pypi.org/classifiers/)
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Version minimale de Python requise
    entry_points={
        'console_scripts': [
            # Si vous avez des scripts que vous souhaitez rendre exécutables directement depuis le terminal
            # 'nom-du-script = nom_du_package.module:fonction'
        ],
    },
)
