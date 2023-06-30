# recipes-engine
Un _engine_ para recomendar recetas basado en grafos. Las bases de datos de las que nos nutrimos fueron el popular libro de la cubana Nitza Villapol *"Cocina al minuto"* y un repositorio de 5K recetas que puede visitar en este [enlace](http://www.ub.edu/cvub/recipes5k/).

Para ejecutar la aplicación visual basta con correr en la consola el siguiente comando:

`make run`

Esto abrirá un servidor de **Streamlit** en el `localhost:8501`. En la aplicación podrá realizar las consultas especificadas en el informe.

Requerimientos:
- Python >= 3.8
- networkx >= 3.1
- streamlit >= 1.17.0

**Nota: Puede ayudarnos a mejorar agregando ingredientes que a su parecer pueden ser sustituibles.**
