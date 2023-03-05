import React, { useState, useRef, useEffect } from "react";
import { Editor, EditorState, ContentState } from "draft-js";
import "draft-js/dist/Draft.css";
import axios from "axios";

const editorStyles = {
  width: "90%",
  height: "90%",
  marginTop: "20px",
  margin: "auto",
  alignItems: "center",
  background: "#f2f2f2",
  color: "black",
  borderRadius: "5px",
  overflow: "hidden",
  padding: "20px",
  boxSizing: "border-box",
  boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.2)",
};

export default function MyEditor(props) {
  const [td, setd] = useState(" ");
  const [editorState, setEditorState] = useState(() =>
    EditorState.createWithContent(ContentState.createFromText(props["text"]))
  );
  const [ro, setro] = useState(false);
  function handleChange(event) {
    setro(event.target.checked);
  }
  const editor = useRef(null);
  function focusEditor() {
    editor.current.focus();
  }
  useEffect(() => {
    const st = async () => {
      const response = await axios.get("/textd");
      setd(response.data["textdata"]);
    };
    st();
  }, []);
  useEffect(() => {
    setEditorState(
      EditorState.createWithContent(ContentState.createFromText(td))
    );
  }, [td]);

  return (
    <div>
      <div>
        <h2>Text Editor </h2>
        <div className="read-only">
          <label>
            <input
              type={"checkbox"}
              name={"Read only"}
              checked={ro}
              onChange={handleChange}
            />
            Read Only
          </label>
        </div>
      </div>
      <div style={editorStyles} onClick={focusEditor}>
        <Editor
          ref={editor}
          editorState={editorState}
          onChange={setEditorState}
          placeholder="Write something!"
          readOnly={ro}
        />
      </div>
    </div>
  );
}
