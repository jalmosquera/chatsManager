# Custom aliases for Fish
# Cheatsheet Management System Configuration

# Cheat sheets aliases - Required for the system to work
alias csnew='~/.cheatsheets/csnew'
alias csadd='~/.cheatsheets/csadd'
alias csedit='~/.cheatsheets/csedit'
alias csdel='~/.cheatsheets/csdel'
alias cshelp='~/.cheatsheets/cshelp'
alias csalias='~/.cheatsheets/csalias'

# Cheat sheets function - Main command
function cs
    set cheat_dir "$HOME/.cheatsheets"

    if test (count $argv) -eq 0
        echo "🛠️  Sistema de Cheatsheets"
        echo "════════════════════════════════════════"
        echo ""
        echo "📖 COMANDOS DISPONIBLES:"
        echo "  cs <herramienta>       Ver cheatsheet"
        echo "  csnew <herramienta>    ✨ Crear nuevo cheatsheet"
        echo "  csadd <herramienta>    ➕ Agregar comandos"
        echo "  csedit <herramienta>   ✏️  Editar comandos"
        echo "  csdel <herramienta>    🗑️  Eliminar comandos"
        echo "  csalias                🔧 Agregar alias vivo"
        echo "  cshelp                 ❓ Ver ayuda completa"
        echo ""
        echo "📚 CHEATSHEETS DISPONIBLES:"
        ls -1 "$cheat_dir"/*.md 2>/dev/null | sed 's|.*/||' | sed 's/\.md$//' | sed 's/^/  📄 /'
        echo ""
        echo "💡 Ejemplo: cs git"
        return 0
    end

    set tool $argv[1]
    set file "$cheat_dir/$tool.md"

    if test -f "$file"
        # Usar glow para mostrar en terminal
        glow -p "$file"
    else
        echo "❌ No encontré cheat sheet para '$tool'"
        echo "📝 Puedes crearlo con: csnew $tool"
        echo ""
        echo "📚 Disponibles:"
        ls -1 "$cheat_dir"/*.md 2>/dev/null | sed 's|.*/||' | sed 's/\.md$//' | sed 's/^/  📄 /'
    end
end

# Optional: Add your custom aliases below
# Example aliases:
# alias v='nvim'
# alias la='ls -la'
# alias l1='tree -L 1'
# alias l2='tree -L 2'
