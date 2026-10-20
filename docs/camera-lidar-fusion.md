# Camera-LiDAR Fusion

## Description

O projeto de fusão Camera-LiDAR tem como objetivo a percepção e estimação de posição dos cones na pista, aproveitando das capacidades de inferência das redes neurais através da camera, e da extrema precisão das pointclouds geradas pelo LiDAR. Para isso, é necessario projetar os pontos 3D gerados pelo LiDAR, na imagem 2D da camera, isto é, saber onde cada ponto 3D estaria localizado na imagem se transformado em um ponto 2D. Dessa forma, conseguimos conversar os dois sensores pois ambos estão atuando no "mesmo mundo". Tudo isso é feito atraves de transformações lineares, 