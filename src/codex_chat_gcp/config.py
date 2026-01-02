# --- Constants ---
MAX_CANVASES = 20

# --- Environment Variable Keys ---
GCP_PROJECT_ID_NAME = "GCP_PROJECT_ID"
GCP_LOCATION_NAME = "GCP_LOCATION"
GEMINI_MODEL_ID_NAME = "GEMINI_MODEL_ID"

# --- Editor Settings ---
ACE_EDITOR_SETTINGS = {
    "language": "python",
    "theme": "monokai",
    "font_size": 14,
    "show_gutter": True,
    "wrap": True,
}
ACE_EDITOR_DEFAULT_CODE = "# Code goes here\n"

# --- Default Session State ---
SESSION_STATE_DEFAULTS = {
    "messages": [],
    "system_role_defined": False,
    "total_usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
    "is_generating": False,
    "last_usage_info": None,
    "python_canvases": [ACE_EDITOR_DEFAULT_CODE],
    "multi_code_enabled": False,
    "stop_generation": False,
    "canvas_key_counter": 0,
    "reasoning_effort": "high",
    "debug_logs": [],
    "current_model_id": "gemini-3-pro-preview" # UIで切り替え可能にする
}

# 選択可能なモデルリスト
AVAILABLE_MODELS = [
    "gemini-3-pro-preview",
    "gemini-3-flash-preview",
    "gemini-2.0-flash-001",
    "gemini-1.5-pro-002",
    "gemini-1.5-flash-002"
]

# --- UI Texts ---
class UITexts:
    APP_TITLE = "🤖Codex-Chat_With_Gemini3"
    SIDEBAR_HEADER = "設定"
    RESET_BUTTON_LABEL = "会話履歴をリセット"
    CODEX_MINI_INFO = "`Gemini 3 Pro` allows processing massive codebases with its 1M context window."
    HISTORY_SUBHEADER = "会話履歴 (JSON)"
    DOWNLOAD_HISTORY_BUTTON = "会話履歴をダウンロード"
    UPLOAD_HISTORY_LABEL = "JSONで会話を再開"
    HISTORY_LOADED_SUCCESS = "History and Canvases loaded."
    OLD_HISTORY_FORMAT_WARNING = "Old format detected. Code could not be restored."
    JSON_FORMAT_ERROR = "Unsupported JSON format."
    JSON_LOAD_ERROR = "JSON load error: {e}"

    EDITOR_SUBHEADER = "🔧 コードエディタ"
    MULTI_CODE_CHECKBOX = "マルチコードを有効化"
    ADD_CANVAS_BUTTON = "Canvasを追加"
    CLEAR_BUTTON = "クリア"
    REVIEW_BUTTON = "レビュー"
    VALIDATE_BUTTON = "検証"

    SYSTEM_PROMPT_HEADER = "Set AI System Role"
    SYSTEM_PROMPT_TEXT_AREA_LABEL = "System Role"
    START_CHAT_BUTTON = "Start Chat"

    ENV_VARS_ERROR = "Error: Environment variable '{vars}' is not set."
    CLIENT_INIT_ERROR = "SDK initialization failed: {e}"
    API_REQUEST_ERROR = "API request failed: {e}"
    
    NO_CODE_TO_VALIDATE = "No code to validate."
    VALIDATE_SPINNER_MULTI = "Validating Canvas-{i}..."
    VALIDATE_SPINNER_SINGLE = "Validating code..."
    
    PYLINT_SYNTAX_ERROR = "⚠️ Syntax error detected by pylint."

    STOP_GENERATION_BUTTON = "Stop"
    CHAT_INPUT_PLACEHOLDER = "Message Gemini 3 Pro..."
    
    REVIEW_PROMPT_SINGLE = "### Reference Code (Canvas)\nPlease review this code and suggest improvements."
    REVIEW_PROMPT_MULTI = "### Reference Code (Canvas-{i})\nPlease review this canvas and suggest improvements."