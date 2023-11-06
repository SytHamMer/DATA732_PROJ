import pandas as pd
import plotly.express as px

# Exemple de données (remplacez par vos propres données)
listPers = ['Personne1', 'Personne2', 'Personne3']
data = {
    'Personne1': [0.1, 0.2, 0.3],
    'Personne2': [0.4, 0.5, 0.6],
    'Personne3': [0.7, 0.8, 0.9],
}

matrice = pd.DataFrame(data, index=listPers, columns=listPers)

# Utilisez pd.melt() pour reformater les données
matrice_melted = matrice.reset_index().melt(id_vars='index')

# Utilisez px.density_heatmap avec les données reformulées
fig = px.density_heatmap(
    matrice_melted,
    x='index',
    y='variable',
    z='value',
)

# Personnalisez les noms d'axe si nécessaire
fig.update_xaxes(title="Axe X")
fig.update_yaxes(title="Axe Y")

# Affichez la figure
fig.show()



