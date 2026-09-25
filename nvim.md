# ⌨️ Nvim - Comandos Esenciales

## 📁 Comandos Generales
```tsv
Space	Space	Abrir menú principal (Which-Key)
Space + E	Space + E	Explorador de archivos (Neo-tree)
Space + Space	Space + Space	Buscar archivos
Space + /	Space + /	Buscar en archivos (Grep)
Space + ,	Space + ,	Cambiar entre buffers
Space + :	Space + :	Historial de comandos
Ctrl + H	Ctrl + H	Navegar panel izquierdo (Tmux/Split)
Ctrl + J	Ctrl + J	Navegar panel abajo (Tmux/Split)
Ctrl + K	Ctrl + K	Navegar panel arriba (Tmux/Split)
Ctrl + L	Ctrl + L	Navegar panel derecha (Tmux/Split)
Ctrl + \	Ctrl + \	Navegar al último panel activo
Ctrl + Space	Ctrl + Space	Navegar al siguiente panel
Ctrl + S	Ctrl + S	Guardar archivo
Ctrl + B	Ctrl + B	Eliminar hasta fin de palabra (Insert mode)
Ctrl + C	Ctrl + C	Salir a modo normal
Space + B + D	Space + B + D	Cerrar buffer actual
Space + B + O	Space + B + O	Cerrar otros buffers
Space + B + Q	Space + B + Q	Cerrar todos los buffers excepto actual
Space + B + P	Space + B + P	Pin buffer (mantener abierto)
Space + F + F	Space + F + F	Buscar archivos
Space + F + R	Space + F + R	Archivos recientes
Space + F + N	Space + F + N	Nuevo archivo
Space + F + G	Space + F + G	Buscar archivos en git
Space + F + W	Space + F + W	Buscar palabra bajo cursor
Space + S + G	Space + S + G	Buscar texto (Grep) en selección visual
Space + S + G	Space + S + G	Buscar texto en root del proyecto
Space + S + W	Space + S + W	Buscar palabra bajo cursor
Space + S + R	Space + S + R	Búsqueda y reemplazo
Space + C + A	Space + C + A	Code actions (acciones de código)
Space + C + R	Space + C + R	Renombrar símbolo
Space + C + D	Space + C + D	Ir a definición
Space + C + D	Space + C + D	Ir a declaración
Space + C + I	Space + C + I	Ir a implementación
Space + C + T	Space + C + T	Ir a definición de tipo
Space + C + S	Space + C + S	Símbolos del documento
Space + C + F	Space + C + F	Formatear código
Space + G + S	Space + G + S	Git status (Lazygit)
Space + G + C	Space + G + C	Git commits
Space + G + B	Space + G + B	Git branches
Space + G + B	Space + G + B	Git blame line
Space + G + D	Space + G + D	Git diff
Space + G + H	Space + G + H	Git hunk (preview)
Space + X + X	Space + X + X	Lista de problemas (Trouble)
Space + X + W	Space + X + W	Diagnósticos del workspace
Space + X + D	Space + X + D	Diagnósticos del documento
Space + X + Q	Space + X + Q	Quickfix list
Space + X + L	Space + X + L	Location list
Space + U + K	Space + U + K	Toggle Screenkey (mostrar teclas)
Space + U + N	Space + U + N	Toggle line numbers
Space + U + W	Space + U + W	Toggle word wrap
Space + U + S	Space + U + S	Toggle spelling
Space + U + T	Space + U + T	Toggle Treesitter
Space + U + C	Space + U + C	Toggle conceallevel
Space + Z	Space + Z	Zen Mode
Space + W + W	Space + W + W	Cambiar entre ventanas
Space + W + D	Space + W + D	Cerrar ventana
Space + W	Space + W	- Split horizontal
Space + W + |	Space + W + |	Split vertical
Space + O + C	Space + O + C	Obsidian: Toggle checkbox
Space + O + T	Space + O + T	Obsidian: Insertar template
Space + O + O	Space + O + O	Obsidian: Abrir en app
Space + O + B	Space + O + B	Obsidian: Ver backlinks
Space + O + L	Space + O + L	Obsidian: Ver links
Space + O + N	Space + O + N	Obsidian: Nueva nota
Space + O + S	Space + O + S	Obsidian: Buscar notas
Space + O + Q	Space + O + Q	Obsidian: Quick switch
Space + M + D	Space + M + D	Eliminar todas las marcas
-	-	Abrir Oil (navegador de archivos)
Space	Space	- Oil en directorio del buffer actual
G + D	G + D	Ir a definición
G + R	G + R	Ir a referencias
G + I	G + I	Ir a implementación
K	K	Mostrar documentación (hover)
] + D	] + D	Siguiente diagnóstico
[ + D	[ + D	Diagnóstico anterior
] + E	] + E	Siguiente error
[ + E	[ + E	Error anterior
J + J	J + J	Escape (en modo insert)
J + K	J + K	Escape (en modo insert)
/	/	Buscar en buffer
n	n	Siguiente coincidencia
N	N	Anterior coincidencia
*	*	Buscar palabra bajo cursor hacia adelante
Y + Y	Y + Y	Copiar línea
Y + W	Y + W	Copiar palabra
Y + $	Y + $	Copiar hasta final de línea
p	p	Pegar después
P	P	Pegar antes
D + D	D + D	Cortar línea
D + W	D + W	Cortar palabra
C + W	C + W	Cambiar palabra
u	u	Deshacer
Ctrl + R	Ctrl + R	Rehacer
v	v	Modo visual
V	V	Modo visual línea
Ctrl + V	Ctrl + V	Modo visual bloque
>	>	Indentar selección
<	<	Desindentar selección
G + C	G + C	Comentar/descomentar selección
Z + Z	Z + Z	Centrar cursor en pantalla
Z + T	Z + T	Cursor al top
Z + B	Z + B	Cursor al bottom
H	H	Ir al top de la pantalla
M	M	Ir al medio de la pantalla
L	L	Ir al bottom de la pantalla
w	w	Siguiente palabra
b	b	Palabra anterior
e	e	Final de palabra
0	0	Inicio de línea
^	^	Primer carácter no blanco
$	$	Final de línea
G + G	G + G	Ir al inicio del archivo
G	G	Ir al final del archivo
: numero	: numero	Ir a línea específica
f letra	f letra	Buscar letra hacia adelante
F letra	F letra	Buscar letra hacia atrás
t letra	t letra	Hasta letra (forward)
T letra	T letra	Hasta letra (backward)
;	;	Repetir búsqueda f/t
,	,	Repetir búsqueda f/t inversa
%	%	Ir al paréntesis/bracket correspondiente
C + I + (	C + I + (	Cambiar dentro de paréntesis
C + I + {	C + I + {	Cambiar dentro de llaves
C + I + [	C + I + [	Cambiar dentro de brackets
C + I + "	C + I + "	Cambiar dentro de comillas
D + I + W	D + I + W	Eliminar palabra interior
V + I + P	V + I + P	Seleccionar párrafo interior
.	.	Repetir último comando
q letra	q letra	Grabar macro
@ letra	@ letra	Ejecutar macro
Space + Space + ?	Space + Space + ?	Buscar ayuda
Space + Space + K	Space + Space + K	Ver keymaps disponibles
```

## 📁 mas usados
```tsv
greep text	g s a symbol	meter texto dentro de simbolos por ejemplo 'texto'
```

---
*Actualizado: 2026-09-24*
