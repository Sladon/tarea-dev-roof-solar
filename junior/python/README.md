# Tarea Dev Junior - Ruuf

## 🎯 Objetivo

El objetivo de este ejercicio es poder entender tus habilidades como programador/a, la forma en que planteas un problema, cómo los resuelves y finalmente cómo comunicas tu forma de razonar y resultados.

## 🛠️ Problema

El problema a resolver consiste en encontrar la máxima cantidad de rectángulos de dimensiones "a" y "b" (paneles solares) que caben dentro de un rectángulo de dimensiones "x" e "y" (techo).

## 🚀 Cómo Empezar

### Opción 1: Solución en TypeScript
```bash
cd typescript
npm install
npm start
```

### Opción 2: Solución en Python
```bash
cd python
python3 main.py
```

## ✅ Casos de Prueba

Tu solución debe pasar los siguientes casos de prueba:
- Paneles 1x2 y techo 2x4 ⇒ Caben 4
- Paneles 1x2 y techo 3x5 ⇒ Caben 7
- Paneles 2x2 y techo 1x10 ⇒ Caben 0

---

## 📝 Tu Solución

[Video](https://www.youtube.com/watch?v=Qj-z738lIM8)

---

## 💰 Bonus (Opcional)

Si completaste alguno de los ejercicios bonus, explica tu solución aquí:

### Bonus Implementado
Rectángulos superpuestos: En proceso




### Explicación del Bonus
EN PROCESO

Hasta el momento, se obtienen todos los subrectangulos disponibles en la figura, en este momento serián 3 en un sentido y otros 3 en el otro sentido. Es decir, digamos que del poligono se sacan los 3 rectangulos observables de manera horizontal, y luego los 3 rectangulos observables de manera vrtical, luego utilizando las funciones ya creadas se obtienen todos los paneles que se pueden poner dentro de estos rectangulos.

Por hacer: Identificar espacios sobrantes los cuales se puedan unir con los de otro rectangulo, de modo que se pueda rellenar el espacio sobrante con mas paneles.



---

## 🤔 Supuestos y Decisiones

*[Si tuviste que tomar algún supuesto o decisión de diseño, explícalo aquí]*
