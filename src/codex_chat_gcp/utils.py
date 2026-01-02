import os
import sys
import yaml
import tempfile
import subprocess
from importlib import resources
import streamlit as st
from . import config

@st.cache_data
def load_prompts():
    """パッケージ内のprompts.yamlを一度だけ読み込み、結果をキャッシュする"""
    try:
        with resources.open_text("codex_chat_gcp", "prompts.yaml") as f:
            yaml_data = yaml.safe_load(f)
            return yaml_data.get("prompts", {})
    except Exception as e:
        st.error(f"prompts.yamlの読み込み失敗: {e}")
        st.stop()

def find_env_files(directory="env"):
    """指定されたディレクトリ内の.envファイルを検索する"""
    if not os.path.isdir(directory):
        return []
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".env")]

def run_pylint_validation(canvas_code, canvas_index, prompts):
    """
    指定されたコードに対してpylintを実行し、分析プロンプトを生成する
    ※コールバック関数のため st.rerun() は不要
    """
    if not canvas_code or canvas_code.strip() == "" or canvas_code.strip() == config.ACE_EDITOR_DEFAULT_CODE.strip():
        st.toast(config.UITexts.NO_CODE_TO_VALIDATE, icon="⚠️")
        return

    spinner_text = config.UITexts.VALIDATE_SPINNER_MULTI.format(i=canvas_index + 1) if st.session_state['multi_code_enabled'] else config.UITexts.VALIDATE_SPINNER_SINGLE
    with st.spinner(spinner_text):
        tmp_file_path = ""
        pylint_report = ""
        try:
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False, encoding='utf-8') as tmp_file:
                tmp_file_path = tmp_file.name
                tmp_file.write(canvas_code.replace('\r\n', '\n'))
                tmp_file.flush()
            
            result = subprocess.run(
                [sys.executable, "-m", "pylint", tmp_file_path],
                capture_output=True, text=True, check=False
            )
            
            error_output = (result.stderr or "") + (result.stdout or "")
            if "syntax-error" in error_output.lower():
                st.toast(config.UITexts.PYLINT_SYNTAX_ERROR, icon="⚠️")
                return 

            issues = []
            if result.stdout:
                issues = [line for line in result.stdout.splitlines() if line.strip() and not line.startswith(('*', '-')) and 'Your code has been rated' not in line]
            
            if issues:
                cleaned_issues = [issue.replace(f'{tmp_file_path}:', 'Line ') for issue in issues]
                pylint_report = "\n".join(cleaned_issues)
        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    if not pylint_report.strip():
        st.sidebar.success(f"✅ Canvas-{canvas_index + 1}: pylint検証完了。問題なし。")
        return

    # Geminiへの分析依頼プロンプト
    validation_template = prompts.get("validation", {}).get("text", "以下はpylintのレポートです。解析してください:\n{pylint_report}\n\n対象コード:\n{code_for_prompt}")
    code_for_prompt = f"```python\n{canvas_code}\n```"
    validation_prompt = validation_template.format(code_for_prompt=code_for_prompt, pylint_report=pylint_report)
    
    system_message = st.session_state['messages'][0] if st.session_state['messages'] and st.session_state['messages'][0]["role"] == "system" else {"role": "system", "content": ""}
    st.session_state['special_generation_messages'] = [system_message, {"role": "user", "content": validation_prompt}]
    st.session_state['is_generating'] = True
    # コールバック内なので st.rerun() は削除

def load_app_config():
    """パッケージ内のconfig.yamlを読み込む"""
    try:
        with resources.open_text("codex_chat_gcp", "config.yaml") as f:
            return yaml.safe_load(f)
    except Exception:
        return {}
    