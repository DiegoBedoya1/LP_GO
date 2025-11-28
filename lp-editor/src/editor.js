import { EditorState } from '@codemirror/state';
import { openSearchPanel, highlightSelectionMatches } from '@codemirror/search';
import { indentWithTab, history, defaultKeymap, historyKeymap } from '@codemirror/commands';
import { foldGutter, indentOnInput, indentUnit, bracketMatching, foldKeymap, syntaxHighlighting, defaultHighlightStyle } from '@codemirror/language';
import { closeBrackets, autocompletion, closeBracketsKeymap, completionKeymap } from '@codemirror/autocomplete';
import { lineNumbers, highlightActiveLineGutter, highlightSpecialChars, drawSelection, dropCursor, rectangularSelection, crosshairCursor, highlightActiveLine, keymap, EditorView } from '@codemirror/view';

// Linter
import { linter, lintGutter } from "@codemirror/lint";

// Theme
import { oneDark } from "@codemirror/theme-one-dark";

// Language
import { go } from "@codemirror/lang-go";

const BACKEND_URL = "http://localhost:5000/api/analyze";

/* -------------------------------------------------------
   🎯 MOCK: Linter que simula errores sintácticos/semánticos
   ------------------------------------------------------- */
const mockLinter = linter(view => {
    const diagnostics = [];

    // ❗ Aquí pondrás los errores que vengan de tu backend
    // Por ahora: simular uno
    const mockErrors = [
        { linea: 2, columna: 10, mensaje: "Error sintáctico: símbolo inesperado" },
        { linea: 4, columna: 5, mensaje: "Tipo incompatible en asignación" }
    ];

    for (const err of mockErrors) {
        const line = view.state.doc.line(err.linea);
        const pos = line.from + (err.columna - 1);

        diagnostics.push({
            from: pos,
            to: pos + 1,
            severity: "error",
            message: err.mensaje,
        });
    }

    return diagnostics;
});



/* -------------------------------------------------------
   🎨 CREACIÓN DEL EDITOR
   ------------------------------------------------------- */
function createEditorState(initialContents, options = {}) {
    let extensions = [
        lineNumbers(),
        highlightActiveLineGutter(),
        highlightSpecialChars(),
        history(),
        foldGutter(),
        drawSelection(),
        indentUnit.of("    "),
        EditorState.allowMultipleSelections.of(true),
        indentOnInput(),
        bracketMatching(),
        closeBrackets(),
        autocompletion(),
        rectangularSelection(),
        crosshairCursor(),
        highlightActiveLine(),
        highlightSelectionMatches(),
        keymap.of([
            indentWithTab,
            ...closeBracketsKeymap,
            ...defaultKeymap,
            ...historyKeymap,
            ...foldKeymap,
            ...completionKeymap,
        ]),

        // GO language
        go(),

        // Syntax highlight
        syntaxHighlighting(defaultHighlightStyle, { fallback: true }),

        // 🔥 Gutter + Linter
        lintGutter(),
    ];

    if (options.oneDark)
        extensions.push(oneDark);

    return EditorState.create({
        doc: initialContents,
        extensions
    });
}

function createEditorView(state, parent) {
    return new EditorView({ state, parent });
}



/* -------------------------------------------------------
   🎯 Lógica de pestañas
   ------------------------------------------------------- */
const tabs = document.querySelectorAll(".tab-link");
const contents = document.querySelectorAll(".tab-content");

tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        tabs.forEach(item => item.classList.remove("active"));
        contents.forEach(item => item.classList.remove("active"));
        tab.classList.add("active");
        document.getElementById(tab.dataset.tab).classList.add("active");
    });
});



/* -------------------------------------------------------
   Mostrar resultados en pestañas
   ------------------------------------------------------- */
function showResult(tabId, data) {
    const contentArea = document.querySelector(`#${tabId} pre code`);
    contentArea.textContent = data;
    document.querySelector(`.tab-link[data-tab="${tabId}"]`).click();
}



/* -------------------------------------------------------
    Botones de análisis 
   ------------------------------------------------------- */
/* -------------------------------------------------------
    Botones de análisis 
   ------------------------------------------------------- */

async function analyzeCode(analysisType) {
    const code = view.state.doc.toString();
    const payload = {
        type: analysisType,
        code: code
    };

    console.log("Payload a enviar al backend:", JSON.stringify(payload, null, 2));
    showResult(analysisType, "Analizando...");

    try {
        const response = await fetch(BACKEND_URL, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor");
        }

        const result = await response.json();
        console.log("Respuesta del backend:", result);

        // 💥 NUEVA LÓGICA DE MANEJO DE RESULTADOS 💥
        let outputMessage = "";

        if (analysisType === 'lexical') {
            const errors = result.errors;
            if (result.hay_errores) {
                // Aquí deberías mostrar los errores, o si tu lexer devuelve tokens, mostrarlos.
                // Como solo devuelves 'errors' en Flask, mostraremos los errores.
                outputMessage = errors.length > 0
                    ? "🚨 Errores Léxicos:\n" + errors.join('\n')
                    : "✅ Análisis Léxico **SIN ERRORES**. Se pueden mostrar los tokens si el backend los devuelve.";
            } else {
                 // Si no hay errores, asume que el backend solo devolvió los errores
                 // y no los tokens. Podrías modificar Flask para que devuelva los tokens aquí.
                 outputMessage = "✅ Análisis Léxico **SIN ERRORES**.";
            }

        } else if (analysisType === 'syntactic') {
            const errors = result.syntactic_errors;
            outputMessage = errors.length > 0
                ? `🚨 ${result.count} Errores Sintácticos:\n` + errors.join('\n')
                : "✅ Análisis Sintáctico **SIN ERRORES**. El código es gramaticalmente correcto.";

        } else if (analysisType === 'semantic') {
            const errors = result.semantic_errors;
            outputMessage = errors.length > 0
                ? `🚨 ${result.count} Errores Semánticos:\n` + errors.join('\n')
                : "✅ Análisis Semántico **SIN ERRORES**. El código es lógicamente válido.";
        }

        // Mostrar el mensaje formateado en la pestaña
        showResult(analysisType, outputMessage);

    } catch (err) {
        console.error("Fallo en la conexión con el backend:", err);
        showResult(analysisType, `❌ Error de Conexión con el Servidor:\n${err.message}`);
    }
}

document.getElementById("lexical-btn").addEventListener("click", () => analyzeCode('lexical'));
document.getElementById("syntactic-btn").addEventListener("click", () => analyzeCode('syntactic'));
document.getElementById("semantic-btn").addEventListener("click", () => analyzeCode('semantic'));



/* -------------------------------------------------------
   🎯 Exportar
   ------------------------------------------------------- */
export { createEditorState, createEditorView, openSearchPanel };
