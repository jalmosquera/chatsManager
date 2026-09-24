# Cheatsheet Management System Configuration for Fish

alias csnew='~/.cheatsheets/csnew'
alias csadd='~/.cheatsheets/csadd'
alias csedit='~/.cheatsheets/csedit'
alias csdel='~/.cheatsheets/csdel'
alias cshelp='~/.cheatsheets/cshelp'
alias csalias='~/.cheatsheets/csalias'

function __cs_cheatsheet_icon
    switch (string lower -- $argv[1])
        case aliases
            printf '%s\n' '🔧'
        case django google
            printf '%s\n' '🌐'
        case docker
            printf '%s\n' '🐳'
        case git
            printf '%s\n' '🔀'
        case nvim nvichad
            printf '%s\n' '⌨️'
        case tmux
            printf '%s\n' '🪟'
        case warp
            printf '%s\n' '⚡'
        case '*'
            printf '%s\n' '📄'
    end
end

function csfind
    set cheat_dir "$HOME/.cheatsheets"
    set rich_python (brew --prefix rich-cli)/libexec/bin/python
    set field_separator (printf '\t')

    set selected (
        $rich_python "$cheat_dir/index_cheatsheets.py" "$cheat_dir" --query '' |
            env SHELL=/bin/sh fzf \
                --disabled \
                --ignore-case \
                --delimiter="$field_separator" \
                --with-nth=2,4 \
                --prompt='⌕ commands> ' \
                --header='Buscá por sección, comando o descripción · Enter abre · Esc cancela' \
                --bind="start:reload:$rich_python $cheat_dir/index_cheatsheets.py $cheat_dir --query {q}" \
                --bind="change:reload:$rich_python $cheat_dir/index_cheatsheets.py $cheat_dir --query {q}" \
                --preview="$rich_python $cheat_dir/render_cheatsheet.py --no-pager {1}" \
                --preview-window='right:65%:wrap'
    )

    if test -n "$selected"
        set selected $selected[1]
        set file (string split \t -- $selected)[1]
        $rich_python "$cheat_dir/render_cheatsheet.py" "$file"
    end
end

function __cs_select_cheatsheet
    set cheat_dir "$HOME/.cheatsheets"
    set rich_python (brew --prefix rich-cli)/libexec/bin/python
    set field_separator (printf '\t')
    set prompt $argv[1]
    set header $argv[2]

    if test -z "$prompt"
        set prompt '⌕ cheatsheets> '
    end
    if test -z "$header"
        set header 'Seleccioná un cheatsheet · Enter confirma · Esc cancela'
    end

    set selected (
        for file in "$cheat_dir"/*.md
            set filename (string replace -r '^.*/' '' -- "$file")
            if string match -q 'README*.md' -- "$filename"
                continue
            end
            set tool (string replace -r '\.md$' '' -- "$filename")
            printf '%s\t%s\t%s %s\n' "$file" "$tool" (__cs_cheatsheet_icon "$tool") "$tool"
        end |
            env SHELL=/bin/sh fzf \
                --ignore-case \
                --delimiter="$field_separator" \
                --with-nth=3 \
                --prompt="$prompt" \
                --header="$header" \
                --preview="$rich_python $cheat_dir/render_cheatsheet.py --no-pager {1}" \
                --preview-window='right:65%:wrap'
    )

    if test -n "$selected"
        set fields (string split \t -- $selected)
        printf '%s\n' "$fields[2]"
    end
end

function cs
    set cheat_dir "$HOME/.cheatsheets"
    set rich_python (brew --prefix rich-cli)/libexec/bin/python
    set field_separator (printf '\t')

    if test (count $argv) -eq 0
        set selected (
            begin
                printf 'action\tnew\t✨ Crear cheatsheet nuevo\n'
                printf 'action\tadd\t➕ Agregar comandos\n'
                printf 'action\tedit\t✏️  Editar comandos\n'
                printf 'action\tdelete\t🗑️  Eliminar comandos\n'
                printf 'action\talias\t🔧 Agregar alias vivo\n'
                printf 'action\tfind\t🔍 Buscar comando o descripción\n'
                printf 'action\thelp\t❓ Ver ayuda\n'
                for file in "$cheat_dir"/*.md
                    set filename (string replace -r '^.*/' '' -- "$file")
                    if string match -q 'README*.md' -- "$filename"
                        continue
                    end
                    set tool (string replace -r '\.md$' '' -- "$filename")
                    printf 'cheat\t%s\t%s %s\n' "$file" (__cs_cheatsheet_icon "$tool") "$tool"
                end
            end |
                env SHELL=/bin/sh fzf \
                    --ignore-case \
                    --delimiter="$field_separator" \
                    --with-nth=3 \
                    --prompt='⌕ cheatsheets> ' \
                    --header='Elegí una acción o cheatsheet · Enter ejecuta · Esc cancela' \
                    --preview="if [ {1} = cheat ]; then $rich_python $cheat_dir/render_cheatsheet.py --no-pager {2}; else printf '%s\\n' {3}; fi" \
                    --preview-window='right:65%:wrap'
        )

        if test -z "$selected"
            return 0
        end

        set fields (string split \t -- $selected)
        if test "$fields[1]" = cheat
            $rich_python "$cheat_dir/render_cheatsheet.py" "$fields[2]"
            return 0
        end

        switch $fields[2]
            case new
                read -P 'Nombre del cheatsheet: ' tool
                if test -n "$tool"
                    "$cheat_dir/csnew" "$tool"
                end
            case add edit delete
                set tool (__cs_select_cheatsheet '⌕ destino> ' 'Seleccioná el cheatsheet a modificar')
                if test -n "$tool"
                    set script_action $fields[2]
                    if test "$script_action" = delete
                        set script_action del
                    end
                    "$cheat_dir/cs$script_action" "$tool"
                end
            case alias
                "$cheat_dir/csalias"
            case find
                csfind
            case help
                "$cheat_dir/cshelp"
        end
        return 0
    end

    set tool $argv[1]
    set file "$cheat_dir/$tool.md"

    if test -f "$file"
        $rich_python "$cheat_dir/render_cheatsheet.py" "$file"
    else
        echo "❌ No encontré cheat sheet para '$tool'"
        echo "📝 Puedes crearlo con: csnew $tool"
        echo ""
        echo "📚 Disponibles:"
        for available_file in "$cheat_dir"/*.md
            set filename (string replace -r '^.*/' '' -- "$available_file")
            if string match -q 'README*.md' -- "$filename"
                continue
            end
            set available_tool (string replace -r '\.md$' '' -- "$filename")
            printf '  %s %s\n' (__cs_cheatsheet_icon "$available_tool") "$available_tool"
        end
    end
end
