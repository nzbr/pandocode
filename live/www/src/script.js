import * as monaco from "monaco-editor";
import {g, r} from "@xeserv/xeact";

const defaultCode = `def main():
    print("Hello World!")
`;

r(() => {

    monaco.editor.defineTheme('copperflame', {
        base: 'vs',
        inherit: true,
        rules: [],
        colors: {
            "editor.background": "#00000000",
        }
    });

    const commonOptions = {
        automaticLayout: true,
        theme: "copperflame",
        lineNumbers: "off",
        minimap: {
            enabled: false
        },
        scrollBeyondLastLine: false,
    };

    const editor = monaco.editor.create(g("editor"), {
        value: defaultCode,
        language: "python",
        ...commonOptions,
    });

    const outEditor = monaco.editor.create(g("output"), {
        value: "",
        language: "tex",
        readOnly: true,
        ...commonOptions,
    });

    const updateOutput = async () => {
        const currentState = editor.getValue();
        const setOut = (text) => {
            if (currentState === editor.getValue()) {
                outEditor.setValue(text);
            }
        };
        try {
            const res = await fetch("/cgi-bin/latex.py", {
                method: "POST",
                body: currentState,
            });
            const text = await res.text();
            setOut(text);
        } catch (e) {
            setOut("Error: " + e);
        }
    }

    editor.onDidChangeModelContent(updateOutput)
    updateOutput();
})

export default {};
