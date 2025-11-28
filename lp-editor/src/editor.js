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
        mockLinter
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
async function analyzeCode(analysisType) {
    const code = view.state.doc.toString();

    // JSON para backend
    const payload = {
        type: analysisType,
        code: code
    };

    console.log("Payload a enviar al backend:");
    console.log(JSON.stringify(payload, null, 2));

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

        // Mostrar respuesta en pestaña
        showResult(analysisType, result.output || "Sin resultados");

    } catch (err) {
        console.error("Fallo en la conexión con el backend:", err);

        // --- Mock fallback ---
        const mockResults = {
            lexical: `Token PACKAGE -> 'package'\nToken IDENT -> 'main'\n...`,
            syntactic: `[SyntaxError] Línea 2, Columna 10: símbolo inesperado`,
            semantic: `[SemanticError] Línea 4: tipo incompatible`,
        };

        showResult(analysisType, mockResults[analysisType] || "Sin resultados (fallback)");
    }
}



document.getElementById("lexical-btn").addEventListener("click", () => analyzeCode('lexical'));
document.getElementById("syntactic-btn").addEventListener("click", () => analyzeCode('syntactic'));
document.getElementById("semantic-btn").addEventListener("click", () => analyzeCode('semantic'));



/* -------------------------------------------------------
   🎯 Exportar
   ------------------------------------------------------- */
export { createEditorState, createEditorView, openSearchPanel };
