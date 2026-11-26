
# Proyecto-IB_ShellDoc-Web

**Escuela Politécnica Nacional (EPN)**  
**Asignatura:** Sistemas Operativos  
**Periodo académico:** 2026-B  
**Proyecto:** Primer Bimestre

## Descripción del proyecto

Generación automatizada de presentaciones web a partir de sesiones de terminal Linux, mediante Python, hilos, semáforos, Quarto y Reveal.js.

## Tecnologías utilizadas

- Ubuntu Server
- Python
- Hilos y semáforos
- Quarto
- Reveal.js
- Git y GitHub

---

## Captura de la sesión Linux

### Descripción

Se realizó la captura de una sesión real de terminal en Ubuntu Server mediante la herramienta `script`, registrando los comandos ejecutados y sus respectivas salidas.

Como resultado, se obtuvo el archivo `session.txt`, que constituye la entrada del Hilo 1 para su posterior transformación en una presentación web mediante Quarto y Reveal.js.

### Comandos ejecutados

| N.º | Comando | Descripción |
|:---:|---------|-------------|
| 1 | `pwd` | Muestra la ruta del directorio actual. |
| 2 | `whoami` | Identifica al usuario actual. |
| 3 | `date` | Presenta la fecha y hora del sistema. |
| 4 | `hostname` | Muestra el nombre del equipo. |
| 5 | `uname -a` | Presenta información del kernel. |
| 6 | `mkdir -p prueba_linux` | Crea un directorio de prueba. |
| 7 | `ls` | Lista archivos y directorios. |
| 8 | `ls -l` | Presenta información detallada de archivos y directorios. |
| 9 | `ps` | Muestra los procesos asociados a la terminal. |
| 10 | `free -h` | Presenta información sobre la memoria RAM y swap. |
| 11 | `df -h` | Muestra el espacio disponible y utilizado en los sistemas de archivos. |

### Resultado obtenido

Se obtuvo el archivo `session.txt`, que contiene el registro de la sesión Linux y permite continuar con la etapa de transformación del proyecto.

## Presentación web – Funcionalidad extra (Hilo 4)

La presentación generada por ShellDoc Web se encuentra disponible mediante GitHub Pages:
https://welltror.github.io/prueba_publicador/#/title-slide
Esta funcionalidad permite publicar automáticamente la presentación HTML una vez finalizada correctamente la etapa de renderización.

---

