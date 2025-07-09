// API設定
const API_CONFIG = {
    // ベースURL（本番環境では適切なURLに変更してください）
    BASE_URL: '',
    
    // APIエンドポイント
    ENDPOINTS: {
        BUS_STATUS: 'http://172.16.1.33:8000/api/status'
    }
};

// バスの種類設定
const BUS_TYPES = {
    DIRECT: {
        id: 'direct',
        name: '豊中キャンパス直通',
        shortName: '直通',
        color: '#0055a4',
        description: '豊中キャンパスへ直通するバス'
    },
    VIA_MINOO: {
        id: 'via_minoo',
        name: '箕面キャンパス経由',
        shortName: '箕面経由',
        color: '#28a745',
        description: '箕面キャンパスを経由して豊中キャンパスに向かうバス'
    }
};

// 設定をグローバルに公開
window.API_CONFIG = API_CONFIG;
window.BUS_TYPES = BUS_TYPES;
