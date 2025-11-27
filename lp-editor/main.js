

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
    const code = editorView.state.doc.toString();

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
    showResult(analysisType, mockResults[analysisType] || "No se pudo obtener el resultado.");
    // --- Fin de la simulación ---
}

document.getElementById("lexical-btn").addEventListener("click", () => analyzeCode('lexical'));
document.getElementById("syntactic-btn").addEventListener("click", () => analyzeCode('syntactic'));
document.getElementById("semantic-btn").addEventListener("click", () => analyzeCode('semantic'));