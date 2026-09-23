# ⌨️ Nvim - Comandos Esenciales

## 📁 Comandos Generales
```bash
Space                           # Abrir menú principal (Which-Key)
Space + E                       # Explorador de archivos (Neo-tree)
Space + Space                   # Buscar archivos
Space + /                       # Buscar en archivos (Grep)
Space + ,                       # Cambiar entre buffers
Space + :                       # Historial de comandos
Ctrl + H                        # Navegar panel izquierdo (Tmux/Split)
Ctrl + J                        # Navegar panel abajo (Tmux/Split)
Ctrl + K                        # Navegar panel arriba (Tmux/Split)
Ctrl + L                        # Navegar panel derecha (Tmux/Split)
Ctrl + \                        # Navegar al último panel activo
Ctrl + Space                    # Navegar al siguiente panel
Ctrl + S                        # Guardar archivo
Ctrl + B                        # Eliminar hasta fin de palabra (Insert mode)
Ctrl + C                        # Salir a modo normal
Space + B + D                   # Cerrar buffer actual
Space + B + O                   # Cerrar otros buffers
Space + B + Q                   # Cerrar todos los buffers excepto actual
Space + B + P                   # Pin buffer (mantener abierto)
Space + F + F                   # Buscar archivos
Space + F + R                   # Archivos recientes
Space + F + N                   # Nuevo archivo
Space + F + G                   # Buscar archivos en git
Space + F + W                   # Buscar palabra bajo cursor
Space + S + G                   # Buscar texto (Grep) en selección visual
Space + S + G                   # Buscar texto en root del proyecto
Space + S + W                   # Buscar palabra bajo cursor
Space + S + R                   # Búsqueda y reemplazo
Space + C + A                   # Code actions (acciones de código)
Space + C + R                   # Renombrar símbolo
Space + C + D                   # Ir a definición
Space + C + D                   # Ir a declaración
Space + C + I                   # Ir a implementación
Space + C + T                   # Ir a definición de tipo
Space + C + S                   # Símbolos del documento
Space + C + F                   # Formatear código
Space + G + S                   # Git status (Lazygit)
Space + G + C                   # Git commits
Space + G + B                   # Git branches
Space + G + B                   # Git blame line
Space + G + D                   # Git diff
Space + G + H                   # Git hunk (preview)
Space + X + X                   # Lista de problemas (Trouble)
Space + X + W                   # Diagnósticos del workspace
Space + X + D                   # Diagnósticos del documento
Space + X + Q                   # Quickfix list
Space + X + L                   # Location list
Space + U + K                   # Toggle Screenkey (mostrar teclas)
Space + U + N                   # Toggle line numbers
Space + U + W                   # Toggle word wrap
Space + U + S                   # Toggle spelling
Space + U + T                   # Toggle Treesitter
Space + U + C                   # Toggle conceallevel
Space + Z                       # Zen Mode
Space + W + W                   # Cambiar entre ventanas
Space + W + D                   # Cerrar ventana
Space + W                       # - Split horizontal
Space + W + |                   # Split vertical
Space + O + C                   # Obsidian: Toggle checkbox
Space + O + T                   # Obsidian: Insertar template
Space + O + O                   # Obsidian: Abrir en app
Space + O + B                   # Obsidian: Ver backlinks
Space + O + L                   # Obsidian: Ver links
Space + O + N                   # Obsidian: Nueva nota
Space + O + S                   # Obsidian: Buscar notas
Space + O + Q                   # Obsidian: Quick switch
Space + M + D                   # Eliminar todas las marcas
-                               # Abrir Oil (navegador de archivos)
Space                           # - Oil en directorio del buffer actual
G + D                           # Ir a definición
G + R                           # Ir a referencias
G + I                           # Ir a implementación
K                               # Mostrar documentación (hover)
] + D                           # Siguiente diagnóstico
[ + D                           # Diagnóstico anterior
] + E                           # Siguiente error
[ + E                           # Error anterior
J + J                           # Escape (en modo insert)
J + K                           # Escape (en modo insert)
/                               # Buscar en buffer
n                               # Siguiente coincidencia
N                               # Anterior coincidencia
*                               # Buscar palabra bajo cursor hacia adelante
Y + Y                           # Copiar línea
Y + W                           # Copiar palabra
Y + $                           # Copiar hasta final de línea
p                               # Pegar después
P                               # Pegar antes
D + D                           # Cortar línea
D + W                           # Cortar palabra
C + W                           # Cambiar palabra
u                               # Deshacer
Ctrl + R                        # Rehacer
v                               # Modo visual
V                               # Modo visual línea
Ctrl + V                        # Modo visual bloque
>                               # Indentar selección
<                               # Desindentar selección
G + C                           # Comentar/descomentar selección
Z + Z                           # Centrar cursor en pantalla
Z + T                           # Cursor al top
Z + B                           # Cursor al bottom
H                               # Ir al top de la pantalla
M                               # Ir al medio de la pantalla
L                               # Ir al bottom de la pantalla
w                               # Siguiente palabra
b                               # Palabra anterior
e                               # Final de palabra
0                               # Inicio de línea
^                               # Primer carácter no blanco
$                               # Final de línea
G + G                           # Ir al inicio del archivo
G                               # Ir al final del archivo
: numero                        # Ir a línea específica
f letra                         # Buscar letra hacia adelante
F letra                         # Buscar letra hacia atrás
t letra                         # Hasta letra (forward)
T letra                         # Hasta letra (backward)
;                               # Repetir búsqueda f/t
,                               # Repetir búsqueda f/t inversa
%                               # Ir al paréntesis/bracket correspondiente
C + I + (                       # Cambiar dentro de paréntesis
C + I + {                       # Cambiar dentro de llaves
C + I + [                       # Cambiar dentro de brackets
C + I + "                       # Cambiar dentro de comillas
D + I + W                       # Eliminar palabra interior
V + I + P                       # Seleccionar párrafo interior
.                               # Repetir último comando
q letra                         # Grabar macro
@ letra                         # Ejecutar macro
Space + Space + ?               # Buscar ayuda
Space + Space + K               # Ver keymaps disponibles
```

---
*Creado: 2025-10-15*
