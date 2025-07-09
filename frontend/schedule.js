// 時刻表データ（バスの種類別）
const BUS_SCHEDULE = {
    engineering: {
        direct: [
            { hour: 9, minutes: [20, 30] },
            { hour: 11, minutes: [20] },
            { hour: 12, minutes: [10, 15, 35] },
            { hour: 15, minutes: [10, 15] },
            { hour: 16, minutes: [0, 55] },
            { hour: 17, minutes: [0] },
            { hour: 18, minutes: [30, 35] }
        ],
        via_minoo: [
            { hour: 7, minutes: [55] },
            { hour: 8, minutes: [30, 55] },
            { hour: 10, minutes: [0, 40] },
            { hour: 11, minutes: [15] },
            { hour: 12, minutes: [40] },
            { hour: 13, minutes: [35] },
            { hour: 14, minutes: [15] },
            { hour: 16, minutes: [5] },
            { hour: 18, minutes: [5, 40] },
            { hour: 19, minutes: [0, 25] },
            { hour: 20, minutes: [10] }
        ]
    },
    humanities: {
        direct: [
            { hour: 9, minutes: [25, 35] },
            { hour: 11, minutes: [25] },
            { hour: 12, minutes: [15, 20, 40] },
            { hour: 15, minutes: [15, 20] },
            { hour: 16, minutes: [4] },
            { hour: 17, minutes: [0, 5] },
            { hour: 18, minutes: [35, 40] }
        ],
        via_minoo: [
            { hour: 8, minutes: [0, 35] },
            { hour: 9, minutes: [0] },
            { hour: 10, minutes: [5, 45] },
            { hour: 11, minutes: [20] },
            { hour: 12, minutes: [45] },
            { hour: 13, minutes: [40] },
            { hour: 14, minutes: [20] },
            { hour: 16, minutes: [10] },
            { hour: 18, minutes: [10, 45] },
            { hour: 19, minutes: [5, 30] },
            { hour: 20, minutes: [15] }
        ]
    }
};

// 時刻表データをグローバルに公開
window.BUS_SCHEDULE = BUS_SCHEDULE;
