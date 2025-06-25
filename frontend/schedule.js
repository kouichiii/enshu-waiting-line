// 時刻表データ（バスの種類別）
const BUS_SCHEDULE = {
    engineering: {
        direct: [
            { hour: 7, minutes: [30, 55] },
            { hour: 8, minutes: [10, 40] },
            { hour: 9, minutes: [10, 40] },
            { hour: 10, minutes: [10, 40] },
            { hour: 11, minutes: [10, 40] },
            { hour: 12, minutes: [10, 40] },
            { hour: 13, minutes: [10, 40] },
            { hour: 14, minutes: [10, 40] },
            { hour: 15, minutes: [10, 40] },
            { hour: 16, minutes: [10, 40] },
            { hour: 17, minutes: [10, 40] },
            { hour: 18, minutes: [10] }
        ],
        via_minoo: [
            { hour: 7, minutes: [45] },
            { hour: 8, minutes: [25, 55] },
            { hour: 9, minutes: [25, 55] },
            { hour: 10, minutes: [25, 55] },
            { hour: 11, minutes: [25, 55] },
            { hour: 12, minutes: [25, 55] },
            { hour: 13, minutes: [25, 55] },
            { hour: 14, minutes: [25, 55] },
            { hour: 15, minutes: [25, 55] },
            { hour: 16, minutes: [25, 55] },
            { hour: 17, minutes: [25, 55] },
            { hour: 18, minutes: [25, 40] }
        ]
    },
    humanities: {
        direct: [
            { hour: 7, minutes: [35] },
            { hour: 8, minutes: [15, 45] },
            { hour: 9, minutes: [15, 45] },
            { hour: 10, minutes: [15, 45] },
            { hour: 11, minutes: [15, 45] },
            { hour: 12, minutes: [15, 45] },
            { hour: 13, minutes: [15, 45] },
            { hour: 14, minutes: [15, 45] },
            { hour: 15, minutes: [15, 45] },
            { hour: 16, minutes: [15, 45] },
            { hour: 17, minutes: [15, 45] },
            { hour: 18, minutes: [15] }
        ],
        via_minoo: [
            { hour: 7, minutes: [50] },
            { hour: 8, minutes: [0, 30] },
            { hour: 9, minutes: [0, 30] },
            { hour: 10, minutes: [0, 30] },
            { hour: 11, minutes: [0, 30] },
            { hour: 12, minutes: [0, 30] },
            { hour: 13, minutes: [0, 30] },
            { hour: 14, minutes: [0, 30] },
            { hour: 15, minutes: [0, 30] },
            { hour: 16, minutes: [0, 30] },
            { hour: 17, minutes: [0, 30] },
            { hour: 18, minutes: [0, 30] }
        ]
    }
};

// 時刻表データをグローバルに公開
window.BUS_SCHEDULE = BUS_SCHEDULE;
