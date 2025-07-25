// API設定
const API_CONFIG = {
    // フロントエンドサーバーの中継URLを指定（例: 本番では https://yourdomain.com/api/... になる）
    BASE_URL: '', // プロキシを前提に

    // APIエンドポイント（中継を前提に相対パスで）
    ENDPOINTS: {
        BUS_STATUS: '/status' // Updated to match proxy settings
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
