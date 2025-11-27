import { EditorState } from '@codemirror/state';
import { openSearchPanel, highlightSelectionMatches } from '@codemirror/search';
import { indentWithTab, history, defaultKeymap, historyKeymap } from '@codemirror/commands';
import { foldGutter, indentOnInput, indentUnit, bracketMatching, foldKeymap, syntaxHighlighting, defaultHighlightStyle } from '@codemirror/language';
import { closeBrackets, autocompletion, closeBracketsKeymap, completionKeymap } from '@codemirror/autocomplete';
import { lineNumbers, highlightActiveLineGutter, highlightSpecialChars, drawSelection, dropCursor, rectangularSelection, crosshairCursor, highlightActiveLine, keymap, EditorView } from '@codemirror/view';
import { showTooltip } from "@codemirror/tooltip";
// Theme
import { oneDark } from "@codemirror/theme-one-dark";

// Language
import { go } from "@codemirror/lang-go";

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
        go(),
        syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
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

function showErrorTooltip(view, pos, message) {
    const tooltip = {
        pos,
        above: true,
        create() {
            let dom = document.createElement("div");
            dom.textContent = message;
            dom.className = "cm-error-tooltip";
            return { dom };
        }
    };

    view.dispatch({
        effects: showTooltip.of(tooltip)
    });
}




// --- Lógica para las Pestañas de Resultados ---
const tabs = document.querySelectorAll(".tab-link");
const contents = document.querySelectorAll(".tab-content");

tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        // Desactivar todas las pestañas y contenidos
        tabs.forEach(item => item.classList.remove("active"));
        contents.forEach(item => item.classList.remove("active"));

        // Activar la pestaña y contenido seleccionados
        tab.classList.add("active");
        document.getElementById(tab.dataset.tab).classList.add("active");
    });
});

// --- Lógica para los Botones de Análisis ---
// Helper para mostrar resultados
function showResult(tabId, data) {
    const contentArea = document.querySelector(`#${tabId} pre code`);
    contentArea.textContent = data;

    // Cambiar a la pestaña correspondiente
    document.querySelector(`.tab-link[data-tab="${tabId}"]`).click();
}

// Simulación de llamada a la API
async function analyzeCode(analysisType) {
    const code = view.state.doc.toString();

    // Muestra un mensaje de carga
    showResult(analysisType, `Analizando...`);

    // **AQUÍ DEBES HACER LA LLAMADA A TU BACKEND**
    // Ejemplo:
    // const response = await fetch(\`/api/analyze?type=\${analysisType}\`, {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ code })
    // });
    // const result = await response.text();
    // showResult(analysisType, result);

    // --- Simulación (borra esto cuando integres tu backend) ---
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simula espera de red
    const mockResults = {
        lexical: `[Token] type=PACKAGE, value='package'\\n[Token] type=IDENTIFIER, value='main'\\n...`,
        syntactic: `[SyntaxError] Syntax error at token '{' (type=LBRACE)\\n...`,
        semantic: `[Error semantico:] La variable x es de tipo int, pero se intento asignar string\\n...`
    };
    const output = mockResults[analysisType] || "No se pudo obtener el resultado.";
    showResult(analysisType, output);

    // EJEMPLO: Simular que tu backend devuelve un error en línea 2, columna 10
    if (analysisType === "syntactic") {
        const line = 2;
        const column = 10;

        // Convertir line/column a posición absoluta
        let pos = view.state.doc.line(line).from + (column - 1);

        // Mostrar tooltip
        showErrorTooltip(view, pos, "Error sintáctico: símbolo inesperado");
    }

    // --- Fin de la simulación ---
}

document.getElementById("lexical-btn").addEventListener("click", () => analyzeCode('lexical'));
document.getElementById("syntactic-btn").addEventListener("click", () => analyzeCode('syntactic'));
document.getElementById("semantic-btn").addEventListener("click", () => analyzeCode('semantic'));

export { createEditorState, createEditorView, openSearchPanel };