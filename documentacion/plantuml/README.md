# Diagramas C4 en PlantUML

Esta carpeta contiene los diagramas C4 del sistema en formato PlantUML.

## Archivos

1. **01_system_context.puml** - Diagrama de Contexto del Sistema (Nivel 1)
2. **02_container.puml** - Diagrama de Contenedores (Nivel 2)
3. **03_component.puml** - Diagrama de Componentes (Nivel 3)
4. **04_deployment.puml** - Diagrama de Despliegue (Nivel 4)

## Cómo visualizar los diagramas

### Opción 1: Visual Studio Code

1. Instalar la extensión [PlantUML](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml)
2. Abrir cualquier archivo `.puml`
3. Presionar `Alt + D` para previsualizar

### Opción 2: PlantUML Online

1. Ir a http://www.plantuml.com/plantuml/uml/
2. Copiar el contenido del archivo `.puml`
3. Pegar en el editor web
4. El diagrama se genera automáticamente

### Opción 3: PlantUML Local

```bash
# Instalar PlantUML (requiere Java)
# Windows (con Chocolatey):
choco install plantuml

# Mac (con Homebrew):
brew install plantuml

# Linux (Ubuntu/Debian):
sudo apt-get install plantuml

# Generar imagen PNG
plantuml 01_system_context.puml

# Generar todas las imágenes
plantuml *.puml
```

### Opción 4: Extensiones de navegador

- Chrome: [PlantUML Viewer](https://chrome.google.com/webstore/detail/plantuml-viewer)
- Firefox: PlantUML Visualizer

## Exportar diagramas

Los diagramas se pueden exportar a:
- PNG (imagen raster)
- SVG (vector escalable)
- PDF (documento)
- ASCII Art (texto)

```bash
# PNG
plantuml -tpng diagrama.puml

# SVG
plantuml -tsvg diagrama.puml

# PDF
plantuml -tpdf diagrama.puml
```

## Modelo C4

Los diagramas siguen el modelo C4 (Context, Containers, Components, Code):
- **Nivel 1 - Contexto**: Vista general del sistema y sus usuarios
- **Nivel 2 - Contenedores**: Aplicaciones y servicios principales
- **Nivel 3 - Componentes**: Estructura interna de los contenedores
- **Nivel 4 - Despliegue**: Infraestructura de producción

Más información: https://c4model.com/
