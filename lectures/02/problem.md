# Sesión 2: práctica y tarea - aprender un formato de respuesta con LoRA y comparar antes/después

Esta sesión se realiza en Google Colab (GPU T4, cuota gratuita). No se utiliza Codespaces.

## Objetivos de esta sesión

- Entrenar brevemente un modelo pequeño con LoRA y comprobar con cifras y salidas **qué cambia y qué no cambia** antes y después del entrenamiento.
- Explicar con tus propios resultados que el modelo puede aprender un formato, pero no necesariamente aprende a decidir cuándo debe pedir confirmación en lugar de afirmar algo.
- Explicar con tus propias palabras cuándo conviene y cuándo no conviene hacer fine-tuning.

## Notebook que se utiliza

- [notebooks/lora_format_tuning.ipynb](../../notebooks/lora_format_tuning.ipynb)
- Abrir en Colab: https://colab.research.google.com/github/matsuolab/lecture-ai-engineering-2026/blob/main/notebooks/lora_format_tuning.ipynb

Usaremos una FAQ ficticia de cinco elementos y entrenaremos `Qwen/Qwen3.5-0.8B` con LoRA durante 20 épocas (14 ejemplos repetidos 20 veces, 40 pasos; unos 4-5 minutos en una T4).
La salida esperada es una sola línea JSON con el formato `{"answer": ..., "needs_review": ...}`. Para una pregunta que no esté respaldada por la FAQ, la respuesta correcta debe usar `needs_review: true` y pedir confirmación.
La evaluación se divide en dos métricas: **tasa de cumplimiento del formato** (si respeta el JSON) y **tasa de contenido correcto** (si `needs_review` y las palabras esperadas son correctas).

## Preparación previa (opcional, 5 minutos)

Antes de la clase puedes ejecutar las secciones 0-3 para verificar que se asigna la GPU, se instalan las bibliotecas y se descarga el modelo.
Si la sesión de Colab se desconecta, las variables desaparecen; en ese caso vuelve a ejecutar el notebook desde la sección 0.

## Práctica (30 minutos)

1. Abre el notebook en Colab y selecciona **File → Save a copy in Drive**.
2. Selecciona **Runtime → Change runtime type → T4 GPU**.
3. Ejecuta las secciones 0-3 en orden (unos 5 minutos). En la tabla previa al entrenamiento, revisa **qué claves faltan** y si las respuestas coinciden con la FAQ.
4. Ejecuta el entrenamiento en la sección 4 (4-5 minutos). Mientras esperas, lee la diferencia entre LoRA y QLoRA y revisa `trainable%` y la evolución de `Training Loss`.
5. Evalúa el modelo después del entrenamiento en las secciones 5-6 y compáralo con el resultado anterior.
   - Tabla comparativa: ¿cómo cambiaron `format_rate` y `content_rate`?
   - `regressed`: preguntas que funcionaban antes y fallan después; lo esperado es una lista vacía.
   - Tipos de fallo restantes: afirmar usando otra entrada de la FAQ o responder que no hay información ante una pregunta que sí estaba respaldada.
   - Sección 6: comprobar si ante preguntas que no aparecen en la FAQ ni en los datos de entrenamiento el modelo pide confirmación o afirma algo.
6. Crea `result.json` en la sección 7. Escribe los puntos principales en `lectures/02/answer.md` y crea un PR desde la rama `lec02` hacia `main` de tu fork. También puedes editar `answer.md` desde GitHub. Puedes incluir `result.json` en `lectures/02/`.
7. Selecciona **Runtime → Disconnect and delete runtime**.

> La GPU gratuita de Colab tiene un límite de tiempo. Elimina el entorno cuando termines.
> Si no consigues una GPU o el entrenamiento no termina a tiempo, sigue la sección 4b y utiliza los resultados del profesor para comparar y analizar. En ese caso pon `executed_training_myself` en `False` y explica en `answer.md` hasta dónde pudiste llegar.

Aunque se fije la semilla, el entrenamiento en GPU no es completamente reproducible. Es normal que las preguntas restantes sean diferentes entre ejecuciones; compara los tipos de fallo.

## Tarea (elige una opción)

| Nivel | Contenido |
|---|---|
| Básico | Cambia uno de estos valores de `CONFIG`: `lora_r`, `lr` o `num_train_epochs`. Vuelve a entrenar y registra `format_rate`, `content_rate`, la pérdida final y el tiempo junto con la configuración original. Después del cambio selecciona **Runtime → Restart session** y ejecuta todo desde arriba. Compara los dos `result.json`. |
| Implementación | Sustituye `FAQ`, `GROUNDED` y `UNGROUNDED` por un tema propio con unos cinco elementos. Entrena y compara antes/después. Conserva el formato JSON y el diseño de `needs_review`, y explica cómo preparaste las preguntas sin fundamento. |
| Avanzado | Usa `scripts/make_sft_dataset.py` para crear datos Q&A en formato JSONL `messages` a partir del glosario del curso. Entrena con esos datos en lugar de la FAQ. Prepara preguntas y respuestas de evaluación sobre términos del glosario, reformulaciones y términos fuera del glosario. Compara antes/después y analiza las ventajas y desventajas de entrenar el modelo frente a buscar en el glosario. |

Para preparar los datos de la opción Avanzada, ejecuta esto en Codespaces y sube el archivo resultante a Colab:

```bash
uv run python scripts/make_sft_dataset.py > glossary_sft.jsonl
```

En Colab, cada línea tiene el mismo formato `messages` que utiliza `to_chat` en el notebook. Puedes pasar las líneas cargadas directamente a `Dataset.from_list` y entrenarlas con `SFTTrainer` en la sección 4. Debes rehacer `test` y `gold` de acuerdo con el glosario.

La sección 8, que carga el modelo en 4 bits y compara sus salidas, es una observación sin entrenamiento y puede añadirse a cualquier nivel. Entrenar directamente en 4 bits (QLoRA) no forma parte de la tarea porque no se ha verificado en el entorno T4 de este curso.

## Precauciones

- Después del entrenamiento, el adapter también queda insertado en la variable `model`. Para volver a obtener salidas previas al entrenamiento, usa `tuned.disable_adapter()` (sección 6) o reinicia la sesión.
- Las versiones de las bibliotecas están fijadas en `PINS` en la sección 0. Cambiarlas puede hacer que el notebook deje de funcionar.
